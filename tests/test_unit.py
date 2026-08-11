"""Tests the tap using a mock base credentials config."""

import datetime
import json
import unittest
from unittest import mock

import requests

from tap_egencia.client import egenciaStream
from tap_egencia.tap import TapEgencia

SAMPLE_CONFIG = {
    # date format needs to be yyyy-MM-dd HH:mm:ss
    "start_date": "2023-01-01 09:00:00",
    "egencia_base_url": "https://apis.egencia.com",
    "client_id": "testclientid",
    "client_secret": "testclientsecret",
}

EXPECTED_STREAMS = {
    "air",
    "car",
    "fee",
    "ground",
    "hotel",
    "reconciled_air",
    "train",
}

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _response(status_code, payload=None):
    """Build a requests.Response the way the API would return one."""
    response = requests.Response()
    response.status_code = status_code
    response.request = requests.Request(
        method="POST", url="https://apis.egencia.com/bi/api/v1/transactions/air"
    ).prepare()
    if payload is not None:
        response._content = json.dumps(payload).encode()
    return response


def _stream(name):
    return next(s for s in TapEgencia(config=SAMPLE_CONFIG).discover_streams() if s.name == name)


class TestTapEgenciaSync(unittest.TestCase):
    """Test class for TapEgencia"""

    def test_base_credentials_discovery(self):
        """Test basic discover sync"""

        catalog = TapEgencia(config=SAMPLE_CONFIG).discover_streams()

        self.assertEqual(
            {stream.name for stream in catalog},
            EXPECTED_STREAMS,
            "Streams discovered from default catalog",
        )


class TestRequestWindow(unittest.TestCase):
    """The report window must stay inside the API's one-year limit."""

    def _window_days(self, stream, context=None):
        start, end = stream.get_window(context)
        return (
            datetime.datetime.strptime(end, DATE_FORMAT)
            - datetime.datetime.strptime(start, DATE_FORMAT)
        ).days

    def test_reconciled_air_uses_rolling_lookback(self):
        """reconciled_air ignores the bookmark: its records lag reconciliation."""
        stream = _stream("reconciled_air")
        self.assertEqual(stream.lookback_days, 364)

        with mock.patch.object(
            stream, "get_starting_timestamp", side_effect=AssertionError("bookmark used")
        ):
            self.assertEqual(self._window_days(stream), 364)

    def test_bookmark_within_limit_is_used_as_is(self):
        """A recent bookmark drives the window for ordinary streams."""
        stream = _stream("air")
        bookmark = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=2)

        with mock.patch.object(stream, "get_starting_timestamp", return_value=bookmark):
            self.assertEqual(self._window_days(stream), 2)

    def test_missing_bookmark_and_start_date_does_not_crash(self):
        """start_date is not a required setting, so the window must survive without it."""
        config = {k: v for k, v in SAMPLE_CONFIG.items() if k != "start_date"}
        stream = next(
            s for s in TapEgencia(config=config).discover_streams() if s.name == "air"
        )

        self.assertIsNone(stream.get_starting_timestamp(None))
        self.assertEqual(self._window_days(stream), stream.max_window_days)

    def test_bookmark_older_than_limit_is_clamped(self):
        """A stale bookmark is clamped rather than sent and rejected with a 400.

        Without this, state loss is unrecoverable: the fallback start_date is
        older than a year, so every subsequent run fails and rewrites the state
        file empty again.
        """
        stream = _stream("air")
        bookmark = datetime.datetime(2025, 2, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)

        with mock.patch.object(stream, "get_starting_timestamp", return_value=bookmark):
            self.assertEqual(self._window_days(stream), stream.max_window_days)


class TestEmptyReportHandling(unittest.TestCase):
    """HTTP 204 means the report holds no rows, which is not an error."""

    def setUp(self):
        patcher = mock.patch.object(
            egenciaStream, "authenticator", new_callable=mock.PropertyMock
        )
        self.addCleanup(patcher.stop)
        patcher.start().return_value = mock.Mock(auth_headers={})

    def test_204_yields_no_records_and_does_not_raise(self):
        stream = _stream("reconciled_air")

        with mock.patch.object(stream, "_request", return_value=_response(204)):
            self.assertEqual(list(stream.get_records(None)), [])

    def test_201_returns_the_report_id(self):
        stream = _stream("reconciled_air")
        payload = {"report_id": "abc-123", "metadata": {"total_pages": 2}}

        with mock.patch.object(stream, "_request", return_value=_response(201, payload)):
            self.assertEqual(stream.get_report_id(None), "abc-123")

    def test_unexpected_status_raises_with_the_response_body(self):
        """The body is where Egencia explains the rejection, so it must surface."""
        stream = _stream("reconciled_air")
        payload = [{"message": "exceeds the maximum allowable date range of one year"}]

        with mock.patch.object(stream, "_request", return_value=_response(202, payload)):
            with self.assertRaises(Exception) as ctx:
                stream.get_report_id(None)

        self.assertIn("maximum allowable date range", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
