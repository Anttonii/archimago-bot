# Changelog

Notable changes and additions will be logged into this file.

## [1.0.4] - 2024-24-10

### Added
 
 - New commands:
   - `faq` and `faqs` command for discord bot that retrieve cards frequently-asked-questions from curiosa.io.
   - `faq` CLI command with same functionality.
 - `requests` and `beautifulsoup4` are now depedencies


## [1.0.3] - 2024-22-10

### Added

 - Fetching card image and text can be done within messages!
   - [!<card_name>] for retrieving a cards image
   - [[!<card_name>]] for retrieving a cards text

### Changed

 - No longer uses a `discord.by` bot, switched to a client instance for more flexibility
 - Gave the bot a custom activity status
 - Deck and overlap commands are only accepted from servers. This is to stop blocking the bot from private messages.

 ### Removed

  - With the removal of standard bot implementation the bot no longer has a help command. This will be readded later.

## [1.0.2] - 2024-20-10

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

## [1.0.1] - 2024-20-10

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

## [1.0.0] - 2024-19-10

 - Initial release
