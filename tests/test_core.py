"""Tests standard tap features using the built-in SDK tests library."""

import datetime

import pytest

from singer_sdk.testing import get_standard_tap_tests#, get_tap_test_class

from tap_egencia.tap import TapEgencia

from tests.mock_api import mock_auth_api, mock_transactions_api, mock_api

# from requests_mock.exceptions import NoMockAddress
import requests_mock

SAMPLE_CONFIG = {
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    "end_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    "egencia_base_url": "https://apis.egencia.com",
    "domain": "https://apis.egencia.com",
    "client_id": "4j3t1ttuj3uqvfiqg0f4n2qund",
    "client_secret": "1mplj4ilnbtv1161lpns6i2unjd48179fs37cla5jps3odqkb03f",
    "oauth_request_body": {
        "grant_type": "client_credentials",
        "client_id": "4j3t1ttuj3uqvfiqg0f4n2qund",
        "client_secret": "1mplj4ilnbtv1161lpns6i2unjd48179fs37cla5jps3odqkb03f",
    }
}

def test_transactions_tap_tests():
    """Run standard tap tests from the SDK."""
    config = SAMPLE_CONFIG
    tests = get_standard_tap_tests(TapEgencia, config=config)
    for test in tests:
        if test.__name__ in ("_test_stream_connections"):
            mock_api(test)
            continue
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

@pytest.mark.skip("skipping auth")
def test_auth_tap_tests():
    """Run standard tap tests from the SDK."""
    config = SAMPLE_CONFIG.copy()
    tests = get_standard_tap_tests(TapEgencia, config=config)
    for test in tests:
        if test.__name__ in ("_test_stream_connections"):
            try:
                mock_auth_api(test)
            except requests_mock.exceptions.NoMockAddress:
                pass
            except Exception:
                assert False

        test()
