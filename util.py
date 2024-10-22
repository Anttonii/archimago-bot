import json
import os


def is_json(value: str) -> bool:
    """
    Checks if string is a valid json.
    """
    try:
        json.loads(value)
    except ValueError as e:
        return False
    return True


def code_blockify(message: str) -> str:
    """
    Turns a string into a code block for discord
    """
    return "```" + message + "```"


def boldify(message: str) -> str:
    """
    Bolds a string for discord
    """
    return "**" + message + "**"


def load_cards(json_path: str = "data/cards.json"):
    """
    Loads cards from cards.json into memory for quick retrieval.
    """
    if not os.path.exists(json_path):
        print("Could not load cards.json, make sure to download it before attempting to retrieve data from it.")
        print("The file can be automatically downloaded with the command: python curiosa.py download")
        return None

    with open(json_path, 'r', encoding="utf-8") as json_file:
        try:
            data = json.load(json_file)
        except json.JSONDecodeError:
            print(f"Failed to load {
                  json_path}, the file at path is an invalid JSON file.")
            return None

    return data


def parse_sets(card):
    """
    Parses sets into a single line
    """
    output = ""
    sets = card['sets']

    for _set in sets:
        output += _set['name'] + ", "

    return output[0:len(output) - 2]


def parse_threshold(guardian):
    """
    Parses thresholds object into a more readable form.

    Example output for a card having 1 air and 1 water threshold is (A)(W)
    """
    output = ""
    thresholds = guardian['thresholds']
    for (k, v) in thresholds.items():
        if v == 0:
            continue

        output += ("(" + k[0].capitalize() + ")") * v
    return output


def get_card_entry(card_name: str, cards: dict = None) -> str:
    """
    Gets the card object from given card dictionary.
    """
    # Load cards if a proper dictionary object is not provided
    if cards == None:
        cards = load_cards()

    for card in cards:
        if card['name'].lower() == card_name.lower():
            return card

    return None


def generate_image_url(card_name: str) -> str:
    """
    Generates an image URL from a given card name.
    """
    base_url = "https://curiosa.io/_next/image?url=https://d27a44hjr9gen3.cloudfront.net/"
    extension = "_b_s.png&w=384&q=75"

    card = get_card_entry(card_name)
    card_name = card['name'].lower()

    # Convert spaces into underscores
    name_split = card_name.split(" ")
    if len(name_split) > 1:
        card_name = "_".join(name_split)

    set = parse_sets(card)

    # Take the first set and the first 3 characters converted to lower case
    set_name = set[0:3].lower()

    return base_url + set_name + "/" + card_name + extension
