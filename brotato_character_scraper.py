#!/usr/bin/env python3
"""
Brotato Characters Scraper
Extracts all character data from the Brotato wiki and saves it as JSON
"""

import requests
import json
import re
from bs4 import BeautifulSoup
from typing import List, Dict, Any

def clean_text(text: str) -> str:
    """Clean up text by removing extra whitespace and newlines"""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text.strip())

def extract_stat_from_image(img_tag) -> str:
    """Extract stat name from image alt text or title"""
    if img_tag.get('alt'):
        return img_tag['alt']
    elif img_tag.get('title'):
        return img_tag['title']
    else:
        # Try to extract from the image filename
        src = img_tag.get('src', '')
        if 'Melee_Damage' in src:
            return 'Melee Damage'
        elif 'Ranged_Damage' in src:
            return 'Ranged Damage'
        elif 'Elemental_Damage' in src:
            return 'Elemental Damage'
        elif 'Max_HP' in src:
            return 'Max HP'
        elif 'Engineering' in src:
            return 'Engineering'
        elif 'Range' in src:
            return 'Range'
        elif 'Luck' in src:
            return 'Luck'
        elif 'Armor' in src:
            return 'Armor'
        elif 'Attack_Speed' in src:
            return 'Attack Speed'
        else:
            return 'Unknown Stat'

def clean_stats_text(stats_cell) -> str:
    """Clean up the stats text by replacing image tags with readable stat names"""
    if not stats_cell:
        return ""
    
    # Clone the cell to avoid modifying the original
    stats_html = str(stats_cell)
    
    # Find all image tags and replace them with stat names
    soup = BeautifulSoup(stats_html, 'html.parser')
    for img in soup.find_all('img'):
        stat_name = extract_stat_from_image(img)
        img.replace_with(f"[{stat_name}]")
    
    # Get the cleaned text
    cleaned_text = soup.get_text(separator=' ', strip=True)
    
    # Clean up extra whitespace
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    
    return cleaned_text

def extract_tags(tags_cell) -> List[str]:
    """Extract tag names from the tags cell"""
    if not tags_cell:
        return []
    
    tags = []
    for link in tags_cell.find_all('a'):
        tag_text = clean_text(link.get_text())
        if tag_text and tag_text not in tags:
            tags.append(tag_text)
    
    return tags

def extract_unlocks(unlocks_cell) -> List[Dict[str, str]]:
    """Extract unlock items/weapons from the unlocks cell"""
    if not unlocks_cell:
        return []
    
    unlocks = []
    for link in unlocks_cell.find_all('a'):
        # Skip if it's just an image link without text
        if not link.get_text().strip():
            continue
            
        unlock_name = clean_text(link.get_text())
        if unlock_name and unlock_name not in [u['name'] for u in unlocks]:
            # Try to determine if it's a weapon or item based on context
            unlock_type = "item"  # Default to item
            # You could add more logic here to distinguish weapons vs items
            unlocks.append({
                "name": unlock_name,
                "type": unlock_type
            })
    
    return unlocks

def scrape_brotato_characters() -> List[Dict[str, Any]]:
    """Scrape all Brotato characters from the wiki"""
    
    url = "https://brotato.wiki.spellsandguns.com/Characters"
    
    print(f"Fetching data from {url}...")
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the characters table
    characters_table = None
    
    # Look for the table that contains character data
    tables = soup.find_all('table')
    print(f"Found {len(tables)} tables on the page")
    
    # Look for the table that contains the most rows (likely the characters table)
    largest_table = None
    max_rows = 0
    
    for i, table in enumerate(tables):
        rows = table.find_all('tr')
        print(f"Table {i}: {len(rows)} rows")
        if len(rows) > max_rows:
            max_rows = len(rows)
            largest_table = table
    
    if largest_table:
        characters_table = largest_table
        print(f"Using table with {max_rows} rows")
    
    if not characters_table:
        print("Could not find characters table")
        return []
    
    characters = []
    rows = characters_table.find_all('tr')
    
    print(f"Processing {len(rows)} rows...")
    
    # Look for the header row to understand the structure
    header_found = False
    data_start_index = 0
    
    for i, row in enumerate(rows):
        cells = row.find_all(['td', 'th'])
        if len(cells) >= 4:
            # Check if this looks like a header row
            cell_texts = [clean_text(cell.get_text()) for cell in cells]
            if any('Name' in text for text in cell_texts) or any('Stats' in text for text in cell_texts):
                print(f"Found header row at index {i}: {cell_texts}")
                header_found = True
                data_start_index = i + 1
                break
    
    if not header_found:
        print("No header found, starting from row 0")
        data_start_index = 0
    
    # Process data rows
    for i, row in enumerate(rows[data_start_index:], data_start_index):
        cells = row.find_all(['td', 'th'])
        
        if len(cells) < 4:  # Skip rows that don't have enough cells
            continue
        
        try:
            # Debug: print first few cell contents
            if len(characters) < 3:
                cell_texts = [clean_text(cell.get_text())[:50] for cell in cells[:4]]
                print(f"Row {i} cells: {cell_texts}")
            
            # Extract character name from the first cell
            name_cell = cells[0]
            # Get the text directly from the cell
            character_name = clean_text(name_cell.get_text())
            
            # Debug output for first few characters
            if len(characters) < 3:
                print(f"Extracted character name: '{character_name}' from cell: '{clean_text(name_cell.get_text())[:50]}'")
            
            if not character_name or len(character_name) < 2:
                print(f"Skipping row {i}: invalid character name '{character_name}'")
                continue
            
            # Check if it's a DLC character
            is_dlc = '(DLC)' in character_name
            
            # Remove (DLC) suffix if present
            character_name = re.sub(r'\s*\(DLC\)\s*$', '', character_name)
            
            # Extract stats from second cell
            stats = clean_stats_text(cells[1])
            
            # Extract unlock requirement from third cell
            unlock_req = clean_text(cells[2].get_text())
            
            # Extract unlocks from fourth cell
            unlocks = extract_unlocks(cells[3])
            
            # Extract tags from fifth cell (if present)
            tags = extract_tags(cells[4]) if len(cells) > 4 else []
            
            character_data = {
                "name": character_name,
                "stats": stats,
                "unlocked_by": unlock_req,
                "unlocks": unlocks,
                "tags": tags,
                "is_dlc": is_dlc
            }
            
            characters.append(character_data)
            print(f"Processed character {len(characters)}: {character_name}")
            
        except Exception as e:
            print(f"Error processing row {i}: {e}")
            continue
    
    return characters

def main():
    """Main function to scrape characters and save to JSON"""
    try:
        characters = scrape_brotato_characters()
        
        if not characters:
            print("No characters found. The scraping might have failed.")
            return
        
        # Save to JSON file
        output_file = "brotato_characters.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "total_characters": len(characters),
                "characters": characters
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\nSuccessfully scraped {len(characters)} characters!")
        print(f"Data saved to {output_file}")
        
        # Print some sample characters
        print("\nSample characters:")
        for character in characters[:3]:
            print(f"- {character['name']} (DLC: {character['is_dlc']}): {character['stats'][:100]}...")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
