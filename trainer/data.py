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

"""Data batchers for data described in ..//data_prep/README.md."""

import glob
import random
import struct
import sys
import os

from tensorflow.core.example import example_pb2
import tensorflow as tf

# Special tokens
PARAGRAPH_START = '<p>'
PARAGRAPH_END = '</p>'
SENTENCE_START = '<s>'
SENTENCE_END = '</s>'
UNKNOWN_TOKEN = '<UNK>'
PAD_TOKEN = '<PAD>'
DOCUMENT_START = '<d>'
DOCUMENT_END = '</d>'

# filename_queue = tf.train.string_input_producer(["/home/synerzip/Sasidhar/Learning/Tensorflow/textsum/trainer/data/data"])
# reader = tf.TextLineReader()
#
# key, value = reader.read(filename_queue)
# record_defaults = [[""]]
#
# col1 = tf.decode_csv(
#     value, record_defaults=record_defaults)
# features = tf.stack([col1])
#
# with tf.Session() as sess:
#   # Start populating the filename queue.
#   coord = tf.train.Coordinator()
#   threads = tf.train.start_queue_runners(coord=coord)
#
#   for i in range(1000):
#     # Retrieve a single instance:
#     data = sess.run([features])[:8]
#     str_len = struct.unpack('q', data)[0]
#     # example_str = struct.unpack('%ds' % str_len, reader.read(str_len))[0]
#     # print(example_pb2.Example.FromString(example_str))
#     print(data)
#
#   coord.request_stop()
#   coord.join(threads)

import json


# #
# def getresult():
#   print("in  dsf")
#   folder_list =["/home/synerzip/Sasidhar/Learning/Tensorflow/textsum/trainer/data/json"]
#   for folder in folder_list:
#     path_to_json = folder
#     json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
#     for index, js in enumerate(json_files):
#       with open(os.path.join(path_to_json, js)) as json_file:
#         tf_example = example_pb2.Example()
#         json_text = json.load(json_file)
#         tf_example.features.feature['article'].bytes_list.value.extend([str(json_text["article"])])
#         tf_example.features.feature['abstract'].bytes_list.value.extend([str(json_text["summary"])])
#         tf_example_str = tf_example.SerializeToString()
#         yield example_pb2.Example.FromString(tf_example_str)
#         # print(example_pb2.Example.FromString(tf_example_str))
#
# getresult()

class Vocab(object):
    """Vocabulary class for mapping words and ids."""

    def __init__(self, vocab_file, max_size):
        self._word_to_id = {}
        self._id_to_word = {}
        self._count = 0
        #
        filename_queue = tf.train.string_input_producer([vocab_file])
        reader = tf.TextLineReader()

        key, value = reader.read(filename_queue)
        record_defaults = [[""], [1]]
        col1, col2 = tf.decode_csv(
            value, record_defaults=record_defaults, field_delim=" ")
        features = tf.stack([col1])

        with tf.Session() as sess:
            # Start populating the filename queue.
            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(coord=coord)

            for i in range(max_size):
                # Retrieve a single instance:
                example, label = sess.run([features, col2])
                self._word_to_id[example[0]] = self._count
                self._id_to_word[self._count] = example[0]
                self._count += 1

            coord.request_stop()
            coord.join(threads)
            #

            # with open(vocab_file, 'r') as vocab_f:
            #   for line in vocab_f:
            #     pieces = line.split()
            #     if len(pieces) != 2:
            #       sys.stderr.write('Bad line: %s\n' % line)
            #       continue
            #     if pieces[0] in self._word_to_id:
            #       raise ValueError('Duplicated word: %s.' % pieces[0])
            #     self._word_to_id[pieces[0]] = self._count
            #     self._id_to_word[self._count] = pieces[0]
            #     self._count += 1
            #     if self._count > max_size:
            #       raise ValueError('Too many words: >%d.' % max_size)

    def CheckVocab(self, word):
        if word not in self._word_to_id:
            return None
        return self._word_to_id[word]

    def WordToId(self, word):
        if word not in self._word_to_id:
            return self._word_to_id[UNKNOWN_TOKEN]
        return self._word_to_id[word]

    def IdToWord(self, word_id):
        if word_id not in self._id_to_word:
            raise ValueError('id not found in vocab: %d.' % word_id)
        return self._id_to_word[word_id]

    def NumIds(self):
        return self._count


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

"""Data batchers for data described in ..//data_prep/README.md."""

import glob
import random
import struct
import sys
import ast
import os

from tensorflow.core.example import example_pb2
import tensorflow as tf

