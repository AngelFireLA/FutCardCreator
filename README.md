# FUT Card Creator

**FUT Card Creator** is a Python package that allows you to create custom FIFA Ultimate Team (FUT) cards with ease. You can generate cards for your favorite players, complete with their stats, position, nationality, club, and more.

## Features

- Generate custom FUT cards with player photos, club logos, national flags, and stats.
- Automatically fetch and cache club logos and national flags using online APIs.
- Easily customize and update player stats.
- Automatically calculate the overall rating for players based on their position.
- Automatically update player stats when their overall rating changes.
- Export the generated FUT card as an image file.

## Installation

To install FUT Card Creator, simply run:

```bash
pip install fut_card_creator
```

## Requirements

- Python 3.6 or higher
- `Pillow` for image processing
- `requests` for API calls
- `fuzzywuzzy` and `python-Levenshtein` for fuzzy string matching

These dependencies will be installed automatically when you install the package.

## Usage

Here’s a basic example of how to use the FUT Card Creator:

```python
from fut_card_creator.fut_card_creator import Player, Card

# Create a Player instance
player = Player(
    name="Lionel Messi",
    photo_path="path/to/messi_photo.png",
    club="Paris Saint-Germain",
    nation="Argentina",
    overall=93,
    position="RW",
    stats={"PAC": 85, "SHO": 92, "PAS": 91, "DRI": 95, "DEF": 35, "PHY": 65}
)

# Create a FUT card
fut_card = Card(player, card_type="gold")

# Generate the card image
fut_card.create_image()

# Export the card image
fut_card.export_image("messi_fut_card.png")
```

### Automatic Overall Calculation

The FUT Card Creator automatically calculates a player’s overall rating based on their position and individual stats. Each position has a unique formula that emphasizes different stats, ensuring that the overall rating reflects the player’s role on the field.

### Automatic Stat Updater

When you update a player's overall rating, the package automatically adjusts the player's stats to match the new overall. This ensures that the stats are consistent with the player's new rating, maintaining a realistic balance.

### Customization

You can easily customize various aspects of the FUT card, such as:

- **Player stats**: Modify individual stats using the `Player` class.
- **Card type**: Use different card templates by specifying the `card_type` in the `Card` class.
- **Image paths**: Provide paths to player photos, club logos, and nation flags.

### Directory Structure

Make sure your project structure looks like this:

```
fut_card_creator/
│
├── fonts/
│   └── DINPro CondBold.otf   # Required font file
│
├── images/
│   ├── card_templates/       # Store card template images here
│   ├── club_logo_cache/      # Automatically caches club logos
│   └── nation_cache/         # Automatically caches national flags
│
├── __init__.py
├── fut_card_creator.py
└── utils.py
│
setup.py
```

### Dependencies

The package requires the following dependencies, which will be installed automatically:

- `Pillow`
- `requests`
- `fuzzywuzzy`
- `python-Levenshtein`

