<p align="center">
  <img src="data/archimago.png" />
</p>

The wizard of the Finnish Sorcery TCG [discord server](https://discord.gg/en3tmeSGGv). A discord bot that web-scrapes [curiosa.io](https://curiosa.io/) for deck recipes and the official API for card information! Full command documentation is under the `COMMANDS.md` file.

<p align="center">
<a href="https://discord.com/api/oauth2/authorize?client_id=1297139330279669820&permissions=2048&scope=bot%20applications.commands">Invite Archimago to your server by clicking here!</a>
</p>

## Features

Some notable features of Archimago:

- Scraping Curiosa.io for deck recipes and card FAQ entries.
- Retrieving card information and card images.
- Fuzzy card name matching to help users find cards more accurately.
- CI/CD integration for easy development.

Future features and features in progress are documented in the `TODO.md` file.

## Installation

This repository is built with `uv`. To step `uv`, follow the instructions [here](https://docs.astral.sh/uv/getting-started/installation/). After installing uv, simply run:

```sh
uv sync --all-groups
```

Make sure to also have chromium webdriver installed when running from an unix environment:

```sh
sudo apt update
sudo apt install chromium-chromedriver
```

After installing the dependencies, the program will when first run make sure that chromedriver is installed to your path. Alternatively, you can also provide your own instance of a webdriver when interacting with `curiosa.py`.

The program also caches the cards data that can be retrieved from [curiosa.io API](https://api.sorcerytcg.com/). For `card` CLI command to work, first run

```sh
uv run main.py download
```

which then downloads the `cards.json` file into the data folder.

## Usage

Although the main usage is to have this function as bot on the Finnish sorcery server, the program can also be run as a CLI. For instance fetching a deck by ID can be done by

```sh
uv run main.py id <your_deck_id_here>
```

which webscapes the deck and then prints your deck list a string. Running

```sh
uv run main.py --help
```

will get you started on interacting with the program through CLI. If you want to add the bot to your own server, you can invite it with this [link](https://discord.com/api/oauth2/authorize?client_id=1297139330279669820&permissions=2048&scope=bot%20applications.commands).

**NOTE**: this bot can handle single requests at a time, it does no buffering/pooling and thus if a command is given when the bot is processing another command, it will not be able to handle that request.

**NOTE 2**: this bot doesn't accept web-scraping commands through private messaging due to reason above.

**NOTE 3**: if you want to run your own instance, refer to [discord.py](https://discordpy.readthedocs.io/en/latest/intro.html) documentation for setting the discord bot account up and then provide the corresponding bot token to the `discord_client` instance.

## License

This repository is licensed under the MIT license.
