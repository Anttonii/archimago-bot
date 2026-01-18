import json

import pytest

import src.curiosa as curiosa
from src.trie import Trie

TEST_CARDS_PATH = "test/resources/cards.json"


@pytest.fixture(scope="module")
def get_cards():
    """Loads test cards from json file"""

    with open(TEST_CARDS_PATH, "r", encoding="utf-8") as f:
        cards = json.load(f)

    return cards


def test_generate_image_url(get_cards):
    """Test that generate image url provides correct img urls"""
    apprentice_wizard_url = "https://curiosa.io/_next/image?url=https://d27a44hjr9gen3.cloudfront.net/alp/apprentice_wizard_b_s.png&w=384&q=75"
    gen_apprentice_wizard_url = curiosa.generate_image_url(
        "apprentice wizard", Trie(), get_cards
    )

    assert apprentice_wizard_url == gen_apprentice_wizard_url
