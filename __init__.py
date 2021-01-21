import os
import json
import logging

import requests
from warrant import Cognito
from dotenv import load_dotenv

load_dotenv()


class Auth:
    def __init__(self):
        self.USER_POOL_ID = os.environ["USER_POOL_ID"]
        self.CLIENT_ID = os.environ["CLIENT_ID"]

    def login(self, username, password):
        client = Cognito(self.USER_POOL_ID, self.CLIENT_ID, username=username)
        client.authenticate(password)
        return client


class Loader:
    def __init__(self, ticker, datatype, username, password):
        base_url = os.environ["API_BASE_URL"]
        url = f"{base_url}/{datatype}/{ticker}"
        self.url = url

        cognitoClient = Auth().login(username, password)
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
