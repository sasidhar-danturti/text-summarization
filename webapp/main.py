"""
Entry point for application.
"""

import logging, webapp2, json, base64, datetime, time
# from itertools import islice
from textwrap import dedent
from file_utils import FileUtils
from os.path import join, dirname
import constants as con
# from prediction import Prediction
import constants as con
from process_data import ProcessData
from google.appengine.ext.webapp import template
from google.appengine.api.logservice import logservice
from google.appengine.api import users

def get_logs(offset=None):
    # Logs are read backwards from the given end time. This specifies to read
    # all logs up until now.
    end_time = time.time()

    logs = logservice.fetch(
        end_time=end_time,
        offset=offset,
        minimum_log_level=logservice.LOG_LEVEL_INFO,
        include_app_logs=True)

    return logs


def format_log_entry(entry):
    # Format any application logs that happened during this request.
    logs = []
    for log in entry.app_logs:
        date = datetime.datetime.fromtimestamp(
            log.time).strftime('%D %T UTC')
        logs.append('Date: {}, Message: {}'.format(
            date, log.message))

    # Format the request log and include the application logs.
    date = datetime.datetime.fromtimestamp(
        entry.end_time).strftime('%D %T UTC')

    output = dedent("""
        Date: {}
        IP: {}
        Method: {}
        Resource: {}
        Logs:
    """.format(date, entry.ip, entry.method, entry.resource))

    output += '\n'.join(logs)
    return output


def authorise_user(uri):
    user = users.get_current_user()
    url = None
    if user:
        logging.debug("User: {}".format(user.nickname()))
    else:
        url = users.create_login_url(uri)
    return url


class DecodeDataPage(webapp2.RequestHandler):
    def get(self):
        logging.debug("In Class DecodeDataPage")
        # Validate request
        redirect_url = authorise_user(self.request.uri)
        if redirect_url:
            logging.debug("Redirecting")
            self.redirect(redirect_url)

        # If user is logged in redirect to "decoding.html"
        path = join(dirname(__file__), "decoding.html")
        logging.debug(path)
        self.response.out.write(template.render(path, None))


class TrainDataPage(webapp2.RequestHandler):
    def get(self):
        logging.debug("In Class TrainDataPage")
        # Validate request
        redirect_url = authorise_user(self.request.uri)
        if redirect_url:
            logging.debug("Redirecting")
            self.redirect(redirect_url)

        # If user is logged in redirect to "training.html"
        path = join(dirname(__file__), "training.html")
        self.response.out.write(template.render(path, None))


class ProcessArticle(webapp2.RequestHandler):
    def post(self):
        logging.info("---------------------------")
        # Validate request
        redirect_url = authorise_user(self.request.uri)
        if redirect_url:
            logging.info("Redirecting")
            self.redirect(redirect_url)

        # Get data.
        data = self.request.body
        logging.info(">>>>> {}".format(data))

        # Initialize response.
        response = {
            "responseType": "failed"
        }

        # Parse data string as json.
        json_data = json.loads(data)
        # Fetch operation type and data
        operation_type = json_data.get(con.OPERATIONTYPE)
        data = json_data.get(con.DATA)
        logging.info("Operation type: {}".format(operation_type))
        logging.info("data is : {}".format(str(data)))
        if operation_type and operation_type == con.SAVE:
            response = {
                "responseType": "Failed to save file!"
            }
            # Save response on bucket in file
            file_name = FileUtils().create_file(data=data)
            if file_name:
                response = {
                    "file_name": file_name,
                    "responseType": "Success"
                }
            else:
                response = {
                    "responseType": "Failed to save file!"
                }
        elif operation_type == con.TRAIN:
            # Initiate training
            # Process Data
            ProcessData().process_data(data=data)
            pass

        else:
            # Initiate decoding
            pass

        logging.info("---------------------------")

        self.response.headers['content-Type'] = 'application/json'
        self.response.out.write(json.dumps(response))

class LogInfoPage(webapp2.RequestHandler):
    def get(self):
        offset = self.request.get('offset', None)

        if offset:
            offset = base64.urlsafe_b64decode(str(offset))

        # Get the logs given the specified offset.
        logs = get_logs(offset=offset)

        # Output the first 10 logs.
        for log in logs:
            self.response.write(
                '<pre>{}</pre>'.format(format_log_entry(log)))

app = webapp2.WSGIApplication([
    ('/decode', DecodeDataPage),
    ('/training', TrainDataPage),
    ('/process-article', ProcessArticle),
    ('/logs', LogInfoPage)
])
