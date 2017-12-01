import json, logging, requests
import requests_toolbelt.adapters.appengine
# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()
from threading import Thread
from utility.date_time_utils import DateTimeUtils


def _initiate_training(job_id):
    logging.debug("In initiate_training()...")
    headers = {
        "Content-Type": "application/json",
    }
    res = _place_request(
        url="https://104.196.169.174:5000/train",
        data={"input": "{}".format(job_id)},
        headers=headers
    )
    logging.debug("Training request response: {}".format(res.text))


def _place_request(url, data, headers):
    logging.debug("In _place_request()...")
    return requests.post(url=url, data=json.dumps(data), headers=headers)


# Upload training task.
class ProcessData:
    def train_data(self):
        logging.debug("In train_data()...")
        job_id = "Job_{}".format(DateTimeUtils.time_to_int())
        logging.debug("JobID: {}".format(job_id))
        # t = Thread(target=_initiate_training, args=(job_id,))
        # t.start()
        try:
            _initiate_training(job_id)
        except Exception as ex:
            logging.debug(ex.message)
            pass
