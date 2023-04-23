"""
Testing `Almop` core library functions.
"""

import unittest
from almop import core as alc


class TestAlmopCore(unittest.TestCase):
    """
    Tests data pulling functionality of `Almop` library functions.
    """

    def test_parse_config(self):
        """Simple function checking if config parsing works"""
        self.assertRaises(FileNotFoundError, alc.parse_config, "nonexistent")


if __name__ == "__main__":
    unittest.main()
