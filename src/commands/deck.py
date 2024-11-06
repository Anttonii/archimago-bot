from . import BaseCommand

import src.util as util
import src.curiosa as curiosa


class DeckCommand(BaseCommand):
    def __init__(self, command: list[str], browser):
        self.browser = browser

        super().__init__(command)

    def get_content(self, msg, parameters) -> str:
        """
        Gets cards belonging to a deck from a curiosa.io URL or ID.
        """
        ctx = msg.channel

        if not util.check_channel(ctx):
            return "Deck command can currently only be used on servers, not in private messages."

        if len(parameters) > 1:
            return "Incorrect usage, use only 1 deck parameter at a time."

        split_request = parameters[0].split("/")

        if len(split_request) > 1:
            received_output = curiosa.get_deck_from_url(
                parameters[0], False, self.browser
            )
        else:
            received_output = curiosa.get_deck_from_id(
                parameters[0], False, self.browser
            )

        return util.code_blockify(received_output)
