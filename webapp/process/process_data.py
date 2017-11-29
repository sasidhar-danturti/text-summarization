import json, logging, requests
import requests_toolbelt.adapters.appengine
# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()
from threading import Thread
from utility.date_time_utils import DateTimeUtils


# Upload training task.
class ProcessData:
    def _place_request(self, url, data):
         return requests.post(url,
                            json.dumps(data))

    # Post request
    def _initiate_training(self, job_id):
        logging.debug("In initiate_training()...")
        headers = {
            "Content-Type": "application/json",
        }
        res = self._place_request(
            url="http://35.196.110.160:5000/train",
            data={"input": "{}".format(job_id)}
        )
        logging.debug("Training request response: {}".format(res.text))

    def train_data(self):
        logging.debug("In train_data()...")
        job_id = "Job_{}".format(DateTimeUtils.time_to_int())
        logging.debug("JobID: {}".format(job_id))
        t = Thread(target=self._initiate_training, args=(job_id,))
        t.start()

    def decode_data(self, article):
        logging.debug("In decode_data()...")
        self._place_request(
            url="http://35.196.110.160:5000/decode",
            data={"input": "{}".format(article)}
        )