# Special tokens
PARAGRAPH_START = '<p>'
PARAGRAPH_END = '</p>'
SENTENCE_START = '<s>'
SENTENCE_END = '</s>'
UNKNOWN_TOKEN = '<UNK>'
PAD_TOKEN = '<PAD>'
DOCUMENT_START = '<d>'
DOCUMENT_END = '</d>'

# filename_queue = tf.train.string_input_producer(["/home/synerzip/Sasidhar/Learning/Tensorflow/textsum/trainer/data/data"])
# reader = tf.TextLineReader()
#
# key, value = reader.read(filename_queue)
# record_defaults = [[""]]
#
# col1 = tf.decode_csv(
#     value, record_defaults=record_defaults)
# features = tf.stack([col1])
#
# with tf.Session() as sess:
#   # Start populating the filename queue.
#   coord = tf.train.Coordinator()
#   threads = tf.train.start_queue_runners(coord=coord)
#
#   for i in range(1000):
#     # Retrieve a single instance:
#     data = sess.run([features])[:8]
#     str_len = struct.unpack('q', data)[0]
#     # example_str = struct.unpack('%ds' % str_len, reader.read(str_len))[0]
#     # print(example_pb2.Example.FromString(example_str))
#     print(data)
#
#   coord.request_stop()
#   coord.join(threads)

import json


# #
# def getresult():
#   print("in  dsf")
#   folder_list =["/home/synerzip/Sasidhar/Learning/Tensorflow/textsum/trainer/data/json"]
#   for folder in folder_list:
#     path_to_json = folder
#     json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
#     for index, js in enumerate(json_files):
#       with open(os.path.join(path_to_json, js)) as json_file:
#         tf_example = example_pb2.Example()
#         json_text = json.load(json_file)
#         tf_example.features.feature['article'].bytes_list.value.extend([str(json_text["article"])])
#         tf_example.features.feature['abstract'].bytes_list.value.extend([str(json_text["summary"])])
#         tf_example_str = tf_example.SerializeToString()
#         yield example_pb2.Example.FromString(tf_example_str)
#         # print(example_pb2.Example.FromString(tf_example_str))
#
# getresult()

class Vocab(object):
    """Vocabulary class for mapping words and ids."""

    def __init__(self, vocab_file, max_size):
        self._word_to_id = {}
        self._id_to_word = {}
        self._count = 0
        #
        filename_queue = tf.train.string_input_producer([vocab_file])
        reader = tf.TextLineReader()

        key, value = reader.read(filename_queue)
        record_defaults = [[""], [1]]
        col1, col2 = tf.decode_csv(
            value, record_defaults=record_defaults, field_delim=" ")
        features = tf.stack([col1])

        with tf.Session() as sess:
            # Start populating the filename queue.
            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(coord=coord)

            for i in range(max_size):
                # Retrieve a single instance:
                example, label = sess.run([features, col2])
                self._word_to_id[example[0]] = self._count
                self._id_to_word[self._count] = example[0]
                self._count += 1

            coord.request_stop()
            coord.join(threads)
            #

            # with open(vocab_file, 'r') as vocab_f:
            #   for line in vocab_f:
            #     pieces = line.split()
            #     if len(pieces) != 2:
            #       sys.stderr.write('Bad line: %s\n' % line)
            #       continue
            #     if pieces[0] in self._word_to_id:
            #       raise ValueError('Duplicated word: %s.' % pieces[0])
            #     self._word_to_id[pieces[0]] = self._count
            #     self._id_to_word[self._count] = pieces[0]
            #     self._count += 1
            #     if self._count > max_size:
            #       raise ValueError('Too many words: >%d.' % max_size)

    def CheckVocab(self, word):
        if word not in self._word_to_id:
            return None
        return self._word_to_id[word]

    def WordToId(self, word):
        if word not in self._word_to_id:
            return self._word_to_id[UNKNOWN_TOKEN]
        return self._word_to_id[word]

    def IdToWord(self, word_id):
        if word_id not in self._id_to_word:
            raise ValueError('id not found in vocab: %d.' % word_id)
        return self._id_to_word[word_id]

    def NumIds(self):
        return self._count


