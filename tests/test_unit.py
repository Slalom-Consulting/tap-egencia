# """Tests the tap using a mock base credentials config."""

# import unittest

# import responses
# import singer

# import tap_auth0.tests.utils as test_utils
# from tap_egencia.tap import TapAuth0


# class TestTapAuth0Sync(unittest.TestCase):
#     """Test class for tap-auth0 using base credentials"""

#     def setUp(self):
#         self.mock_config = {
#             "client_id": "1234",
#             "client_secret": "1234",
#             "domain": "test.auth0.com",
#         }
#         responses.reset()
#         del test_utils.SINGER_MESSAGES[:]

#         singer.write_message = test_utils.accumulate_singer_messages

#     def test_base_credentials_discovery(self):
#         """Test basic discover sync"""

#         catalog = TapAuth0(self.mock_config).discover_streams()

#         # expect valid catalog to be discovered
#         self.assertEqual(len(catalog), 3, "Total streams from default catalog")
