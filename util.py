import json


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
