#!/usr/bin/env python3
"""
Brotato Items Scraper
Extracts all item data from the Brotato wiki and saves it as JSON
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
        else:
            return 'Unknown Stat'

def clean_effects_text(effects_cell) -> str:
    """Clean up the effects text by replacing image tags with readable stat names"""
    if not effects_cell:
        return ""

    # Clone the cell to avoid modifying the original
    effects = effects_cell.get_text(separator=' ', strip=True)

    # Also process the HTML to replace image tags
    effects_html = str(effects_cell)

    # Find all image tags and replace them with stat names
    soup = BeautifulSoup(effects_html, 'html.parser')
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

def parse_price(price_text: str) -> int:
    """Parse price from text, return 0 if not found"""
    if not price_text:
        return 0

    # Extract numbers from the text
    numbers = re.findall(r'\d+', price_text)
    if numbers:
        return int(numbers[0])
    return 0

def parse_limit(limit_text: str) -> int:
    """Parse limit from text, return 0 for unlimited"""
    if not limit_text or limit_text.strip() == '':
        return 0

    # Extract numbers from the text
    numbers = re.findall(r'\d+', limit_text)
    if numbers:
        return int(numbers[0])
    return 0

def extract_rarity(rarity_text: str) -> str:
    """Extract rarity tier from text"""
    if not rarity_text:
        return "Unknown"

    rarity_text = clean_text(rarity_text)
    if 'Tier 1' in rarity_text:
        return "Tier 1"
    elif 'Tier 2' in rarity_text:
        return "Tier 2"
    elif 'Tier 3' in rarity_text:
        return "Tier 3"
    elif 'Tier 4' in rarity_text:
        return "Tier 4"
    else:
        return rarity_text

def scrape_brotato_items() -> List[Dict[str, Any]]:
    """Scrape all Brotato items from the wiki"""

    url = "https://brotato.wiki.spellsandguns.com/Items"

    print(f"Fetching data from {url}...")
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the items table - it's likely the largest table on the page
    items_table = None

    # Try to find the table by looking for characteristic content
    tables = soup.find_all('table')
    print(f"Found {len(tables)} tables on the page")

    # Look for the table that contains the most rows (likely the items table)
    largest_table = None
    max_rows = 0

    for i, table in enumerate(tables):
        rows = table.find_all('tr')
        print(f"Table {i}: {len(rows)} rows")
        if len(rows) > max_rows:
            max_rows = len(rows)
            largest_table = table

    if largest_table:
        items_table = largest_table
        print(f"Using table with {max_rows} rows")

    if not items_table:
        print("Could not find items table")
        return []

    items = []
    rows = items_table.find_all('tr')

    print(f"Processing {len(rows)} rows...")

    # Look for the header row to understand the structure
    header_found = False
    data_start_index = 0

    for i, row in enumerate(rows):
        cells = row.find_all(['td', 'th'])
        if len(cells) >= 6:
            # Check if this looks like a header row
            cell_texts = [clean_text(cell.get_text()) for cell in cells]
            if any('Name' in text for text in cell_texts) or any('Rarity' in text for text in cell_texts):
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

        if len(cells) < 6:  # Skip rows that don't have enough cells
            continue

        try:
            # Debug: print first few cell contents
            if len(items) < 5:
                cell_texts = [clean_text(cell.get_text())[:50] for cell in cells[:4]]
                print(f"Row {i} cells: {cell_texts}")

            # Extract item name from the first cell
            name_cell = cells[0]
            # Get the text directly from the cell
            item_name = clean_text(name_cell.get_text())

            # Debug output for first few items
            if len(items) < 5:
                print(f"Extracted item name: '{item_name}' from cell: '{clean_text(name_cell.get_text())[:50]}'")

            if not item_name or len(item_name) < 2:
                print(f"Skipping row {i}: invalid item name '{item_name}'")
                continue

            # Check if it's a DLC item before removing the suffix
            is_dlc = '(DLC)' in item_name

            # Remove (DLC) suffix if present
            item_name = re.sub(r'\s*\(DLC\)\s*$', '', item_name)

            # Extract rarity from second cell
            rarity = extract_rarity(cells[1].get_text())

            # Extract effects from third cell
            effects = clean_effects_text(cells[2])

            # Extract price from fourth cell
            price = parse_price(cells[3].get_text())

            # Extract limit from fifth cell
            limit = parse_limit(cells[4].get_text())

            # Extract unlock requirement from sixth cell
            unlock_req = clean_text(cells[5].get_text()) if len(cells) > 5 else ""

            # Extract tags from seventh cell
            tags = extract_tags(cells[6]) if len(cells) > 6 else []

            item_data = {
                "name": item_name,
                "rarity": rarity,
                "effects": effects,
                "base_price": price,
                "limit": limit,
                "unlocked_by": unlock_req,
                "tags": tags,
                "is_dlc": is_dlc
            }

            items.append(item_data)
            print(f"Processed item {len(items)}: {item_name}")

        except Exception as e:
            print(f"Error processing row {i}: {e}")
            continue

    return items

def main():
    """Main function to scrape items and save to JSON"""
    try:
        items = scrape_brotato_items()

        if not items:
            print("No items found. The scraping might have failed.")
            return

        # Save to JSON file
        output_file = "brotato_items.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "total_items": len(items),
                "items": items
            }, f, indent=2, ensure_ascii=False)

        print(f"\nSuccessfully scraped {len(items)} items!")
        print(f"Data saved to {output_file}")

        # Print some sample items
        print("\nSample items:")
        for item in items[:3]:
            print(f"- {item['name']} ({item['rarity']}): {item['effects'][:100]}...")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
