from util import *

import os
import sys
import re

from dotenv import load_dotenv

import discord
from discord import CustomActivity, DMChannel, GroupChannel

from curiosa import *

# Load the .env file at project root
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('discord-bot-token')
DISCORD_BOT_MODE = os.getenv('discord-bot-mode')

# Setup discord.py
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)

# Maximum length of a message
MAX_CONTENT_LEN = 1000

# Load card data from json, exit on failure
cards = load_cards()
if cards == None:
    print("Exiting due to failure to load card data.")
    browser.quit()
    sys.exit()


def get_card_image_url(card_name) -> str:
    # Concatenate the name so that we allow spaces in card names
    if len(card_name) > 1:
        concat_name = " ".join(card_name)
    else:
        concat_name = card_name[0]

    return generate_image_url(concat_name)


def check_channel(ctx):
    """
    Checks if the channel is a private channel or group channel

    Used so that blocking requests are only made from servers
    """
    if isinstance(ctx, DMChannel) or isinstance(ctx, GroupChannel):
        return False

    return True


async def match_command(ctx, command):
    """
    Matches commands that start with command prefix to their respective functionality.
    """
    split_command = command.split(" ")

    command = split_command[0][1:len(split_command[0])]
    parameters = split_command[1:len(split_command)]

    match command:
        case 'deck':
            await get_deck(ctx, parameters)
        case 'overlap':
            await get_overlap(ctx, parameters)
        case 'card':
            await get_card(ctx, parameters)
        case 'cimg':
            await get_card_image(ctx, parameters)
        case _:
            print(f"Failed to interpret command: {command}")


async def get_deck(ctx, req):
    """
    Gets cards belonging to a deck from a curiosa.io URL or ID.
    """
    if not check_channel(ctx):
        await ctx.send("Deck command can currently only be used on servers, not in private messages.")
        return

    if len(req) > 1:
        await ctx.send("Incorrect command, use only 1 deck parameters at a time.")

    split_request = req[0].split("/")

    if len(split_request) > 1:
        received_output = get_deck_from_url(browser, req[0])
    else:
        received_output = get_deck_from_id(browser, req[0])

    await ctx.send(code_blockify(received_output))


async def get_overlap(ctx, request):
    """
    Get overlapping cards between decks having provided at least 2 deck IDs.
    """
    if not check_channel(ctx):
        await ctx.send("Overlap command can currently only be used on servers, not in private messages.")
        return

    # Avoid blocking the whole app by providing a giant list of ids.
    if len(request) > 3:
        request = request[0:3]

    received_output = get_overlapping_cards(browser, *request)
    await ctx.send(code_blockify(received_output))


async def get_card(ctx, card_name):
    """
    Get card data by providing a card name.
    """
    # Concatenate the name so that we allow spaces in card names
    if len(card_name) > 1:
        concat_name = " ".join(card_name)
    else:
        concat_name = card_name[0]

    # Safe to assume cards is not none here since we exit if it is
    received_output = get_card_from_name(concat_name, cards)
    await ctx.send(code_blockify(received_output))


async def get_card_image(ctx, card_name):
    await ctx.send(get_card_image_url(card_name))


@client.event
async def on_ready():
    print("Archimago now running.")
    await client.change_presence(status=None, activity=CustomActivity("Brewing magic.."))


@client.event
async def on_message(msg):
    content = msg.content
    channel = msg.channel

    # Don't process messages that are longer than max content length.
    if len(content) > MAX_CONTENT_LEN:
        return

    # Regex patterns for commands that are within messages.
    card_image_pattern = r'\[!(.*?)\]'
    ci_pattern_match = re.search(card_image_pattern, content)

    card_text_pattern = r'\[\[!(.*?)\]\]'
    ct_pattern_match = re.search(card_text_pattern, content)

    # We don't want to receive messages sent by the bot
    if msg.author == client.user:
        return

    if "stop" in content and DISCORD_BOT_MODE == 'debug':
        channel.send("Closing bot client..")
        await client.close()
        browser.quit()
        sys.exit()

    if content[0] == "!":
        await match_command(channel, content)
        return

    if ct_pattern_match:
        card_name = ct_pattern_match.group(1).split(" ")
        await get_card(channel, card_name)
        return

    if ci_pattern_match:
        card_name = ci_pattern_match.group(1).split(" ")
        await get_card_image(channel, card_name)
        return


client.run(DISCORD_BOT_TOKEN)
client.close()
browser.quit()
