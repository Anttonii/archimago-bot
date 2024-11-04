import pytest

import src.curiosa as curiosa


@pytest.fixture
def test_card():
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


def test_generate_image_url(mocker, test_card):
    """Test that generate image url provides correct img urls"""
    # Mock get_card_entry
    mocker.patch("src.util.get_card_entry", return_value=test_card)

    abundance_url = "https://curiosa.io/_next/image?url=https://d27a44hjr9gen3.cloudfront.net/alp/abundance_b_s.png&w=384&q=75"
    gen_abundance_url = curiosa.generate_image_url("abundance", None, None)

    assert abundance_url == gen_abundance_url
