from src.commands.base import BaseCommand

import src.util as util
import src.curiosa as curiosa
from src.trie import Trie


class TermCommand(BaseCommand):
    """
    Get information about term.
    """

    def __init__(self, command: list[str], terms: dict):
        self.terms = terms
        self.pt = Trie(list([term for term in self.terms["term"]]))

        super().__init__(command)

    def get_content(self, msg, parameters) -> str:
        """
        Usage:

        !term <term> returns an explanation for the given term.
        """
        term = util.get_url_form(" ".join(parameters))

        is_found = term in self.terms["term"]
        is_alternative = False

        # If the term is not recognized but is an alternative
        if not is_found:
            for k, v in self.terms["term"].items():
                if "alternatives" not in v:
                    continue

                if term in v["alternatives"]:
                    term = k
                    is_alternative = True

        if not is_alternative and not is_found:
            # Invalid term
            return util.code_blockify(
                curiosa.get_content_suggestion(
                    term, self.pt, "No explanation found for term"
                )
            )
        else:
            return util.code_blockify(self.terms["term"][term]["text"])