#
def ExampleGen_Old(data_path, num_epochs=None):
  """Generates tf.Examples from path of data files.

    Binary data format: <length><blob>. <length> represents the byte size
    of <blob>. <blob> is serialized tf.Example proto. The tf.Example contains
    the tokenized article text and summary.

  Args:
    data_path: path to tf.Example data files.
    num_epochs: Number of times to go through the data. None means infinite.

  Yields:
    Deserialized tf.Example.

  If there are multiple files specified, they accessed in a random order.
  """
  data_path = "/home/synerzip/Sasidhar/Learning/Tensorflow/textsum/trainer/data/data"
  epoch = 0
  while True:
    if num_epochs is not None and epoch >= num_epochs:
      break
    filelist = glob.glob(data_path)
    assert filelist, 'Empty filelist.'
    random.shuffle(filelist)
    for f in filelist:
      reader = open(f, 'rb')
      while True:
        len_bytes = reader.read(8)
        if not len_bytes:
            break
        str_len = struct.unpack('q', len_bytes)[0]
        example_str = struct.unpack('%ds' % str_len, reader.read(str_len))[0]

        yield example_pb2.Example.FromString(example_str)

    epoch += 1



def ExampleGen(data_path, num_epochs=None):
    """Generates tf.Examples from path of data files.
  ExampleGen
      Binary data format: <length><blob>. <length> represents the byte size
      of <blob>. <blob> is serialized tf.Example proto. The tf.Example contains
      the tokenized article text and summary.

    Args:
      data_path: path to tf.Example data files.
      num_epochs: Number of times to go through the data. None means infinite.

    Yields:
      Deserialized tf.Example.

    If there are multiple files specified, they accessed in a random order.
    """
    # epoch = 0
    # while True:
    #     fileselection_path = data_path + "/*.json"
    #     filenames = tf.train.match_filenames_once(fileselection_path)
    #     count_num_files = tf.size(filenames)
    #     filename_queue = tf.train.string_input_producer(filenames)
    #     reader = tf.WholeFileReader()
    #     filename, _ = reader.read(filename_queue)
    #     counter = 0
    #     with tf.Session() as sess:
    #         sess.run([tf.global_variables_initializer(), tf.local_variables_initializer()])
    #         num_files = sess.run(count_num_files)
    #         if counter >= num_files:
    #          break
    #         coord = tf.train.Coordinator()
    #         threads = tf.train.start_queue_runners(coord=coord)
    #
    #         for i in range(num_files):
    #             csv_file = sess.run(filename)
    #             tf_example = example_pb2.Example()
    #             filename_queue_sub = tf.train.string_input_producer([csv_file])
    #             reader_sub = tf.WholeFileReader()
    #             _, file_contents_sub = reader_sub.read(filename_queue_sub)
    #
    #             threads_sub = tf.train.start_queue_runners(coord=coord)
    #             json_content = sess.run(file_contents_sub)
    #             json_text = json.loads(json_content)
    #             article = str(json_text['article'])
    #             summary = str(json_text["summary"])
    #             tf_example.features.feature['article'].bytes_list.value.extend([article])
    #             tf_example.features.feature['abstract'].bytes_list.value.extend([summary])
    #             counter += 1
    #             yield tf_example
    #
    #         coord.request_stop()
    #         coord.join(threads)
    #         coord.join(threads_sub)
    #     epoch += 1

    epoch = 0
    filenames = tf.train.match_filenames_once(data_path +"/*.json")
    count_num_files = tf.size(filenames)
    filename_queue = tf.train.string_input_producer(filenames)
    reader = tf.WholeFileReader()
    filename, _ = reader.read(filename_queue)

    with tf.Session() as sess:
        sess.run([tf.global_variables_initializer(), tf.local_variables_initializer()])
        num_files = sess.run(count_num_files)
        counter =0
        while True:
            if counter >= num_files:
                break
            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(coord=coord)


            for i in range(num_files):
                csv_file = sess.run(filename)
                tf_example = example_pb2.Example()
                filename_queue_sub = tf.train.string_input_producer([csv_file])
                reader_sub = tf.WholeFileReader()
                _, file_contents_sub = reader_sub.read(filename_queue_sub)
                threads_sub = tf.train.start_queue_runners(coord=coord)
                json_content = sess.run(file_contents_sub)
                json_text = json.loads(json.dumps(ast.literal_eval(json_content)))
                article = str(json_text['article'].encode('ascii','ignore'))
                summary = str(json_text["summary"].encode('ascii','ignore'))
                tf_example.features.feature['article'].bytes_list.value.extend([article])
                tf_example.features.feature['abstract'].bytes_list.value.extend([summary])
                counter = counter +1
                yield(tf_example)


            coord.request_stop()
            coord.join(threads)
            coord.join(threads_sub)
    epoch += 1

        # path_to_json ="data/json"
        # json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
        # file_count= len(json_files)
        # count = 0
        #
        # while True:
        #   if count >= file_count:
        #     break
        #   for index, js in enumerate(json_files):
        #     tf_example = example_pb2.Example()
        #     with open(os.path.join(path_to_json, js)) as json_file:
        #       json_text = json.load(json_file)
        #       article = str(json_text["article"])
        #       summary = str(json_text["summary"])
        #       tf_example.features.feature['article'].bytes_list.value.extend([article])
        #       tf_example.features.feature['abstract'].bytes_list.value.extend([summary])
        #       # tf_example_str = tf_example.SerializeToString()
        #       # str_len = len(tf_example_str)
        #       # writer.write(struct.pack('q', str_len))
        #       # writer.write(struct.pack('%ds' % str_len, tf_example_str))
        #
        #       count = count +1
        #       yield tf_example
        #



        # filename_queue = tf.train.string_input_producer(filelist)
        # reader = tf.TextLineReader()
        #
        # key, value = reader.read(filename_queue)
        # record_defaults = [[""]]
        # col1 = tf.decode_csv(
        #     value, record_defaults=record_defaults)
        # features = tf.stack([col1])
        #
        # with tf.Session() as sess:
        #   # Start populating the filename queue.
        #   coord = tf.train.Coordinator()
        #   threads = tf.train.start_queue_runners(coord=coord)
        #
        #   for i in range(1000):
        #     # Retrieve a single instance:
        #     data = sess.run([features])
        #     str_len = struct.unpack('q', data)[0]
        #     example_str = struct.unpack('%ds' % str_len, reader.read(str_len))[0]
        #     yield example_pb2.Example.FromString(example_str)
        #
        #   coord.request_stop()
        #   coord.join(threads)

        # epoch += 1


