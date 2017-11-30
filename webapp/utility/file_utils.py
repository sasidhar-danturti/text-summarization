"""
This module creates and saves files.
"""
import json, logging
import cloudstorage as gcs
from random import choice
from string import ascii_letters


gcs.set_default_retry_params(
    gcs.RetryParams(
            initial_delay=0.2, max_delay=5.0, backoff_factor=2,
            max_retry_period=15
        ))

class FileUtils:
    def __init__(self):
        self.bucket_name = "text-summarization-webapp.appspot.com"

        self.bucket = '/' + self.bucket_name

    def get_string(self):
        return ''.join(choice(ascii_letters) for _ in range(16))

    # Creates file and stores on Google Cloud Storage.
    def create_file(self, data):
        file_name = self.get_string()
        file_name = self.bucket + '/data/data/{}.json'.format(file_name)
        # The retry_params specified in the open call will override the default
        # retry params for this particular file handle.
        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        with gcs.open(
                file_name, 'w', content_type="application/json",
                options={"x-goog-meta-foo": "foo", "x-goog-meta-bar": "bar"},
                retry_params=write_retry_params) as cloudstorage_file:
            data = json.dumps(data)
            cloudstorage_file.write(data)
        return file_name


    # Reads file data by name.
    def read_file(self, file_name):
        logging.debug("read_file()")
        file_name = '/' + self.bucket_name +  '/' + file_name
        logging.debug("filename: {}".format(file_name))
        with gcs.open(file_name) as cloudstorage_file:
            text = cloudstorage_file.read()
            logging.debug("text: {}".format(text))
        json_text = json.loads(text)
        return json_text
