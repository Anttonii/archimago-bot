from . import BaseCommand

import src.util as util
import src.curiosa as curiosa


class OverlapCommand(BaseCommand):
    """
    Get overlapping cards between decks having provided at least 2 deck IDs.
    """

    def __init__(self, command: list[str], browser):
        self.browser = browser

        super().__init__(command)

    def get_content(self, msg, parameters) -> str:
        """
        Usage:

        !overlap <id#1> <id#2> returns the overlapping cards between two deck IDs.
        """
        ctx = msg.channel

        if not util.check_channel(ctx):
            return "Overlap command can currently only be used on servers, not in private messages."

        # Avoid blocking the whole app by providing a giant list of ids.
        if len(parameters) > 3:
            parameters = parameters[0:3]

        received_output = curiosa.get_overlapping_cards(parameters, self.browser)

        return util.code_blockify(received_output)
