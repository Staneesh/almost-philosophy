"""
Testing core `Almop` library functions
"""

import unittest
from almop import almop


class TestCoreAlmop(unittest.TestCase):
    """
    Tests core functionality of `Almop` library functions.
    """

    def test_add_one(self):
        """Simple test function"""
        self.assertEqual(almop.add_one(4), 5)

    def test_get_hpi(self):
        """
        Tests if data from eurostat for HPI index change
        is retrieved and filtered OK.
        """
        self.assertEqual(len(almop.get_hpi(["PL", "DE"]).columns), 2)


if __name__ == "__main__":
    unittest.main()
