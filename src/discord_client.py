import asyncio
import os
import random
import re
import time
from asyncio import run as aiorun

import discord
from discord import CustomActivity
from dotenv import load_dotenv

from src.commands import (
    BaseCommand,
    CardCommand,
    CimgCommand,
    DeckCommand,
    FaqCommand,
    OverlapCommand,
    TermCommand,
    RulebookCommand,
    HelpCommand,
)

from . import util
from .trie import Trie

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("discord-bot-token")
DISCORD_BOT_MODE = os.getenv("discord-bot-mode")


class DiscordClient(discord.Client):
    def __init__(self, *, intents=None, **options):
        if intents is None:
            intents = discord.Intents.default()
            intents.members = True
            intents.message_content = True

        super().__init__(intents=intents, **options)

        self._browser = None
        self.current_status = ""
        self.commands: list[BaseCommand] = []

        # Store all replies sent by the bot and the time they are sent
        self.replies: list[tuple[int, int, float]] = list()

    async def handle_command(self, msg) -> str | None:
        """
        Matches commands that start with command prefix to their respective functionality.
        """
        content = msg.content

        if content[0] != self.config["command_prefix"]:
            return None

        split_command = content.split(" ")

        command = split_command[0][1:]
        parameters = split_command[1:]

        if command == "stop" and DISCORD_BOT_MODE == "debug":
            await self.close_client()

        return self.invoke_command(command, msg, parameters)

    def handle_regex(self, msg) -> str | None:
        """
        Handles regex commands
        """
        content = msg.content

        # Regex patterns for commands that are within messages.
        card_image_pattern = self.config["cimg_regex"]
        ci_pattern_match = re.search(card_image_pattern, content)

        card_text_pattern = self.config["card_regex"]
        ct_pattern_match = re.search(card_text_pattern, content)

        if ct_pattern_match:
            # Check if there are more than once matches.
            all_cards = util.get_all_card_names(self.cards)

            all_ref_cards = re.findall(card_image_pattern, content)
            all_ref_cards = list(map(util.get_url_form, all_ref_cards))
            all_ref_cards = list(filter(lambda x: x in all_cards, all_ref_cards))

            if len(all_ref_cards) == 1:
                card_name = ct_pattern_match.group(1).split(" ")
                return self.invoke_command("card", msg, card_name)

            return self.get_referenced_cards(all_ref_cards)

        if ci_pattern_match:
            card_name = ci_pattern_match.group(1).split(" ")
            return self.invoke_command("cimg", msg, card_name)

        return None

    def get_referenced_cards(self, cards: list[str]):
        """
        Returns a string that contains all referenced cards and links to their
        curiosa.io pages.
        """
        base_url = "https://curiosa.io/cards/"
        output = "Referenced cards:\n"

        for i, card in enumerate(cards):
            output += f"[{i + 1}] → " + base_url + card + "\n"

        return output

    def handle_incorrect_command(self, command) -> str:
        """
        Handle case where user send a message that is invalid.
        """
        return f"Invalid command: {util.code_blockify(command)}"

    async def handle_concurrent(self):
        """
        Handles concurrent events.

         - Changes the activity message of bot randomly every 15 minutes
         - Prunes reply list
        """
        current_time: int = 0

        while True:
            if current_time % self.config["status_update_time"] == 0:
                await self.presence_change()

            if current_time % self.config["prune_replies_time"] == 0:
                self.prune_replies()

            current_time += 1
            await asyncio.sleep(1)

    async def presence_change(self):
        """
        Changes presence to a random new one.
        """
        random_status = random.choice(
            list(
                filter(
                    lambda x: x != self.current_status, self.config["status_messages"]
                )
            )
        )

        print(f"Changing presence to: {random_status}")
        self.current_status = random_status

        await self.change_presence(
            status=None, activity=CustomActivity(self.current_status)
        )

    def prune_replies(self):
        """
        Prunes replies list so that it doesn't grow congested.

        When this is called, filter out messages that were replied to more than 30 seconds ago.
        """
        self.replies = list(
            filter(
                lambda x: time.time() - x[2] < self.config["prune_replies_time"],
                self.replies,
            )
        )

    async def handle_edit(self, index, message, after):
        """
        Handles the edit event by editing the reply message if the reply message is still present.
        """
        reply = self.replies[index]
        reply_id = reply[1]

        content = self.handle_regex(after)

        if content is None:
            content = await self.handle_command(after)

        reply_msg = await message.channel.fetch_message(reply_id)
        await reply_msg.edit(content=content)

    async def on_ready(self):
        """
        Handles the event after the client is initialized.
        """
        print("Archimago now running.")
        await self.handle_concurrent()

    async def on_message(self, msg):
        """
        Handles the event of message being sent to a server where the client is present.
        """
        # Sanity checks, don't process messages sent by the bot.
        if len(msg.content) == 0 or msg.author == self.user:
            return

        content = await self.handle_command(msg)
        if content is not None:
            await self.send_reply(msg, content)

        ic_content = self.handle_regex(msg)
        if ic_content is not None:
            await self.send_reply(msg, ic_content)

    async def on_message_edit(self, before, after):
        """
        Handles the event where a message has been edited.

        If such message contains a command, updates the reply or creates a new reply if one was not present.
        """
        # Sanity checks, don't process messages sent by the bot.
        if len(after.content) == 0 or before.author == self.user:
            return

        messages = list(map(lambda x: x[0], self.replies))
        msg_id = before.id

        try:
            # If we have already replied to the edited message, edit the reply
            index = messages.index(msg_id)

            await self.handle_edit(index, before, after)
        except ValueError:
            # No reply, just return.
            return

    def invoke_command(self, command: str, msg, parameters) -> str:
        """
        Invokes a command by command name and given parameters.
        """
        for comm in self.commands:
            if comm.is_command_suffix(command):
                return comm.get_content(msg, parameters)

        # If command was not found in registered commands, return the base case.
        return self.handle_incorrect_command(command)

    async def send_reply(self, message, content):
        """
        Helper function that adds bots replies to a trackable list.
        """
        reply = await message.reply(content)
        self.replies.append((message.id, reply.id, time.time()))

    def start_client(self, browser):
        """
        Starts the discord client and initializes card data.

        If card data fails to load, throws an exception.
        """
        if browser is None:
            print("Selenium webdriver required for starting discord client.")
            return

        self._browser = browser

        try:
            self.cards = util.load_cards()
            self.terms = util.load_toml("data/terms.toml")
            self.config = util.load_toml("data/config.toml")
        except Exception as e:
            print(f"Failed to initialize discord client due to exception: {e}")
            return

        self.prefixTree = Trie(util.get_all_card_names(self.cards))

        self.commands = list(
            [
                CardCommand(["card"], self.prefixTree, self.cards),
                FaqCommand(["faq", "faqs"], self.prefixTree, self.cards),
                CimgCommand(["cimg"], self.prefixTree, self.cards),
                DeckCommand(["deck"], self._browser),
                OverlapCommand(["overlap"], self._browser),
                TermCommand(["term"], self.terms),
                RulebookCommand(["rulebook", "rb"]),
            ]
        )

        self.commands.append(HelpCommand(["help"], self.commands))

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
