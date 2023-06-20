"""Mock API."""

import json

import requests_mock

API_URL = "https://apis.egencia.com"

mock_responses_path = "tests/mock_responses"

mock_config = {
    "authorization_token": {
        "type": "post",
        "endpoint": "/auth/v1/token",
        "file": "mock_auth.json",
    },
    "transactions": {
        "type": "post",
        "endpoint": "/bi/api/v1/transactions",
        "file": "mock_transactions.json",
    },
    "transactions-page-1": {
        "type": "get",
        "endpoint": "/bi/api/v1/transactions/f5d4d0f8-7243-4c2d-b2ab-bce09fbf4053?page=1",
        "file": "mock_transactions_page1.json",
    }
}

def mock_api(func):
    """Mock API."""

    def wrapper():
        with requests_mock.Mocker() as m:
            for k, v in mock_config.items():
                path = f"{mock_responses_path}/{v['file']}"

                endpoint = v["endpoint"]

                url = f"{API_URL}{endpoint}"

                with open(path, "r") as f:
                    response = json.load(f)

                if v["type"] == "post":
                    m.post(url, json=response)

                elif v["type"] == "get":
                    m.get(url, json=response)

            func()

    wrapper()
