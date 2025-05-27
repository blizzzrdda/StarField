# Brotato Characters Data Summary

## Overview
Successfully extracted **62 characters** from the Brotato Wiki (https://brotato.wiki.spellsandguns.com/Characters)

## Data Structure
Each character contains the following information:
- **name**: Character name (string)
- **stats**: Detailed character stats and abilities (string)
- **unlocked_by**: Requirement to unlock the character (string)
- **unlocks**: Array of items/weapons unlocked by this character (array of objects)
- **tags**: Array of gameplay tags associated with the character (array of strings)
- **is_dlc**: Whether the character is from DLC content (boolean)

## Character Distribution
- **Base Game Characters**: 47 characters
- **DLC Characters**: 15 characters

## DLC Characters
Characters marked with `"is_dlc": true` are from the "Abyssal Terrors" DLC expansion:
- Sailor, Curious, Builder, Captain, Creature, Chef, Druid, Dwarf, Gangster, Diver, Hiker, Buccaneer, Ogre, Romantic

## Unlock Requirements
Characters have various unlock requirements:
- **Default**: Some characters are unlocked by default
- **Kill-based**: Kill X enemies, kill bosses/elites
- **Collection-based**: Collect X materials, pick up consumables
- **Stat-based**: Reach certain stat thresholds
- **Achievement-based**: Complete specific challenges

## Character Tags System
Characters are categorized with tags that indicate their gameplay focus:
- **Damage Types**: Melee Damage, Ranged Damage, Elemental Damage
- **Defensive**: Max HP, Armor, Dodge, HP Regeneration
- **Utility**: Engineering, Structure, Luck, Speed
- **Special**: Curse, Consumable, Explosive, XP Gain

## Sample Characters

### Well Rounded (Base Game)
```json
{
  "name": "Well Rounded",
  "stats": "+5 Max Hp +5% Speed +8 Harvesting",
  "unlocked_by": "Unlocked by default",
  "unlocks": [{"name": "Potato", "type": "item"}],
  "tags": [],
  "is_dlc": false
}
```

### Sailor (DLC)
```json
{
  "name": "Sailor",
  "stats": "+200% damage with Naval weapons against cursed enemies +25 Curse -25 % Damage You can only equip tier II weapons or above Dodge is capped at 20% Harvesting modifications are reduced by 100%",
  "unlocked_by": "Unlocked by default",
  "unlocks": [{"name": "Treasure Map", "type": "item"}],
  "tags": ["Curse"],
  "is_dlc": true
}
```

### Pacifist (Base Game)
```json
{
  "name": "Pacifist",
  "stats": "Gain 0.65 material and XP for every living enemy at the end of a wave You start with 1 Lumberjack Shirt -100% Damage -100 Engineering",
  "unlocked_by": "Collect 10000 materials",
  "unlocks": [{"name": "Panda", "type": "item"}],
  "tags": ["Max HP", "HP Regeneration", "Armor"],
  "is_dlc": false
}
```

## Character Unlock Progression
Characters unlock in a progression system based on achievements:
- **Early Game**: Default characters (Well Rounded, Brawler, Crazy, Ranger, Mage)
- **Mid Game**: Kill/collection milestones (Chunky, Old, Lucky, Mutant)
- **Late Game**: High-tier achievements (complex stat requirements, large numbers)

## Files Generated
1. **brotato_characters.json**: Complete dataset with all 62 characters
2. **brotato_character_scraper.py**: Python script used to extract the data
3. **brotato_characters_summary.md**: This summary file

## Usage
The JSON file can be used for:
- Character progression tracking
- Build planning and optimization
- Game guides and wikis
- Character unlock calculators
- Statistical analysis of character balance

## Data Quality Notes
- All 62 characters successfully extracted
- Stats include detailed ability descriptions
- Unlock requirements properly captured
- Character-specific item unlocks included
- DLC characters properly identified
- Tags system provides gameplay categorization

## Character Categories by Playstyle

### **Damage Focused**
- Brawler (Unarmed), Crazy (Precise), Ranger (Ranged), Gladiator (Melee)

### **Defensive**
- Chunky (HP), Ghost (Dodge), Knight (Armor), Vampire (Life Steal)

### **Economic**
- Saver (Materials), Entrepreneur (Economy), Arms Dealer (Weapons)

### **Specialist**
- Engineer (Structures), Doctor (Healing), Hunter (Range), Artificer (Explosions)

### **Challenge**
- Pacifist (No Damage), Wildling (Low Tier), One Armed (Limited Weapons)

## Last Updated
Data extracted on: $(date)
Source: Brotato Wiki (https://brotato.wiki.spellsandguns.com/Characters)
Version: 1.1.10.9 (as noted on the wiki)
