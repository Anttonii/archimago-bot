from src.commands.base import BaseCommand

from src.discord import check_channel, code_blockify
import src.curiosa as curiosa


class DeckCommand(BaseCommand):
    """
    Gets cards belonging to a deck from a curiosa.io URL or ID.
    """

    def __init__(self, command: list[str], browser):
        self.browser = browser

        super().__init__(command)

    def get_content(self, msg, parameters) -> str:
        """
        Usage:

        !deck <id> returns the deck of cards from given curiosa.io deck ID.
        !deck <url> returns the deck of cards from given curiosa.io deck URL.
        """
        ctx = msg.channel

        if not check_channel(ctx):
            return "Deck command can currently only be used on servers, not in private messages."

        if len(parameters) > 1:
            return "Incorrect usage, use only 1 deck parameter at a time."

        if len(parameters) < 1:
            return "Requires a curiosa.io deck ID or URL to function."

        split_request = parameters[0].split("/")

        if len(split_request) > 1:
            received_output = curiosa.get_deck_from_url(
                parameters[0], self.browser, False
            )
        else:
            received_output = curiosa.get_deck_from_id(
                parameters[0], self.browser, False
            )

        return code_blockify(received_output)
