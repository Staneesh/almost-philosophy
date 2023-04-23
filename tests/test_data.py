"""
Testing `Almop` library functions for pulling data.
"""

import unittest
from almop import data as ald


class TestAlmopData(unittest.TestCase):
    """
    Tests data pulling functionality of `Almop` library functions.
    """

    # def test_add_one(self):
    #     """Simple test function"""
    #     self.assertEqual(almop.add_one(4), 5)

    def test_get_hpi(self):
        """
        Tests if data from eurostat for HPI index change
        is retrieved and filtered OK.
        """
        self.assertGreater(len(ald.get_hpi(["PL", "DE"]).columns), 35)


if __name__ == "__main__":
    unittest.main()
