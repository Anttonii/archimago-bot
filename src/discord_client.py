from . import curiosa, util
from .trie import Trie

import os
import sys
import re
from asyncio import run as aiorun

from dotenv import load_dotenv

import discord
from discord import CustomActivity

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('discord-bot-token')
DISCORD_BOT_MODE = os.getenv('discord-bot-mode')

default_intents = discord.Intents.default()
default_intents.members = True
default_intents.message_content = True

# Maximum length of a message
MAX_CONTENT_LEN = 1000


class DiscordClient(discord.Client):
    def __init__(self, *, intents=None, **options):
        if intents is None:
            intents = default_intents

        super().__init__(intents=intents, **options)

        self._browser = None

    async def match_command(self, ctx, command):
        """
        Matches commands that start with command prefix to their respective functionality.
        """
        split_command = command.split(" ")

        command = split_command[0][1:len(split_command[0])]
        parameters = split_command[1:len(split_command)]

        match command:
            case 'deck':
                await self.get_deck(ctx, parameters)
            case 'overlap':
                await self.get_overlap(ctx, parameters)
            case 'card':
                await self.get_card(ctx, parameters)
            case 'cimg':
                await self.get_card_image(ctx, parameters)
            case c if c in ['faq', 'faqs']:
                await self.get_faq(ctx, parameters)
            case _:
                print(f"Failed to interpret command: {command}")

    async def get_faq(self, ctx, card_name):
        """
        Gets FAQ entries from curiosa.io for given card name
        """
        card_name = util.get_card_name_url_form(' '.join(card_name))

        faq_entries = curiosa.get_faq_entries(
            card_name,
            self.prefixTree,
            self.cards
        )

        # preserve 6 space for code block
        truncated = util.message_truncate(faq_entries, 6)

        await ctx.send(util.code_blockify(truncated))

    async def get_deck(self, ctx, req):
        """
        Gets cards belonging to a deck from a curiosa.io URL or ID.
        """
        if not util.check_channel(ctx):
            await ctx.send("Deck command can currently only be used on servers, not in private messages.")
            return

        if len(req) > 1:
            await ctx.send("Incorrect usage, use only 1 deck parameter at a time.")
            return

        split_request = req[0].split("/")

        if len(split_request) > 1:
            received_output = curiosa.get_deck_from_url(
                req[0], False, self._browser)
        else:
            received_output = curiosa.get_deck_from_id(
                req[0], False, self._browser)

        await ctx.send(util.code_blockify(received_output))

    async def get_overlap(self, ctx, request):
        """
        Get overlapping cards between decks having provided at least 2 deck IDs.
        """
        if not util.check_channel(ctx):
            await ctx.send("Overlap command can currently only be used on servers, not in private messages.")
            return

        # Avoid blocking the whole app by providing a giant list of ids.
        if len(request) > 3:
            request = request[0:3]

        received_output = curiosa.get_overlapping_cards(*request, self._browser)
        await ctx.send(util.code_blockify(received_output))

    async def get_card(self, ctx, parameters):
        """
        Get card data by providing a card name.
        """
        card_name = util.get_card_name_url_form(' '.join(parameters))

        # Safe to assume cards is not none here since we exit if it is
        received_output = curiosa.get_card_from_name(
            card_name,
            self.prefixTree,
            self.cards
        )
        await ctx.send(util.code_blockify(received_output))

    async def get_card_image(self, ctx, card_name):
        """
        Gets card image in URL form
        """
        image_url = curiosa.generate_image_url(
            ' '.join(card_name),
            self.prefixTree,
            self.cards
        )

        if not image_url.startswith("https://"):
            image_url = util.code_blockify(image_url)

        await ctx.send(image_url)

    async def on_ready(self):
        print("Archimago now running.")
        await self.change_presence(status=None, activity=CustomActivity("Brewing magic.."))

    async def on_message(self, msg):
        content = msg.content
        channel = msg.channel

        # Don't process messages that are longer than max content length.
        if len(content) > MAX_CONTENT_LEN or len(content) == 0:
            return

        # Regex patterns for commands that are within messages.
        card_image_pattern = r'\[!(.*?)\]'
        ci_pattern_match = re.search(card_image_pattern, content)

        card_text_pattern = r'\[\[!(.*?)\]\]'
        ct_pattern_match = re.search(card_text_pattern, content)

        # We don't want to receive messages sent by the bot
        if msg.author == self.user:
            return

        if "stop" in content and DISCORD_BOT_MODE == 'debug':
            channel.send("Closing bot client..")
            curiosa.close_browser()
            sys.exit()

        if content[0] == "!":
            await self.match_command(channel, content)
            return

        if ct_pattern_match:
            card_name = ct_pattern_match.group(1).split(" ")
            await self.get_card(channel, card_name)
            return

        if ci_pattern_match:
            card_name = ci_pattern_match.group(1).split(" ")
            await self.get_card_image(channel, card_name)
            return

    def start_client(self, browser):
        if browser is None:
            print("Selenium webdriver required for starting discord client.")
            return

        self._browser = browser
        self.cards = util.load_cards()
        self.prefixTree = Trie(util.get_all_card_names(self.cards))

        async def runner():
            async with self:
                await self.start(DISCORD_BOT_TOKEN, reconnect=True)

        try:
            aiorun(runner())
        except KeyboardInterrupt:
            return

    async def close_client(self):
        self._browser.close()
        await self.close()
