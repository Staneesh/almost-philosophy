"""
Testing `Almop` library functions for pulling data.
"""

import unittest
from almop import data as ald


class TestAlmopData(unittest.TestCase):
    """
    Tests data pulling functionality of `Almop` library functions.
    """

    def test_get_hpi(self):
        """
        Tests if data from eurostat for HPI index change
        is retrieved and filtered OK.
        """
        self.assertEqual(
            len(
                ald.get_hpi(
                    {"dataset_persist_dir": "whatever"}, ["PL", "DE"], no_persist=True
                ).columns
            ),
            2,
        )


if __name__ == "__main__":
    unittest.main()
