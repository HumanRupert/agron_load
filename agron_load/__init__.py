import os
import json
import logging

import requests
from warrant import Cognito
from dotenv import load_dotenv

load_dotenv()


def login():
    USER_POOL_ID = os.environ["USER_POOL_ID"]
    CLIENT_ID = os.environ["CLIENT_ID"]
    COGNITO_PASSWORD = os.environ["COGNITO_PASSWORD"]
    COGNITO_USERNAME = os.environ["COGNITO_USERNAME"]

    client = Cognito(USER_POOL_ID, CLIENT_ID,
                     username=COGNITO_USERNAME)
    client.authenticate(COGNITO_PASSWORD)
    return client


class Loader:
    def __init__(self, ticker, datatype):
        base_url = os.environ["API_BASE_URL"]
        url = f"{base_url}/{datatype}/{ticker}"
        self.url = url

        cognitoClient = login()
        self.idToken = cognitoClient.id_token

    def load(self, data):
        headers = {
            "Authorization": f"Bearer {self.idToken}"
        }

        try:
            response = requests.post(self.url, data=data, headers=headers)

            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            logging.error(str(e) + " ––– " + response.text)
            raise

        return response.json()
