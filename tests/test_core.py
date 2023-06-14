"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import get_standard_tap_tests#, get_tap_test_class

from tap_egencia.tap import TapEgencia

from requests_mock.exceptions import NoMockAddress

from tests.mock_api import mock_auth_api, mock_transactions_api

SAMPLE_CONFIG = {
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    # "egencia_base_url": "https://api.mysample.com"
}


def test_transactions_tap_tests():
    """Run standard tap tests from the SDK."""
    config = SAMPLE_CONFIG
    tests = get_standard_tap_tests(TapEgencia, config=config)
    for test in tests:
        if test.__name__ in ("_test_stream_connections"):
            mock_transactions_api(test, config)
            continue

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