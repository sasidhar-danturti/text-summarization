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

import json

import tensorflow as tf
from flask import Flask, request
from flask_cors import CORS

import seq2seq_decode_article
import seq2seq_attention_model
import vocab
import data

app = Flask(__name__)
CORS(app)

BUCKET_NAME ="gs://text-summarization-webapp.appspot.com"

DATA_PATH = BUCKET_NAME + "/data/data"
VOCAB_PATH = BUCKET_NAME + "/data/vocab_data/vocab"
LOG_ROOT = BUCKET_NAME + "/models/job_new_1000_steps"

# DATA_PATH = "/home/synerzip/Sasidhar/Learning/Tensorflow/textsum/data/reviews"
# VOCAB_PATH = "/home/synerzip/Sasidhar/Learning/Tensorflow/textsum/data/vocab_1"
# LOG_ROOT = "/home/synerzip/Sasidhar/Learning/Tensorflow/textsum/log_root"


FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string('data_path',DATA_PATH, 'data path')
tf.app.flags.DEFINE_string('vocab_path',VOCAB_PATH, 'Path expression to text vocabulary file.')
tf.app.flags.DEFINE_string('log_root',LOG_ROOT,  'Directory for model root.')

tf.app.flags.DEFINE_integer('beam_size', 4,
                            'beam size for beam search decoding.')
tf.app.flags.DEFINE_integer('random_seed', 111, 'A seed value for randomness.')
tf.app.flags.DEFINE_integer('num_gpus', 0, 'Number of gpus used.')

vocab = data.Vocab(FLAGS.vocab_path, 10003)

batch_size = 4

hps = seq2seq_attention_model.HParams(
  mode='decode',
  min_lr=0.01,  # min learning rate.
  lr=0.15,  # learning rate
  batch_size=batch_size,
  enc_layers=4,
  enc_timesteps=200,
  dec_timesteps=30,
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
    print(request.data)
    input_data =json.loads(request.data).get("input")
    # input_data ="abcd abcdon.dumpsabcd"
    resp = decoder.Decode(input_data)

    return json.dumps({"responseText": resp})


@app.route("/train",methods=['POST'])
def train():
    # creatthe vocabulary file first and then  submit the job
    input_data  = json.loads(request.data)
    files_to_exclude = ",".join(input_data.get("files_to_exclude"))
    v = vocab.Vocab("gs://text-summarization-webapp.appspot.com/data/data","data/vocab",files_to_exclude)
    v.create_vocab_file()
    os.system("sudo sh submit_training_job.sh {} {}".format(str(input_data.get("input")),files_to_exclude))
    return json.dumps({"responseText": "Submitted training job"})


if __name__ == "__main__":
    app.run(host='0.0.0.0')