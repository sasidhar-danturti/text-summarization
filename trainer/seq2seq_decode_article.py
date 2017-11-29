# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Module for decoding."""

import os
import time
import numpy as np
import beam_search
import data
# from six.moves import xrange
import tensorflow as tf

FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_integer('max_decode_steps', 1000000,
                            'Number of decoding steps.')
tf.app.flags.DEFINE_integer('decode_batches_per_ckpt', 8000,
                            'Number of batches to decode before restoring next '
                            'checkpoint')

DECODE_LOOP_DELAY_SECS = 60
DECODE_IO_FLUSH_INTERVAL = 100


class BSDecoder(object):
  """Beam search decoder."""

  def __init__(self, model, data, hps, vocab):
    """Beam search decoding.

    Args:
      model: The seq2seq attentional model.
      batch_reader: The batch data reader.
      hps: Hyperparamters.
      vocab: Vocabulary
    """
    self._model = model
    self._model.build_graph()
    self._hps = hps
    self._vocab = vocab
    self._saver = tf.train.Saver()
    self._data = data
    self._max_article_sentences = 100
    self.sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
    saver = self._saver
    ckpt_state = tf.train.get_checkpoint_state(FLAGS.log_root)

    if (ckpt_state and ckpt_state.model_checkpoint_path):
        tf.logging.info('No model to decode yet at %s', FLAGS.log_root)
        tf.logging.info('checkpoint path %s', ckpt_state.model_checkpoint_path)
        ckpt_path = os.path.join(FLAGS.log_root, os.path.basename(ckpt_state.model_checkpoint_path))
        tf.logging.info('renamed checkpoint path %s', ckpt_path)
        saver.restore(self.sess, ckpt_path)


  def get_article_inputs(self,article):

    pad_id = self._vocab.WordToId(data.PAD_TOKEN)

    article_sentences = [sent.strip() for sent in
                         data.ToSentences(article, include_token=False)]

    enc_inputs = []

    # Convert first N sentences to word IDs, stripping existing <s> and </s>.
    for i in xrange(min(self._max_article_sentences,
                        len(article_sentences))):
      enc_inputs += data.GetWordIds(article_sentences[i], self._vocab)

    # Now len(enc_inputs) should be <= enc_timesteps, and
    # len(targets) = len(dec_inputs) should be <= dec_timesteps

    enc_input_len = len(enc_inputs)

    # Pad if necessary
    while len(enc_inputs) < self._hps.enc_timesteps:
      enc_inputs.append(pad_id)

    enc_batch = np.zeros(
        (self._hps.batch_size, self._hps.enc_timesteps), dtype=np.int32)
    enc_input_lens = np.zeros(
        (self._hps.batch_size), dtype=np.int32)


    for i in xrange(self._hps.batch_size):
      enc_input_lens[i] = enc_input_len
      enc_batch[i, :] = enc_inputs[:]

    return (enc_batch, enc_input_lens)

  def Decode(self,article):
    """Restore a checkpoint and decode it.

    Args:
      saver: Tensorflow checkpoint saver.
      sess: Tensorflow session.
    Returns:
      If success, returns true, otherwise, false.
    """

    (article_batch,  article_lens) = self.get_article_inputs(article)

    bs = beam_search.BeamSearch(
        self._model, 4,
        self._vocab.WordToId(data.SENTENCE_START),
        self._vocab.WordToId(data.SENTENCE_END),
        self._hps.dec_timesteps)

    article_batch_cp = article_batch.copy()

    article_lens_cp = article_lens.copy()
    best_beam = bs.BeamSearch(self.sess, article_batch_cp, article_lens_cp)[0]

    decode_output = [int(t) for t in best_beam.tokens[1:]]
    decoded_text = ' '.join(data.Ids2Words(decode_output, self._vocab))

    return decoded_text


  def _DecodeBatch(self, article, abstract, output_ids):
    """Convert id to words and writing results.

    Args:
      article: The original article string.
      abstract: The human (correct) abstract string.
      output_ids: The abstract word ids output by machine.
    """
    decoded_output = ' '.join(data.Ids2Words(output_ids, self._vocab))
    end_p = decoded_output.find(data.SENTENCE_END, 0)
    if end_p != -1:
      decoded_output = decoded_output[:end_p]
    tf.logging.info('article:  %s', article)
    tf.logging.info('abstract: %s', abstract)
    tf.logging.info('decoded:  %s', decoded_output)
    self._decode_io.Write(abstract, decoded_output.strip())
