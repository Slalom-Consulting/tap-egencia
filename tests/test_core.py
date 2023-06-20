"""Tests standard tap features using the built-in SDK tests library."""

from singer_sdk.testing import get_standard_tap_tests

from tap_egencia.tap import TapEgencia

from tests.mock_api import mock_api

SAMPLE_CONFIG = {
    # date format needs to be yyyy-MM-dd HH:mm:ss
    "start_date": "2023-01-01 09:00:00",
    "end_date": "2023-06-06 09:00:00",
    "egencia_base_url": "https://apis.egencia.com",
    "client_id": "testclientid",
    "client_secret": "testclientsecret"
}

def test_transactions_tap_tests():
    """Run standard tap tests from the SDK."""
    config = SAMPLE_CONFIG
    tests = get_standard_tap_tests(TapEgencia, config=config)
    for test in tests:
        if test.__name__ in ("_test_stream_connections"):
            mock_api(test)
            continue
        test()
