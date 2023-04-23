"""
Testing `Almop` core library functions.
"""

import unittest
from almop import core as alc


class TestAlmopCore(unittest.TestCase):
    """
    Tests data pulling functionality of `Almop` library functions.
    """

    def test_add_one(self):
        """Simple test function"""
        self.assertEqual(alc.add_one(4), 5)


if __name__ == "__main__":
    unittest.main()
