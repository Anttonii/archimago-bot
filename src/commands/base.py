class BaseCommand(object):
    """
    The base class for commands.
    """

    def __init__(self, command: list[str]):
        """
        Initialize a new command.

        Command string here refers to the name of the command or the string after the command prefix.
        """
        self.command = command

    def get_content(self, msg, parameters) -> str:
        """
        Returns the content from a resolving command.

        If this function is not overridden, throw an exception.
        """
        raise Exception("get_content function should be overridden by a subclass.")

    def get_command_suffix(self) -> list[str]:
        """
        Returns the command suffix or the string after the command prefix character.
        """
        return self.command

    def is_command_suffix(self, suffix: str) -> bool:
        """
        Checks if given suffix is recognized as this commands suffix.
        """
        return suffix in self.command
