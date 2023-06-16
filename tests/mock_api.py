"""Mock API."""

import json

import requests_mock

from tap_egencia.schemas.reporting import (
    linksObject,
    metadataObject
)

from singer_sdk.typing import (
    PropertiesList,
    Property,
)

schema = PropertiesList(
        Property("links", linksObject),
        Property("metadata", metadataObject),
        ).to_dict()


API_URL = "https://apis.egencia.com"

mock_responses_path = "tests/mock_responses"

mock_auth_config = {
    "authorization_token": {
        "type": "stream",
        "endpoint": "/auth/v1/token",
        "file": "mock_auth.json",
    }
}

mock_transactions_config = {
    "transactions_api": {
        "type": "stream",
        "endpoint": "/bi/api/v1/transactions",
        "file": "transactions.json",
    }
}

mock_config = {
    "authorization_token": {
        "type": "auth",
        "endpoint": "/auth/v1/token",
        "file": "mock_auth.json",
    },
    "transactions-api": {
        "type": "stream",
        "endpoint": "/bi/api/v1/transactions",
        "file": "mock_transactions.json",
    }
}

def mock_api(func):
    """Mock API."""

    def wrapper():
        with requests_mock.Mocker() as m:
            for k, v in mock_config.items():

                if v["type"] == "stream":
                    path = f"{mock_responses_path}/{v['file']}"
                    endpoint = v["endpoint"]

                    url = f"{API_URL}{endpoint}"

                    with open(path, "r") as f:
                        response = json.load(f)
                        print(response)
                        print(type(response))
                        decodedresponse = response.decode()
                        print(decodedresponse)
                        print(type(decodedresponse))
                    # response = schema

                    m.post(url, json=decodedresponse)

                elif v["type"] == "auth":
                    path = f"{mock_responses_path}/{v['file']}"
                    url = v["endpoint"]

                    with open(path, "r") as f:
                        response = json.load(f)

                    m.post(url, json=response)

            func()

    wrapper()


def mock_auth_api(func, SAMPLE_CONFIG):
    """Mock API."""

    def wrapper():
        with requests_mock.Mocker() as m:
            for k, v in mock_auth_config.items():
                path = f"{mock_responses_path}/{v['file']}"

                if v["type"] == "stream":
                    endpoint = v["endpoint"]
                    for k, v in SAMPLE_CONFIG.items():
                        var = f"{{{k}}}"
                        if var in endpoint:
                            endpoint = endpoint.replace(var, v)

                    url = f"{API_URL}{endpoint}"

                    with open(path, "r") as f:
                        response = json.load(f)

                    m.get(url, json=response)

            func()

    wrapper()


def mock_transactions_api(func):
    """Mock API."""
    mock_config = mock_transactions_config

    def wrapper():
        with requests_mock.Mocker() as m:
            for k, v in mock_config.items():
                path = f"tap_egencia/schemas/{v['file']}"

                if v["type"] == "stream":
                    endpoint = v["endpoint"]
                    for k, v in SAMPLE_CONFIG.items():
                        var = f"{{{k}}}"
                        if var in endpoint:
                            endpoint = endpoint.replace(var, v)

                    url = f"{API_URL}{endpoint}"

                    with open(path, "r") as f:
                        response = json.load(f)

                    m.post(url, json=response)

            func()

    wrapper()