def Pad(ids, pad_id, length):
    """Pad or trim list to len length.

    Args:
      ids: list of ints to pad
      pad_id: what to pad with
      length: length to pad or trim to

    Returns:
      ids trimmed or padded with pad_id
    """
    assert pad_id is not None
    assert length is not None

    if len(ids) < length:
        a = [pad_id] * (length - len(ids))
        return ids + a
    else:
        return ids[:length]


def GetWordIds(text, vocab, pad_len=None, pad_id=None):
    """Get ids corresponding to words in text.

    Assumes tokens separated by space.

    Args:
      text: a string
      vocab: TextVocabularyFile object
      pad_len: int, length to pad to
      pad_id: int, word id for pad symbol

    Returns:
      A list of ints representing word ids.
    """
    ids = []
    for w in text.split():
        i = vocab.WordToId(w)
        if i >= 0:
            ids.append(i)
        else:
            ids.append(vocab.WordToId(UNKNOWN_TOKEN))
    if pad_len is not None:
        return Pad(ids, pad_id, pad_len)
    return ids


def Ids2Words(ids_list, vocab):
    """Get words from ids.

    Args:
      ids_list: list of int32
      vocab: TextVocabulary object

    Returns:
      List of words corresponding to ids.
    """
    assert isinstance(ids_list, list), '%s  is not a list' % ids_list
    return [vocab.IdToWord(i) for i in ids_list]


def SnippetGen(text, start_tok, end_tok, inclusive=True):
    """Generates consecutive snippets between start and end tokens.

    Args:
      text: a string
      start_tok: a string denoting the start of snippets
      end_tok: a string denoting the end of snippets
      inclusive: Whether include the tokens in the returned snippets.

    Yields:
      String snippets
    """
    cur = 0
    while True:
        try:
            start_p = text.index(start_tok, cur)
            end_p = text.index(end_tok, start_p + 1)
            cur = end_p + len(end_tok)
            if inclusive:
                yield text[start_p:cur]
            else:
                yield text[start_p + len(start_tok):end_p]
        except ValueError as e:
            raise StopIteration('no more snippets in text: %s' % e)


def GetExFeatureText(ex, key):
    return ex.features.feature[key].bytes_list.value[0]


def ToSentences(paragraph, include_token=True):
    """Takes tokens of a paragraph and returns list of sentences.

    Args:
      paragraph: string, text of paragraph
      include_token: Whether include the sentence separation tokens result.

    Returns:
      List of sentence strings.
    """
    s_gen = SnippetGen(paragraph, SENTENCE_START, SENTENCE_END, include_token)
    return [s for s in s_gen]


