import json, logging, requests
import requests_toolbelt.adapters.appengine
# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()
from threading import Thread
from utility.date_time_utils import DateTimeUtils


# Post request
def initiate_training(job_id):
    logging.debug("In initiate_training()...")
    headers = {
        "Content-Type": "application/json",
    }
    res = requests.post("http://35.196.66.17:8080/summarize",
                        json.dumps({"input": "{}".format(job_id)}))
    logging.debug("Training request response: {}".format(res.text))


# Upload training task.
class ProcessData:
    def process_data(self):
        logging.debug("In process_data()...")
        job_id = "Job_{}".format(DateTimeUtils.time_to_int())
        logging.debug("JobID: {}".format(job_id))
        t = Thread(target=initiate_training, args=(job_id,))
        t.start()


if __name__ == "__main__":
    ProcessData().process_data()