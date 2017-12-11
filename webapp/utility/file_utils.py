"""
This module creates and saves files.
"""
import json, logging, re
import cloudstorage as gcs
from random import choice
from string import ascii_letters
import constants.constants as con
from utility.date_time_utils import DateTimeUtils
from config.application_config import ApplicationConfig

APPLICATION_CONFIGURATION = ApplicationConfig.get_config()

gcs.set_default_retry_params(
    gcs.RetryParams(
        initial_delay=0.2, max_delay=5.0, backoff_factor=2,
        max_retry_period=15
    ))


class FileUtils:
    def __init__(self):
        self.bucket_name = '/' + APPLICATION_CONFIGURATION.get(con.BUCKET_NAME)

    def get_string(self):
        return ''.join(choice(ascii_letters) for _ in range(16))

    # Creates file and stores on Google Cloud Storage.
    def create_file(self, request_data):
        data = {
            con.ARTICLE: request_data.get(con.ARTICLE),
            con.SUMMARY: request_data.get(con.SUMMARY)
        }
        file_name = request_data.get(con.FILE_NAME)
        tag_name = request_data.get(con.TAG_NAME, "data")
        logging.debug("File name: {}".format(file_name) )
        file_name = self.bucket_name + "/data/{tag_name}/{file_name}.json".format(
            tag_name=tag_name,
            file_name=file_name
        )
        # The retry_params specified in the open call will override the default
        # retry params for this particular file handle.
        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        with gcs.open(
                file_name, 'w', content_type="application/json",
                options={"x-goog-meta-foo": "foo", "x-goog-meta-bar": "bar"},
                retry_params=write_retry_params) as cloudstorage_file:
            cloudstorage_file.write(json.dumps(data))
        return file_name

    # Reads file data by name.
    def read_file(self, file_name):
        logging.debug("read_file()")
        file_name = self.bucket_name + '/' + file_name
        logging.debug("file name: {}".format(file_name))
        with gcs.open(file_name) as cloudstorage_file:
            text = cloudstorage_file.read()
            logging.debug("text: {}".format(text))
        json_text = json.loads(text)
        return json_text

    # Get files list
    def get_files_list(self):
        logging.debug("In get_files_list()...")
        tags = {}
        for stat in gcs.listbucket(self.bucket_name + '/data', delimiter='/'):
            dir_name = stat.filename
            for sub_dir in gcs.listbucket(dir_name, delimiter='/'):
                sub_dir_name = sub_dir.filename
                if not sub_dir_name == dir_name and sub_dir.is_dir:
                    files = []
                    for sub_dir_child in gcs.listbucket(sub_dir_name):
                        sub_dir_child_name = sub_dir_child.filename
                        if ".json" in sub_dir_child_name:
                            files.append(re.sub(
                                pattern=sub_dir_name,
                                repl='',
                                string=sub_dir_child_name
                            ))
                    dummy_name = sub_dir_name.replace(dir_name, '')
                    tags[dummy_name.replace('/', '')] = files
        return tags


