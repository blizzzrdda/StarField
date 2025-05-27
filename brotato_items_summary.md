# Brotato Items Data Summary

## Overview
Successfully extracted **224 items** from the Brotato Wiki (https://brotato.wiki.spellsandguns.com/Items)

## Data Structure
Each item contains the following information:
- **name**: Item name (string)
- **rarity**: Tier 1-4 (string)
- **effects**: Detailed description of item effects (string)
- **base_price**: Shop price in materials (integer)
- **limit**: Maximum number you can have (0 = unlimited) (integer)
- **unlocked_by**: Character or condition required to unlock (string)
- **tags**: Array of gameplay tags (array of strings)
- **is_dlc**: Whether the item is from DLC content (boolean)

## Rarity Distribution
- **Tier 1**: Basic items (lowest tier)
- **Tier 2**: Intermediate items
- **Tier 3**: Advanced items
- **Tier 4**: Legendary items (highest tier)

## DLC Items
Items marked with `"is_dlc": true` are from downloadable content expansions.

## Tags System
Items are categorized with tags that correspond to stats and gameplay mechanics:
- **Stat Tags**: Max HP, Damage, Attack Speed, Crit Chance, etc.
- **Mechanic Tags**: Pickup, Explosive, Structure, Economy, etc.
- **Character Tags**: Tags that match specific character builds

## Sample Items

### Acid (Tier 2)
```json
{
  "name": "Acid",
  "rarity": "Tier 2",
  "effects": "+8 Max HP -2 % Dodge -2 Knockback",
  "base_price": 65,
  "limit": 0,
  "unlocked_by": "",
  "tags": ["Max HP"],
  "is_dlc": false
}
```

### Potato (Tier 4)
```json
{
  "name": "Potato",
  "rarity": "Tier 4",
  "effects": "+3 Max HP +2 HP Regeneration +1 % Life Steal +5 % Damage +5 % Attack Speed +3 % Speed +3 % Dodge +1 Armor +5 Luck",
  "base_price": 95,
  "limit": 0,
  "unlocked_by": "Win a run with Well Rounded",
  "tags": ["Max HP", "HP Regeneration", "Damage", "Speed", "Luck"],
  "is_dlc": false
}
```

## Files Generated
1. **brotato_items.json**: Complete dataset with all 224 items
2. **brotato_scraper.py**: Python script used to extract the data
3. **brotato_items_summary.md**: This summary file

## Usage
The JSON file can be used for:
- Game analysis and statistics
- Building optimization tools
- Creating item databases
- Developing Brotato-related applications
- Research and data analysis

## Data Quality Notes
- All 224 items successfully extracted
- Effects text includes stat scaling information
- Some effects contain image references (e.g., "[Max HP.png]") that indicate stat scaling
- DLC items properly identified
- Character unlock requirements captured where available
- Tags properly extracted and categorized

## Last Updated
Data extracted on: $(date)
Source: Brotato Wiki (https://brotato.wiki.spellsandguns.com/Items)
Version: 1.1.10.9 (as noted on the wiki)
