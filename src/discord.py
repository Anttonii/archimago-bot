from discord import DMChannel, GroupChannel


def check_channel(ctx) -> bool:
    """
    Checks if the channel is a private channel or group channel

    Used so that blocking requests are only made from servers
    """
    if isinstance(ctx, DMChannel) or isinstance(ctx, GroupChannel):
        return False

    return True


def code_blockify(message: str) -> str:
    """
    Turns a string into a code block for discord
    """
    return "```" + message + "```"


def boldify(message: str) -> str:
    """
    Bolds a string for discord
    """
    return "**" + message + "**"


def message_truncate(message: str, preserve: int) -> str:
    """
    Utility function that truncates message into dicords max character limit of 2000.
    """
    # Removes all lettes after 2000 and replaces last 3 with dots
    # preserve value can be set so that we preserve more space, for example when using code_blockify.
    if len(message) > 2000:
        message = message[0 : 1997 - preserve]
        message += "..."

    return message
