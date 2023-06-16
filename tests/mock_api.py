"""Mock API."""

import json
import io

import requests_mock

API_URL = "https://apis.egencia.com"

mock_responses_path = "tests/mock_responses"

mock_config = {
    "authorization_token": {
        "type": "stream",
        "endpoint": "/auth/v1/token",
        "file": "mock_auth.json",
    }
}


def mock_auth_api(func):
    """Mock API."""

    def wrapper():
        with requests_mock.Mocker() as m:
            for k, v in mock_config.items():
                path = f"{mock_responses_path}/{v['file']}"

                if v["type"] == "stream":
                    endpoint = v["endpoint"]

                    url = f"{API_URL}{endpoint}"

                    with open(path, "r") as f:
                        response = json.load(f)
                        print(response)
                        print(type(response))
                        strresponse = response.decode()
                        print(strresponse)
                        print(type(strresponse))
                        strutf8 = str(response, 'UTF-8')
                        print(strutf8)
                        print(type(strutf8))

                    m.post(url, json=response)

            func()

    wrapper()


mock_transactions_config = {
    "organization_members": {
        "type": "stream",
        "endpoint": "/bi/api/v1/transactions",
        "file": "transactions.json",
    }
}


def mock_transactions_api(func):
    """Mock API."""
    mock_config = mock_transactions_config

    def wrapper():
        with requests_mock.Mocker() as m:
            for k, v in mock_config.items():
                path = f"tap_egencia/schemas/{v['file']}"

                if v["type"] == "stream":
                    endpoint = v["endpoint"]

                    url = f"{API_URL}{endpoint}"

                    with open(path, "r") as f:
                        response = json.load(f)

                    m.post(url, json=response)

            func()

    wrapper()

mock_config2 = {
    "authorization_token": {
        "type": "auth",
        "url": "/auth/v1/token",
        "endpoint": "/auth/v1/token",
        "file": "mock_auth.json",
    },
    "transactions-api": {
        "type": "stream",
        "endpoint": "/bi/api/v1/transactions",
        "file": "transactions.json",
    }
}

def mock_api(func):
    """Mock API."""

    def wrapper():
        with requests_mock.Mocker() as m:
            for k, v in mock_config2.items():

                if v["type"] == "stream":
                    path = f"tap_egencia/schemas/{v['file']}"
                    endpoint = v["endpoint"]

                    url = f"{API_URL}{endpoint}"

                    with open(path, "r") as f:
                        response = json.load(f)
                        print(response)
                        print(type(response))

                    m.post(url, json=response)

                elif v["type"] == "auth":
                    path = f"{mock_responses_path}/{v['file']}"
                    url = v["url"]

                    with open(path, "r") as f:
                        response = json.load(f)

                    m.post(url, json=response)

            func()

    wrapper()
