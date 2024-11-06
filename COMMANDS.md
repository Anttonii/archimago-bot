# Commands

**NOTE:** All of these commands are only for the discord bot. For the CLI run: `python main.py --help`.

In all examples output refers to a message sent by the bot after the example input command has been given.

## Inter-comment commands

There are two commands that can be invoked within messages without adding any special prefix.

### \[!\<card_name>\]

Works identical to `!cimage`

Example:

```
I was thinking of adding [!abundance] to my deck.
```

Output:

```
https://curiosa.io/_next/image?url=https://d27a44hjr9gen3.cloudfront.net/alp/abundance_b_s.png&w=384&q=75
```

### \[\[!\<card_name>\]\]

Works identical to `!card`.

Example:

```
I was thinking of adding [[!apprentice wizard]] to my deck.
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

## Prefixed commands

**NOTE:** The bot is currently configured to use `!` as the command prefix. When using the bot, make sure to start all commands with `!`. This is subject to change in the future.

### card

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

### cimg

The cimg command takes in a card name regardless of capitalization and returns the URL for the image of the card.

Example:

```
!cimg Abundance
```

Output:

```
https://curiosa.io/_next/image?url=https://d27a44hjr9gen3.cloudfront.net/alp/abundance_b_s.png&w=384&q=75
```

### deck

The deck commands takes in either a single ID or URL from which it then webscrapes the deck information.

Example:

```
!deck cm2d6ea5g00etsenu9qa7syod
```

is the same as the command

```
!deck https://curiosa.io/decks/cm2d6ea5g00etsenu9qa7syod
```

Output:

```
The deck from url: https://curiosa.io/decks/cm2d6ea5g00etsenu9qa7syod has the following cards:

Avatar (1)
  1 - Druid
Auras (3)
  2 - Sylvan Splendor
  1 - Atlantean Fate
Artifacts (8)
  2 - Just a Rock
  1 - Ring of Morrigan
  1 - Pnakotic Manuscript
  2 - Horn of Caerleon
  2 - Drums of Doom
Minions (33)
  2 - Porcupine Pufferfish
  4 - Raal Dromedary
  4 - Swamp Buffalo
  2 - Thieving Magpie
  4 - Vile Imp
  3 - War Horse
  3 - Lugbog Cat
  3 - Redcap Powries
  2 - Salmon of Knowledge
  3 - Tufted Turtles
  2 - Monstrous Lion
  1 - Ruler of Thul
Magics (6)
  1 - Plague of Frogs
  1 - Pollimorph
  3 - Minor Explosion
  1 - Peasant Revolt
Sites (30)
  3 - Autumn River
  2 - Babbling Brook
  1 - Bonfire
  1 - Bower of Bliss
  1 - Fields of Camlann
  1 - Floodplain
  4 - Forge
  3 - Funeral Pyre
  4 - Hamlet
  3 - Oasis
  1 - River of Flame
  1 - Tadpole Pool
  3 - Troll Bridge
  2 - Winter River

Total: 80 cards (50 Spellbook, 30 Atlas)
```

### overlap

The overlap command gives you the list of cards common between multiple decks. This command can take in any amount of IDs, but for the sake of the bot becoming blocked during requests, it only takes in up to the first 3 and returns their overlap.

Example:

```
!overlap cm2d6ea5g00etsenu9qa7syod cm21hvt0n01fz5ftgdsevs0wu
```

Output:

```
The overlapping cards are:
Artifacts (1)
  1 - Ring of Morrigan
Sites (1)
  1 - Fields of Camlann
```

### faq or faqs

The faq (faqs has same functionality) command retrieves FAQ information related to a card from curiosa.io and returns it as a message.

Example:

```
!faq midland army
```

Output:

```
FAQ entries found for card: midland_army

Q: Are Foot Soldiers Ordinary earth minions?
A: Yes!
```

### rulebook or rb

Returns the official curiosa.io rulebook.

Usage:

```
!rulebook
!rb
```

Output:

```
https://drive.google.com/file/d/1sgQo0xf0N2teIR0zlyl91g9j6LVncZnr/view
```

### term

Returns information about a given game term/keyword.

Usage:

```
!term stealth
```

Output:

```
Minions with Stealth cannot be targeted by spells
or abilities from your opponents, they cannot be
attacked, intercepted, or defended against, and
projectiles cannot hit them.

Stealth is tracked with a stealth token.

Minions lose Stealth after they activate a special
ability, deal damage, or attack. When this happens,
remove the Stealth token.
```

### help

Builds a help command from all registered commands' individual pydocs. Also provides information about individual commands when using a command suffix as a parameter.

Usage:

```
!help
```

Output:

```
Archimago provide the following commands:

- card: Get information about a card by providing a card name.
- faq, faqs: Gets FAQ entries from curiosa.io for given card name.
- cimg: Gets card image in URL form.
- deck: Gets cards belonging to a deck from a curiosa.io URL or ID.
- overlap: Get overlapping cards between decks having provided at least 2 deck IDs.
- term: Get information about term.
- rulebook, rb: Get URL for the official rulebook.
- help: Returns this message.
```

Usage:

```
!help deck
```

Output:

```
Usage:


!deck <id> returns the deck of cards from given curiosa.io deck ID.
!deck <url> returns the deck of cards from given curiosa.io deck URL.
```
