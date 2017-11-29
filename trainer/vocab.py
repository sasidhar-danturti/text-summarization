import tensorflow as tf
import json
import collections
import ast

class Vocab:

    def __init__(self,data,vocab_path):
        self.data_path=data
        # self.data_path="/home/synerzip/Sasidhar/Learning/Tensorflow/textsum/trainer/data"
        self.vocab_output= vocab_path

    def create_vocab_file(self):
        filenames = tf.train.match_filenames_once(self.data_path +"/*.json")
        count_num_files = tf.size(filenames)
        filename_queue = tf.train.string_input_producer(filenames)
        reader = tf.WholeFileReader()
        filename, _ = reader.read(filename_queue)

        with tf.Session() as sess:
            sess.run([tf.global_variables_initializer(), tf.local_variables_initializer()])
            num_files = sess.run(count_num_files)

            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(coord=coord)
            counter = collections.Counter()
            for i in range(num_files):
                csv_file = sess.run(filename)

                filename_queue_sub = tf.train.string_input_producer([csv_file])
                reader_sub = tf.WholeFileReader()
                _, file_contents_sub = reader_sub.read(filename_queue_sub)

                threads_sub = tf.train.start_queue_runners(coord=coord)
                json_content = sess.run(file_contents_sub)
                json_text = json.loads(json.dumps(ast.literal_eval(json_content)))
                article = str(json_text['article'].encode('ascii','ignore'))
                summary = str(json_text["summary"].encode('ascii','ignore'))
                words = article.split()  + summary.split()
                counter.update(words)

            max_words =200000
            with open(self.vocab_output, 'w') as writer:
                for word, count in counter.most_common(max_words - 2):
                    writer.write(word.replace('"','') + ' ' + str(count) + '\n')
                writer.write('<s> 0\n')
                writer.write('</s> 0\n')
                writer.write('<UNK> 0\n')
                writer.write('<PAD> 0\n')

            #coord.request_stop()
            #coord.join(threads)
            #coord.join(threads_sub)

vocab = Vocab("gs://text-summarization-webapp.appspot.com/data/data","data/vocab")
vocab.create_vocab_file()



