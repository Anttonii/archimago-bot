from . import BaseCommand

CURIOSA_RULEBOOK_URL = (
    "https://drive.google.com/file/d/1sgQo0xf0N2teIR0zlyl91g9j6LVncZnr/view"
)


class RulebookCommand(BaseCommand):
    def __init__(self, command: list[str]):
        super().__init__(command)

    def get_content(self, msg, parameters) -> str:
        """
        Get URL for the official rulebook.
        """
        return CURIOSA_RULEBOOK_URL
