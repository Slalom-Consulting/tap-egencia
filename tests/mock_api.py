"""Mock API."""

import json
import re

import requests_mock

API_URL = "https://apis.egencia.com"

mock_responses_path = "tests/mock_responses"

# Endpoints are patterns rather than fixed paths: report creation is per line of
# business (/bi/api/v1/transactions/<lob>) and report pages are keyed by the id
# the creation call hands back. Report creation answers 201, not 200.
mock_config = {
    "authorization_token": {
        "type": "post",
        "endpoint": re.compile(r"/auth/v1/token$"),
        "file": "mock_auth.json",
        "status": 200,
    },
    "transactions": {
        "type": "post",
        "endpoint": re.compile(r"/bi/api/v1/transactions/(air|car|fees|ground|hotel|train)$"),
        "file": "mock_transactions.json",
        "status": 201,
    },
    "transactions-page-1": {
        "type": "get",
        # `/+` because path already ends in a slash and get_url appends another,
        # so the fetch URL carries a double slash. The API tolerates it.
        "endpoint": re.compile(r"/bi/api/v1/transactions/+f5d4d0f8-7243-4c2d-b2ab-bce09fbf4053"),
        "file": "mock_transactions_page1.json",
        "status": 200,
    },
}


def mock_api(func):
    """Mock API."""

    def wrapper():
        with requests_mock.Mocker() as m:
            for k, v in mock_config.items():
                path = f"{mock_responses_path}/{v['file']}"

                with open(path, "r") as f:
                    response = json.load(f)

                m.request(v["type"], v["endpoint"], json=response, status_code=v["status"])

            func()

    wrapper()
