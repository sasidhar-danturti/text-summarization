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

"""Trains a seq2seq model.

WORK IN PROGRESS.

Implement "Abstractive Text Summarization using Sequence-to-sequence RNNS and
Beyond."

"""
import sys
import time

import tensorflow as tf
import batch_reader
import data
import seq2seq_decode_article
import seq2seq_attention_model
import json

from flask import Flask, request
app = Flask(__name__)

FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string('data_path','gs://text-summarization-webapp.appspot.com/data/data', 'data path')
tf.app.flags.DEFINE_string('vocab_path','gs://text-summarization-webapp.appspot.com/data/vocab_data/vocab', 'Path expression to text vocabulary file.')
tf.app.flags.DEFINE_string('article_key', 'article',
                           'tf.Example feature key for article.')
tf.app.flags.DEFINE_string('abstract_key', 'abstract',
                           'tf.Example feature key for abstract.')
tf.app.flags.DEFINE_string('log_root','gs://text-summarization-webapp.appspot.com/data/log_root',  'Directory for model root.')
tf.app.flags.DEFINE_string('train_dir', 'log_root/train', 'Directory for train.')
tf.app.flags.DEFINE_string('eval_dir', 'log_root/eval', 'Directory for eval.')
tf.app.flags.DEFINE_string('decode_dir', '/home/synerzip/Sasidhar/Learning/Tensorflow/textsum/log_root/decode', 'Directory for decode summaries.')
tf.app.flags.DEFINE_string('mode', 'decode', 'train/eval/decode mode')
tf.app.flags.DEFINE_integer('max_run_steps', 10,
                            'Maximum number of run steps.')
tf.app.flags.DEFINE_integer('max_article_sentences', 2,
                            'Max number of first sentences to use from the '
                            'article')
tf.app.flags.DEFINE_integer('max_abstract_sentences', 100,
                            'Max number of first sentences to use from the '
                            'abstract')
tf.app.flags.DEFINE_integer('beam_size', 4,
                            'beam size for beam search decoding.')
tf.app.flags.DEFINE_integer('eval_interval_secs', 60, 'How often to run eval.')
tf.app.flags.DEFINE_integer('checkpoint_secs', 60, 'How often to checkpoint.')
tf.app.flags.DEFINE_bool('use_bucketing', False,
                         'Whether bucket articles of similar length.')
tf.app.flags.DEFINE_bool('truncate_input', False,
                         'Truncate inputs that are too long. If False, '
                         'examples that are too long are discarded.')
tf.app.flags.DEFINE_integer('num_gpus', 0, 'Number of gpus used.')
tf.app.flags.DEFINE_integer('random_seed', 111, 'A seed value for randomness.')


vocab = data.Vocab(FLAGS.vocab_path, 10003)
#Check for presence of required special tokens.
#print(vocab.CheckVocab(data.PAD_TOKEN))
# assert vocab.CheckVocab(data.PAD_TOKEN) > 0
# assert vocab.CheckVocab(data.UNKNOWN_TOKEN) >= 0
# assert vocab.CheckVocab(data.SENTENCE_START) > 0
# assert vocab.CheckVocab(data.SENTENCE_END) > 0

batch_size = 4
if FLAGS.mode == 'decode':
    batch_size = FLAGS.beam_size

hps = seq2seq_attention_model.HParams(
  mode=FLAGS.mode,  # train, eval, decode
  min_lr=0.01,  # min learning rate.
  lr=0.15,  # learning rate
  batch_size=batch_size,
  enc_layers=4,
  enc_timesteps=120,
  dec_timesteps=50,
  min_input_len=2,  # discard articles/summaries < than this
  num_hidden=256,  # for rnn cell
  emb_dim=128,  # If 0, don't use embedding
  max_grad_norm=2,
  num_softmax_samples=4096)  # If 0, no sampled softmax.


tf.set_random_seed(FLAGS.random_seed)

decode_mdl_hps = hps
# Only need to restore the 1st step and reuse it since
# we keep and feed in state for each step's output.
decode_mdl_hps = hps._replace(dec_timesteps=1)
model = seq2seq_attention_model.Seq2SeqAttentionModel(
    decode_mdl_hps, vocab, num_gpus=FLAGS.num_gpus)

decoder = seq2seq_decode_article.BSDecoder(model, data, hps, vocab)

@app.route("/decode", methods=['POST'])
def decode():
    # print(vocab.CheckVocab(data.PAD_TOKEN))
    input_data =json.loads((request.data))
    #print(input_data.get("input"))
    return decoder.Decode(input_data.get("input"))

import os
import vocab
@app.route("/train",methods=['POST'])
def summarize():
    # creatthe vocabulary file first and then  submit the job
    v = vocab.Vocab("gs://text-summarization-webapp.appspot.com/data/data","data/vocab")
    v.create_vocab_file()
    input_data  = json.loads(request.data)
    os.system("sudo sh submit_training_job.sh " + str(input_data.get("input")))
    return "done"

#summarize()
#print(decoder.Decode("abcd 1234566 abcd"))
