from src.commands.base import BaseCommand

from src.trie import Trie
import src.util as util
import src.curiosa as curiosa


class FaqCommand(BaseCommand):
    """
    Gets FAQ entries from curiosa.io for given card name.
    """

    def __init__(self, command: list[str], pt: Trie, cards: dict):
        self.pt = pt
        self.cards = cards

        super().__init__(command)

    def get_content(self, msg, parameters) -> str:
        """
        Usage:

        !faq <card_name> returns the FAQ entries found for the given card.
        !faqs <card_name> same as above.
        """
        card_name = util.get_url_form(" ".join(parameters))

        faq_entries = curiosa.get_faq_entries(card_name, self.pt, self.cards)

        # preserve 6 space for code block
        truncated = util.message_truncate(faq_entries, 6)

        return util.code_blockify(truncated)
