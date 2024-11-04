import src.curiosa as curiosa

import unittest
from unittest.mock import patch


class TestCuriosa(unittest.TestCase):
    def setUp(self):
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
        gen_abundance_url = curiosa.generate_image_url("abundance", None, None)

        self.assertEqual(abundance_url, gen_abundance_url)
