"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import get_standard_tap_tests#, get_tap_test_class

from tap_egencia.tap import TapEgencia

from requests_mock.exceptions import NoMockAddress

from tests.mock_api import mock_auth_api, mock_transactions_api

SAMPLE_CONFIG = {
    # yyyy-MM-dd HH:mm:ss
    # "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%m/%d/%Y, %H:%M:%S"),
    # "end_date": datetime.datetime.now(datetime.timezone.utc).strftime("%m/%d/%Y, %H:%M:%S"),
    "start_date": "2023-01-01 09:00:00",
    "end_date": "2023-06-06 09:00:00",
    "egencia_base_url": "https://apis.egencia.com",
    "domain": "https://apis.egencia.com",
    "client_id": "someclientid",
    "client_secret": "someclientsecret",
    "oauth_request_body": {
        "grant_type": "client_credentials",
        "client_id": "someclientid",
        "client_secret": "someclientsecret",
    }
}

def test_transactions_tap_tests():
    """Run standard tap tests from the SDK."""
    config = SAMPLE_CONFIG
    tests = get_standard_tap_tests(TapEgencia, config=config)
    for test in tests:
        if test.__name__ in ("_test_stream_connections"):
            mock_transactions_api(test, config)
            continue
        # if test.__name__ in ("_test_stream_connections"):
        #     mock_api(test)
        #     continue
            # try:
                # mock_auth_api(test)
            #     mock_transactions_api(test)
            # except requests_mock.exceptions.NoMockAddress:
            #     if requests_mock.exceptions.NoMockAddress == "POST https://apis.egencia.com/auth/v1/token":
            #         continue
            # except Exception:
            #     assert False
            # mock_transactions_api(test)
            # continue

        test()


def test_auth_tap_tests():
    """Run standard tap tests from the SDK."""
    config = SAMPLE_CONFIG
    tests = get_standard_tap_tests(TapEgencia, config=config)
    for test in tests:
        if test.__name__ in ("_test_stream_connections"):
            mock_auth_api(test, config)
            continue

        test()
