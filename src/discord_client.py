from . import curiosa, util
from .trie import Trie

import asyncio
import os
import random
import re
from asyncio import run as aiorun

from dotenv import load_dotenv

import discord
from discord import CustomActivity

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('discord-bot-token')
DISCORD_BOT_MODE = os.getenv('discord-bot-mode')

# Status messages chosen by random displayed under the bots name
STATUS_MESSAGES = [
    "Brewing magic..",
    "Casting Blink..",
    "Sitting by the bonfire..",
    "Sitting on the Immortal Throne..",
    "Erupting Vesuvius..",
    "Pathfinding..",
    "Navigating the Stormy Seas..",
    "Attending the Royal Wedding.."
]

# The time it takes for the status to randomly change in seconds.
STATUS_UPDATE_TIMER = 300

# Command prefix character, messages starting with this are considered commands.
COMMAND_PREFIX = '!'


class DiscordClient(discord.Client):
    def __init__(self, *, intents=None, **options):
        if intents is None:
            intents = discord.Intents.default()
            intents.members = True
            intents.message_content = True

        super().__init__(intents=intents, **options)

        self._browser = None
        self.current_status = ""

    async def handle_command(self, ctx, command):
        """
        Matches commands that start with command prefix to their respective functionality.
        """
        if command[0] != COMMAND_PREFIX:
            return

        split_command = command.split(" ")

        command = split_command[0][1:]
        parameters = split_command[1:]

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
            case 'stop':
                if DISCORD_BOT_MODE == 'debug':
                    await self.close_client()
            case _:
                print(f"Failed to interpret command: {command}")

    async def handle_regex(self, ctx, content):
        """
        Handles regex commands
        """
        # Regex patterns for commands that are within messages.
        card_image_pattern = r'\[!(.*?)\]'
        ci_pattern_match = re.search(card_image_pattern, content)

        card_text_pattern = r'\[\[!(.*?)\]\]'
        ct_pattern_match = re.search(card_text_pattern, content)

        if ct_pattern_match:
            card_name = ct_pattern_match.group(1).split(" ")
            await self.get_card(ctx, card_name)
            return

        if ci_pattern_match:
            card_name = ci_pattern_match.group(1).split(" ")
            await self.get_card_image(ctx, card_name)
            return

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

    async def handle_presence(self):
        """
        Changes the activity message of bot randomly every 15 minutes
        """
        while True:
            random_status = random.choice(STATUS_MESSAGES)
            while random_status == self.current_status:
                random_status = random.choice(STATUS_MESSAGES)

            print(f"Changing presence to: {random_status}")
            self.current_status = random_status

            await self.change_presence(
                status=None,
                activity=CustomActivity(self.current_status)
            )

            await asyncio.sleep(STATUS_UPDATE_TIMER)

    async def on_ready(self):
        """
        Handles the event after the client is initialized.
        """
        print("Archimago now running.")
        await self.handle_presence()

    async def on_message(self, msg):
        """
        Handles the event of message being sent to a server where the client is present.
        """
        content = msg.content
        channel = msg.channel

        # Sanity checks, don't process messages sent by the bot.
        if len(content) == 0 or msg.author == self.user:
            return

        await self.handle_command(channel, content)
        await self.handle_regex(channel, content)

    def start_client(self, browser):
        """
        Starts the discord client and initializes card data.

        If card data fails to load, throws an exception.
        """
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
            self._browser.quit()
            return

    async def close_client(self):
        """
        Closes the discord client instance.
        """
        print("Closing Archimago..")
        self._browser.close()
        await self.close()
