import pytest

import src.util as util


@pytest.fixture
def test_card():
    """Use abundance as a test card for util functionalities"""
    return {
        "name": "abundance",
        "sets": [{"name": "alpha"}, {"name": "beta"}],
        "guardian": {
            "thresholds": {
                "air": 0,
                "earth": 0,
                "fire": 0,
                "water": 2,
            }
        },
    }


def test_parse_sets(test_card):
    """Test that checks that parse sets correctly parses card sets"""
    sets = util.parse_sets(test_card)

    assert "alpha" in sets
    assert "beta" in sets
    assert len(sets) == 11  # "alpha, beta"


def test_parse_threshold(test_card):
    """Test that checks that parse thresholds correctly parses card thresholds"""
    thresholds = util.parse_threshold(test_card["guardian"])

    assert thresholds == "(W)(W)"


def test_get_card_name_url_form():
    """Test that makes sure URL form is correctly formulated for all special cases"""
    test_card_1 = "Wills-o'-the-Wisp"
    test_card_2 = "Merlin's Staff"
    test_card_3 = "Fire Harpoons!"

    assert util.get_card_name_url_form(test_card_1) == "wills_o_the_wisp"
    assert util.get_card_name_url_form(test_card_2) == "merlins_staff"
    assert util.get_card_name_url_form(test_card_3) == "fire_harpoons"
