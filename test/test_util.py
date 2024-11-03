import src.util as util

import unittest
from unittest.mock import patch


class TestUtil(unittest.TestCase):
    def setUp(self):
        # Use abundance as a test card for util functionalities
        self.test_card = {
            "name": "abundance",
            "sets": [
                {"name": "alpha"},
                {"name": "beta"}
            ],
            "guardian": {
                "thresholds": {
                    "air": 0,
                    "earth": 0,
                    "fire": 0,
                    "water": 2,
                }
            }
        }
        return super().setUp()

    @patch('src.util.get_card_entry')
    def test_generate_image_url(self, get_card_mock):
        """Test that generate image url provides correct img urls"""
        # Mock get card entry
        get_card_mock.return_value = self.test_card

        abundance_url = "https://curiosa.io/_next/image?url=https://d27a44hjr9gen3.cloudfront.net/alp/abundance_b_s.png&w=384&q=75"
        gen_abundance_url = util.generate_image_url("abundance")

        self.assertEqual(abundance_url, gen_abundance_url)

    def test_parse_sets(self):
        """Test that checks that parse sets correctly parses card sets"""
        sets = util.parse_sets(self.test_card)

        self.assertIn("alpha", sets)
        self.assertIn("beta", sets)
        self.assertEqual(len(sets), 11)  # "alpha, beta"

    def test_parse_threshold(self):
        """Test that checks that parse thresholds correctly parses card thresholds"""
        thresholds = util.parse_threshold(self.test_card['guardian'])

        self.assertEqual(thresholds, "(W)(W)")

    def test_get_card_name_url_form(self):
        """Test that makes sure URL form is correctly formulated for all special cases"""
        test_card_1 = "Wills-o\'-the-Wisp"
        test_card_2 = "Merlin's Staff"
        test_card_3 = "Fire Harpoons!"

        self.assertEqual(util.get_card_name_url_form(
            test_card_1), "wills_o_the_wisp")
        self.assertEqual(util.get_card_name_url_form(
            test_card_2), "merlins_staff")
        self.assertEqual(util.get_card_name_url_form(
            test_card_3), "fire_harpoons")


if __name__ == "__main__":
    unittest.main()
