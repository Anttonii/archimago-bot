from src.commands.base import BaseCommand

from src.discord import boldify, code_blockify

import inspect


class HelpCommand(BaseCommand):
    """
    Returns this message.
    """

    def __init__(self, command: list[str], commands: list[BaseCommand]):
        super().__init__(command)

        self.commands = commands
        self.commands.append(self)

        self.content = self.build_content()

    def get_content(self, msg, parameters) -> str:
        """
        Usage:

        !help returns list of commands and their explanations.
        !help <command> returns usage information about a command.
        """
        if len(parameters) > 0:
            for command in self.commands:
                if command.is_command_suffix(parameters[0]):
                    doc_string = inspect.getdoc(command.get_content)

                    if doc_string is None:
                        return f"No help provided for command: {parameters[0]}."
                    else:
                        return code_blockify(doc_string)

            # Could not find explicit help for the given parameter.
            return f"Invalid command: {parameters[0]}"

        return self.content

    def build_content(self) -> str:
        """
        Builds the help commands content.
        """
        output = "Archimago provides the following commands:\n\n"
        for command in self.commands:
            output += (
                "- " + boldify(", ".join(command.get_command_suffix())) + ": "
            )

            doc_string = inspect.getdoc(command)
            if doc_string is None:
                output += "\n"
            else:
                output += doc_string + "\n"
        return output
