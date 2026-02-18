#!/usr/bin/env python3
"""
Script to create folder structure for Nintendo Switch games based on Switch.Games.json
"""
import json
import os
import sys

def create_switch_game_folders():
    """Read Switch.Games.json and create folders for each TitleID"""
    
    # Get the script directory (repository root)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the Switch.Games.json file
    json_file_path = os.path.join(script_dir, "Switch.Games.json")
    
    # Check if the JSON file exists
    if not os.path.exists(json_file_path):
        print(f"Error: Switch.Games.json not found at {json_file_path}")
        sys.exit(1)
    
    # Read the JSON file
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            games = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        sys.exit(1)
    
    # Base directory for Switch games
    base_dir = os.path.join(script_dir, "Data", "Nintendo - Switch", "Games")
    
    # Create the base directory if it doesn't exist
    os.makedirs(base_dir, exist_ok=True)
    print(f"Base directory: {base_dir}")
    
    # Create folders for each TitleID
    created_count = 0
    for game in games:
        if 'TitleID' not in game:
            print(f"Warning: Game entry missing TitleID: {game}")
            continue
        
        title_id = game['TitleID']
        game_name = game.get('Name', 'Unknown')
        folder_path = os.path.join(base_dir, title_id)
        
        # Create the folder
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)
            print(f"Created folder for {game_name}: {title_id}")
            created_count += 1
        else:
            print(f"Folder already exists for {game_name}: {title_id}")
    
    print(f"\nTotal folders created: {created_count}")
    print(f"Total games in JSON: {len(games)}")

if __name__ == "__main__":
    create_switch_game_folders()
