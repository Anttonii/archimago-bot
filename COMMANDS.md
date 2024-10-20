# Commands

**NOTE:** The bot is currently configured to use `!` as the command prefix. When using the bot, make sure to start all commands with `!`. This is subject to change in the future.

## card

The card command takes in a card name regardless of capitalization and returns information attached to the card.

Example:

```
!card apprentice wizard
```

Output:

```
Name: Apprentice Wizard
Rarity: Ordinary
Type: Minion
Rules Text: Spellcaster

Genesis → Draw a spell.
Attack: 1
Defence: 1
Thresholds: 1A 
Sets: Alpha, Beta
```

## deck

The deck commands takes in either a single ID or URL from which it then webscrapes the deck information.

Example:

```
!deck cm2d6ea5g00etsenu9qa7syod
```

is the same as the command

```
!deck https://curiosa.io/decks/cm2d6ea5g00etsenu9qa7syod
```

yielding a list of cards.

## overlap

Overlap gives you the list of cards between multiple decks that are common between them. This command can take in any amount of IDs, but for the sake of the bot becoming blocked during requests, it only takes in the first 3 and returns their overlap.

```
!overlap cm2d6ea5g00etsenu9qa7syod cm21hvt0n01fz5ftgdsevs0wu
```

yield the list of cards that the decks have in common.