import os
import logging
import json
from os.path import join, dirname
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery


class Prediction:
    @staticmethod
    def get_abstract_data(json_data):
        # Test through local test.json file
        # with open('test.json') as data_file:
        #     json_data = json.load(data_file)

        PROJECT_ID = "sasidhar-project1"
        response = Prediction._predict_json(project=PROJECT_ID,
                                model='census',
                                instances=[json_data],
                                version='v1')
        return response

    @staticmethod
    def _predict_json(project, model, instances, version=None):
        # Create the ML Engine service object.
        # To authenticate set the environment variable
        # GOOGLE_APPLICATION_CREDENTIALS=<path_to_service_account_file>
        path = join(
            dirname(__file__),
            "Sasidhar-Project1-015d5a46e21e.json"
        )
        os.system(
            'export GOOGLE_APPLICATION_CREDENTIALS="{}"'.format(path))
        logging.debug(os.system("echo $GOOGLE_APPLICATION_CREDENTIALS"))
        credentials = GoogleCredentials.get_application_default()
        service = discovery.build('ml', 'v1', credentials=credentials)
        name = 'projects/{}/models/{}'.format(project, model)

        if version is not None:
            name += '/versions/{}'.format(version)
        print(name)
        response = service.projects().predict(
            name=name,
            body={'instances': instances}
        ).execute()

        if 'error' in response:
            raise RuntimeError(response['error'])

        return response['predictions']


if __name__ == "__main__":
    Prediction().get_abstract_data("")