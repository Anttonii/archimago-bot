from . import BaseCommand

from src.trie import Trie
import src.util as util
import src.curiosa as curiosa


class CimgCommand(BaseCommand):
    def __init__(self, command: list[str], pt: Trie, cards: dict):
        self.pt = pt
        self.cards = cards

        super().__init__(command)

    def get_content(self, msg, parameters) -> str:
        """
        Gets card image in URL form
        """
        image_url = curiosa.generate_image_url(
            " ".join(parameters), self.pt, self.cards
        )

        if not image_url.startswith("https://"):
            image_url = util.code_blockify(image_url)

        return image_url