# def ExampleGen(data_path, num_epochs=None):
#   """Generates tf.Examples from path of data files.
#
#     Binary data format: <length><blob>. <length> represents the byte size
#     of <blob>. <blob> is serialized tf.Example proto. The tf.Example contains
#     the tokenized article text and summary.
#
#   Args:
#     data_path: path to tf.Example data files.
#     num_epochs: Number of times to go through the data. None means infinite.
#
#   Yields:
#     Deserialized tf.Example.
#
#   If there are multiple files specified, they accessed in a random order.
#   """
#
#   path_to_json ="data/json"
#   json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
#   file_count= len(json_files)
#   count = 0
#   while True:
#     if count >= file_count:
#       break
#     for index, js in enumerate(json_files):
#       tf_example = example_pb2.Example()
#       with open(os.path.join(path_to_json, js)) as json_file:
#         json_text = json.load(json_file)
#         article = str(json_text["article"])
#         summary = str(json_text["summary"])
#         tf_example.features.feature['article'].bytes_list.value.extend([article])
#         tf_example.features.feature['abstract'].bytes_list.value.extend([summary])
#         # tf_example_str = tf_example.SerializeToString()
#         count = count +1
#         yield tf_example
#
#     # filename_queue = tf.train.string_input_producer(filelist)
#     # reader = tf.TextLineReader()
#     #
#     # key, value = reader.read(filename_queue)
#     # record_defaults = [[""]]
#     # col1 = tf.decode_csv(
#     #     value, record_defaults=record_defaults)
#     # features = tf.stack([col1])
#     #
#     # with tf.Session() as sess:
#     #   # Start populating the filename queue.
#     #   coord = tf.train.Coordinator()
#     #   threads = tf.train.start_queue_runners(coord=coord)
#     #
#     #   for i in range(1000):
#     #     # Retrieve a single instance:
#     #     data = sess.run([features])
#     #     str_len = struct.unpack('q', data)[0]
#     #     example_str = struct.unpack('%ds' % str_len, reader.read(str_len))[0]
#     #     yield example_pb2.Example.FromString(example_str)
#     #
#     #   coord.request_stop()
#     #   coord.join(threads)
#
#     # epoch += 1

def Pad(ids, pad_id, length):
    """Pad or trim list to len length.

    Args:
      ids: list of ints to pad
      pad_id: what to pad with
      length: length to pad or trim to

    Returns:
      ids trimmed or padded with pad_id
    """
    assert pad_id is not None
    assert length is not None

    if len(ids) < length:
        a = [pad_id] * (length - len(ids))
        return ids + a
    else:
        return ids[:length]


def GetWordIds(text, vocab, pad_len=None, pad_id=None):
    """Get ids corresponding to words in text.

    Assumes tokens separated by space.

    Args:
      text: a string
      vocab: TextVocabularyFile object
      pad_len: int, length to pad to
      pad_id: int, word id for pad symbol

    Returns:
      A list of ints representing word ids.
    """
    ids = []
    for w in text.split():
        i = vocab.WordToId(w)
        if i >= 0:
            ids.append(i)
        else:
            ids.append(vocab.WordToId(UNKNOWN_TOKEN))
    if pad_len is not None:
        return Pad(ids, pad_id, pad_len)
    return ids


def Ids2Words(ids_list, vocab):
    """Get words from ids.

    Args:
      ids_list: list of int32
      vocab: TextVocabulary object

    Returns:
      List of words corresponding to ids.
    """
    assert isinstance(ids_list, list), '%s  is not a list' % ids_list
    return [vocab.IdToWord(i) for i in ids_list]


def SnippetGen(text, start_tok, end_tok, inclusive=True):
    """Generates consecutive snippets between start and end tokens.

    Args:
      text: a string
      start_tok: a string denoting the start of snippets
      end_tok: a string denoting the end of snippets
      inclusive: Whether include the tokens in the returned snippets.

    Yields:
      String snippets
    """
    cur = 0
    while True:
        try:
            start_p = text.index(start_tok, cur)
            end_p = text.index(end_tok, start_p + 1)
            cur = end_p + len(end_tok)
            if inclusive:
                yield text[start_p:cur]
            else:
                yield text[start_p + len(start_tok):end_p]
        except ValueError as e:
            raise StopIteration('no more snippets in text: %s' % e)


def GetExFeatureText(ex, key):
    return ex.features.feature[key].bytes_list.value[0]


def ToSentences(paragraph, include_token=True):
    """Takes tokens of a paragraph and returns list of sentences.

    Args:
      paragraph: string, text of paragraph
      include_token: Whether include the sentence separation tokens result.

    Returns:
      List of sentence strings.
    """
    # s_gen = SnippetGen(paragraph, SENTENCE_START, SENTENCE_END, include_token)
    # return [s for s in s_gen]
    return paragraph.split(".")
