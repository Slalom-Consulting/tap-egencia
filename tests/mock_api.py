"""Mock API."""

import json

import requests_mock

API_URL = "https://api.mysample.com"

mock_responses_path = "tap_egencia/tests/mock_responses"

mock_config = {
    "authorization_token": {
        "type": "stream",
        "endpoint": "/auth/v1/token",
        "file": "auth.json",
    }
}


def mock_auth_api(func, SAMPLE_CONFIG):
    """Mock API."""

    def wrapper():
        with requests_mock.Mocker() as m:
            for k, v in mock_config.items():
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


mock_transactions_config = {
    "organization_members": {
        "type": "stream",
        "endpoint": "/bi/api/v1/transactions",
        "file": "transactions.json",
    }
}


def mock_transactions_api(func, SAMPLE_CONFIG):
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

                    m.get(url, json=response)

            func()

    wrapper()
