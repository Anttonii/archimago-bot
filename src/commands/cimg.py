from . import BaseCommand

from src.trie import Trie
import src.util as util
import src.curiosa as curiosa


class CimgCommand(BaseCommand):
    """
    Gets card image in URL form.
    """

    def __init__(self, command: list[str], pt: Trie, cards: dict):
        self.pt = pt
        self.cards = cards

        super().__init__(command)

    def get_content(self, msg, parameters) -> str:
        """
        Usage:

        !cimg <card_name> returns the URL for the image of the given card name.
        """
        image_url = curiosa.generate_image_url(
            " ".join(parameters), self.pt, self.cards
        )

        if not image_url.startswith("https://"):
            image_url = util.code_blockify(image_url)

        return image_url
