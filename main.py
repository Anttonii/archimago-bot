import os

from dotenv import load_dotenv

import discord
from discord.ext import commands

from curiosa import get_deck_from_id, get_deck_from_url, get_overlapping_cards, browser

# Load the .env file at project root
load_dotenv()

description = '''A bot for parsing curiosa.io decks into discord messages.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

DISCORD_BOT_TOKEN = os.getenv('discord-bot-token')
bot = commands.Bot(command_prefix='$',
                   description=description, intents=intents)


@bot.command(name="deck")
async def get_deck(ctx, request: str):
    split_request = request[0].split("/")

    if len(split_request) > 1:
        received_output = get_deck_from_url(browser, request)
    else:
        received_output = get_deck_from_id(browser, request)

    received_output = "```" + received_output + "```"
    await ctx.send(received_output)


@bot.command(name="overlap")
async def get_overlap(ctx, *request: str):
    # Avoid blocking the whole app by providing a giant list of ids.
    if len(request) > 3:
        request = request[0:3]

    received_output = get_overlapping_cards(browser, *request)
    received_output = "```" + received_output + "```"
    await ctx.send(received_output)

bot.run(DISCORD_BOT_TOKEN)
browser.quit()
