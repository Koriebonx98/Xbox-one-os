#!/usr/bin/env python3
"""
Script to add a "Description" field to all games in a Switch games JSON file.

Usage:
    python add_description_to_games.py <input_json_file> [output_json_file]
    
If output_json_file is not provided, the input file will be backed up with .backup extension
and the original file will be updated.
"""

import json
import sys
import os
from pathlib import Path


def add_description_to_games(data, description_value=""):
    """
    Recursively add 'Description' field to game entries.
    
    Args:
        data: The JSON data structure (dict, list, or primitive)
        description_value: The value to set for Description field (default: empty string)
    
    Returns:
        Modified data structure with Description fields added
    """
    if isinstance(data, dict):
        # If this dict doesn't have a Description key, add it
        if 'Description' not in data:
            # Check if this looks like a game entry (has common game fields)
            game_indicators = ['Name', 'name', 'Title', 'title', 'GameName', 'game_name']
            if any(key in data for key in game_indicators):
                data['Description'] = description_value
        
        # Recursively process all values in the dict
        for key, value in data.items():
            data[key] = add_description_to_games(value, description_value)
    
    elif isinstance(data, list):
        # Process each item in the list
        for i, item in enumerate(data):
            data[i] = add_description_to_games(item, description_value)
    
    return data


def process_json_file(input_file, output_file=None, backup=True):
    """
    Process a JSON file to add Description fields to all games.
    
    Args:
        input_file: Path to the input JSON file
        output_file: Path to the output JSON file (optional)
        backup: Whether to create a backup of the input file (default: True)
    
    Returns:
        Number of games processed
    """
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"Error: Input file '{input_file}' does not exist.")
        return 0
    
    # Read the JSON file
    print(f"Reading JSON file: {input_file}")
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON file. {e}")
        return 0
    except Exception as e:
        print(f"Error: Failed to read file. {e}")
        return 0
    
    # Count games before processing
    def count_games(obj):
        count = 0
        if isinstance(obj, dict):
            # Check if this dict looks like a game
            game_indicators = ['Name', 'name', 'Title', 'title', 'GameName', 'game_name']
            if any(key in obj for key in game_indicators):
                count = 1
            # Recursively count in nested structures
            for value in obj.values():
                count += count_games(value)
        elif isinstance(obj, list):
            for item in obj:
                count += count_games(item)
        return count
    
    games_count = count_games(data)
    print(f"Found {games_count} game entries")
    
    # Add Description fields
    print("Adding 'Description' fields...")
    modified_data = add_description_to_games(data, description_value="")
    
    # Determine output file
    if output_file is None:
        output_path = input_path
        if backup:
            backup_path = input_path.with_suffix(input_path.suffix + '.backup')
            print(f"Creating backup: {backup_path}")
            import shutil
            shutil.copy2(input_path, backup_path)
    else:
        output_path = Path(output_file)
    
    # Write the modified JSON
    print(f"Writing updated JSON to: {output_path}")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(modified_data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error: Failed to write output file. {e}")
        return 0
    
    print(f"Successfully processed {games_count} games!")
    print(f"All games now have a 'Description' field (blank by default)")
    
    return games_count


def main():
    """Main function to handle command line arguments and run the script."""
    if len(sys.argv) < 2:
        print("Usage: python add_description_to_games.py <input_json_file> [output_json_file]")
        print()
        print("Examples:")
        print("  python add_description_to_games.py switch_games.json")
        print("  python add_description_to_games.py switch_games.json switch_games_updated.json")
        print()
        print("If output_json_file is not provided, the input file will be updated")
        print("(with a .backup file created first)")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Process the file
    count = process_json_file(input_file, output_file)
    
    if count > 0:
        print("\n✓ Done!")
    else:
        print("\n✗ Failed to process file")
        sys.exit(1)


if __name__ == "__main__":
    main()
