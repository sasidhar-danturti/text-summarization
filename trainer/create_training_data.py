import struct
from tensorflow.core.example import example_pb2
import json
import os

output_filename ="train_data"

with open(output_filename, 'wb') as writer:

  path_to_json = '/home/synerzip/Sasidhar/Learning/Tensorflow/textsum/trainer/data/json/'
  json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

  for index, js in enumerate(json_files):
    with open(os.path.join(path_to_json, js)) as json_file:
        tf_example = example_pb2.Example()
        json_text = json.load(json_file)
        tf_example.features.feature['article'].bytes_list.value.extend([str(json_text["article"])])
        tf_example.features.feature['abstract'].bytes_list.value.extend([str(json_text["summary"])])
        tf_example_str = tf_example.SerializeToString()
        str_len = len(tf_example_str)
        writer.write(struct.pack('q', str_len))
        writer.write(struct.pack('%ds' % str_len, tf_example_str))


# with open(output_filename, 'wb') as writer:
#   body = 'body'
#   title = 'title'
#   print(type(body))
#   print(type([body]))
#   tf_example = example_pb2.Example()
#   tf_example.features.feature['article'].bytes_list.value.extend([body])
#   tf_example.features.feature['abstract'].bytes_list.value.extend([title])
#   tf_example_str = tf_example.SerializeToString()
#   str_len = len(tf_example_str)
#   writer.write(struct.pack('q', str_len))
#   writer.write(struct.pack('%ds' % str_len, tf_example_str))