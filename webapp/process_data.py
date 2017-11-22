import logging, json
import requests
from threading import Thread
from file_utils import FileUtils


# sending post request
def initiate_training():
    # Job name
    job_name = FileUtils().get_string()

    # API endpoint to initiate training.
    API_ENDPOINT = "http://35.196.66.17:8080/summarize"

    # data to be sent to api
    data = json.dumps({"input": job_name})
    return requests.post(url = API_ENDPOINT, data = data)


class ProcessData:
    def process_data(self):
        logging.debug("In process_data()...")
        Thread(target=initiate_training).start()
        logging.debug("Initiated training!")

if name == "__main__":
    ProcessData().process_data("")