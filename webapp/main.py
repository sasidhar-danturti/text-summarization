"""
Entry point for application.
"""

import logging, datetime, base64, json, time, webapp2
from os.path import join, dirname
from textwrap import dedent
from google.appengine.api import users
from google.appengine.api.logservice import logservice
from google.appengine.ext.webapp import template
import constants.constants as con
# from prediction import Prediction
from process.process_data import ProcessData
from utility.file_utils import FileUtils
import constants.constants as con


user_categories = {
    con.ADMIN: [
        "sasidhar.danturti@gmail.com",
        "shubham.yedage52@gmail.com",
        "mukund@synerzip.com"
    ],
    con.VIEWER: []
}
user_email = ""

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

def get_user_role(email):
    logging.info("In get_user_role()...")
    is_admin = False
    if email in user_categories.get(con.ADMIN):
        is_admin = True
    return is_admin

def check_user_access(email):
    logging.info("In check_user_access()")
    has_access = False
    if "synerzip" in email or email in user_categories.get(con.ADMIN):
        has_access = True
    return has_access

def authorise_user(uri):
    logging.info("In authorise_user()...")
    user = users.get_current_user()
    url = None
    if not user:
        url = users.create_login_url(uri)
        logging.info("Redirect URL {}".format(url))
    return url


class HomePage(webapp2.RequestHandler):
    def get(self):
        logging.info("In Class HomePage")
        # Validate request
        log_in_url = authorise_user(self.request.uri)
        if log_in_url:
            logging.info("Redirecting")
            self.redirect(log_in_url)
            logging.info("Logged In")

        email = ""
        has_access = False
        user = users.get_current_user()
        logout_url = ""
        if user:
            email = user.email()
            logging.info("Email: {}".format(email))
            logging.info("User: {}".format(user.nickname()))
            has_access = check_user_access(email=email)
            logout_url = users.create_logout_url('/')

        if has_access:
            data = {
                "log_out_url": logout_url
            }
            is_admin = get_user_role(email=email)
            # If user is admin in redirect to "homepage.html"
            # else "viewer.html"
            if is_admin:
                path = join(dirname(__file__), "homepage.html")
            else:
                path = join(dirname(__file__), "viewer.html")

            self.response.out.write(template.render(path, data))
        else:
            log_out_tag = "<a href='{}'>Click here</a>".format(logout_url)
            self.response.write(
                "<html>"
                "<body>"
                "Access Denied! {} to log in with a different account."
                "</body>"
                "</html>".format(log_out_tag))

class FileList(webapp2.RequestHandler):
    def get(self):
        files = FileUtils().get_files_list()
        self.response.headers["content-type"] = "application/json"
        response_data = {'fileList': files}
        json_res = json.dumps(response_data)
        logging.info("{}".format(json_res))
        self.response.out.write(json_res)

class SaveArticle(webapp2.RequestHandler):
    def post(self):
        logging.info("---------------------------")
        # # Validate request
        # redirect_url = authorise_user(self.request.uri)
        # if redirect_url:
        #     logging.info("Redirecting")
        #     self.redirect(redirect_url)

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
        operation_type = json_data.get(con.OPERATION_TYPE)
        data = json_data.get(con.DATA)
        logging.info("Operation type: {}".format(operation_type))
        logging.info("Request data: {}".format(data))
        if operation_type and operation_type == con.SAVE:
            response = {
                "responseType": "Failed to save file!"
            }
            # Save response on bucket in file
            file_name = ""
            file_name = FileUtils().create_file(request_data=data)
            if file_name:
                response = {
                    "file_name": file_name,
                    "responseType": "Success"
                }
            else:
                response = {
                    "responseType": "Failed to save file!"
                }
        # elif operation_type == con.TRAIN:
        #     # Initiate training
        #     # Process Data
        #     try:
        #         ProcessData().train_data()
        #         response = {
        #             "message": "Training task updated.",
        #             "responseType": "Success"
        #         }
        #     except Exception as ex:
        #         logging.debug(ex.message)
        #         pass

        logging.info("---------------------------")
        self.response.headers["content-Type"] = "application/json"
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
    ('/', HomePage),
    ('/process-article', SaveArticle),
    ('/logs', LogInfoPage),
    ("/files", FileList)
])
