from util import *

import os
import sys

from dotenv import load_dotenv

import discord
from discord.ext import commands

from curiosa import *

# Load the .env file at project root
load_dotenv()

# Discord.py set-up
description = '''A bot for parsing curiosa.io decks and sorcery card info into discord messages.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

DISCORD_BOT_TOKEN = os.getenv('discord-bot-token')
DISCORD_BOT_MODE = os.getenv('discord-bot-mode')
bot = commands.Bot(command_prefix='!',
                   description=description, intents=intents)


# Load card data from json, exit on failure
cards = load_cards()
if cards == None:
    print("Exiting due to failure to load card data.")
    browser.quit()
    sys.exit()


class Curiosa(commands.Cog):
    """
    Curiosa.io related commands
    """
    @commands.command(name="deck")
    async def get_deck(ctx, request: str):
        """
        Gets cards belonging to a deck from a curiosa.io URL or ID.
        """
        split_request = request.split("/")

        if len(split_request) > 1:
            received_output = get_deck_from_url(browser, request)
        else:
            received_output = get_deck_from_id(browser, request)

        await ctx.send(code_blockify(received_output))

    @commands.command(name="overlap")
    async def get_overlap(ctx, *request: str):
        """
        Get overlapping cards between decks having provided at least 2 deck IDs.
        """
        # Avoid blocking the whole app by providing a giant list of ids.
        if len(request) > 3:
            request = request[0:3]

        received_output = get_overlapping_cards(browser, *request)
        await ctx.send(code_blockify(received_output))

    @commands.command(name="card")
    async def get_card(ctx, *card_name: str):
        """
        Get card data by providing a card name.
        """
        # Concatenate the name so that we allow spaces in card names
        concat_name = " ".join(card_name)

        # Safe to assume cards is not none here since we exit if it is
        received_output = get_card_from_name(concat_name, cards)
        await ctx.send(code_blockify(received_output))


if DISCORD_BOT_MODE == 'debug':
    @bot.command(name="stop")
    async def stop(ctx):
        bot.close()
        browser.quit()


@bot.event
async def on_ready():
    await bot.add_cog(Curiosa())

bot.run(DISCORD_BOT_TOKEN)

bot.close()
browser.quit()
