# """Tests the tap using a mock base credentials config."""

import unittest

from tap_egencia.tap import TapEgencia


class TestTapEgenciaSync(unittest.TestCase):
    """Test class for TapEgencia"""

    def test_base_credentials_discovery(self):
        """Test basic discover sync"""

        catalog = TapEgencia().discover_streams()

        # expect valid catalog to be discovered
        self.assertEqual(len(catalog), 1, "Total streams from default catalog")
