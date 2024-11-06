# Changelog

Notable changes and additions will be logged into this file.

## \[1.0.7\] - 2024-6-11

### Added

- New commands!
  - `rulebook` returns the link to the current iteration of the rulebook.
  - `term` returns information related to the requested term.
  - `help` returns information about the bot and the implemented commands.

## \[1.0.6\] - 2024-5-11

### Added

- CI/CD integration
- Fuzzy matching for card names
- Discord bots status changes randomly every 15 minutes.
- When editing a message containing a command, update pre-existing reply.

### Changed

- `faq` and `cimg` commands now also offer card name suggestions
- Now replies to command messages instead of just sending messages
- Commands are now split into individual files, implementing new commands require having `BaseCommand` as superclass.

### Fixes

- `faq` command no longer sends the request if the card is not found internally.
- Gives user feedback over invalid command

## \[1.0.5\] - 2024-2-11

### Added

- Card name prefix table for autocompleting insufficient card names in commands.
- Unit tests for `util` and `trie` functionalities.
- Firefox support for Mac OS X.

### Changed

- Refactored code base to be in line with `flake8` linter
- Major project restructuring
- Selenium instances are now only instantiated when necessary
  - typer commands that don't require web scraping no longer create a webdriver instance

### Fixes

- Selenium webdriver instances are correctly closed after usage, no more lingering browser processes.

## \[1.0.4\] - 2024-24-10

### Added

- New commands:
  - `faq` and `faqs` command for discord bot that retrieve cards frequently-asked-questions from curiosa.io.
  - `faq` CLI command with same functionality.
- `requests` and `beautifulsoup4` are now dependencies

## \[1.0.3\] - 2024-22-10

### Added

- Fetching card image and text can be done within messages!
  - \[!\<card_name>\] for retrieving a cards image
  - \[\[!\<card_name>\]\] for retrieving a cards text

### Changed

- No longer uses a `discord.by` bot, switched to a client instance for more flexibility
- Gave the bot a custom activity status
- Deck and overlap commands are only accepted from servers. This is to stop blocking the bot from private messages.

### Removed

- With the removal of standard bot implementation the bot no longer has a help command. This will be readded later.

## \[1.0.2\] - 2024-20-10

### Added

- Fetching card images from Curiosa.io

### Changed

- Total cards also now give spellbook/atlas split
- Utility functionality shifted from `curiosa.py` to `util.py`
- Empty card type groups are no longer returned
- No overlapping cards found returns a string indicating that

### Fixes

- No longer throws an exception when using the commands (whoops)
- Avatar is no longer included in deck list total count
- Selenium is now configured to work both on Windows and Ubuntu

## \[1.0.1\] - 2024-20-10

### Added

- Ability to download the card list from curiosa.io.
- Command `card` for retrieving card information, refer to COMMANDS.md for usage.
- Command `stop` for shutting down the bot but only when the program is in debug mode.
- `util.py` for utility functions
- Chromedriver auto-installation

### Changed

- Changed the logo image to a better one.
- Implemented better error resolving when making failing requests to curiosa.io.
- Changed the command prefix to ! instead of $.
- Improved documentation, fixed typos
- Commands are now categorized

## \[1.0.0\] - 2024-19-10

- Initial release
