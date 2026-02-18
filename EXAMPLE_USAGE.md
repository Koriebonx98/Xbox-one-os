# Example: How to Use the Script with Switch Games JSON

## Step 1: Locate your Switch games JSON file

The script is designed to work with a JSON file containing Nintendo Switch games data. 
This file might be named something like:
- `switch_games.json`
- `nintendo_switch_games.json`
- Or any other name containing your game data

## Step 2: Run the script

### Option A: Update the file in place (recommended)
```bash
python add_description_to_games.py path/to/your/switch_games.json
```

This will:
- Create a backup: `switch_games.json.backup`
- Update the original file with Description fields

### Option B: Create a new file
```bash
python add_description_to_games.py path/to/your/switch_games.json path/to/output/switch_games_updated.json
```

This will:
- Leave the original file unchanged
- Create a new file with Description fields added

## Step 3: Verify the results

After running the script, you can:
1. Open the JSON file in any text editor
2. Look for the new "Description" field in each game entry
3. Start filling in the descriptions as needed

## Example Before and After

**Before:**
```json
[
    {
        "Name": "The Legend of Zelda: Breath of the Wild",
        "Platform": "Switch",
        "ReleaseYear": 2017
    }
]
```

**After:**
```json
[
    {
        "Name": "The Legend of Zelda: Breath of the Wild",
        "Platform": "Switch",
        "ReleaseYear": 2017,
        "Description": ""
    }
]
```

## For the Game-OS Project

If you're using this for the Game-OS project and have over 4000 Switch games:

1. Place your Switch games JSON file in the repository
2. Run: `python add_description_to_games.py <your_switch_games_file>.json`
3. The script will process all 4000+ games in seconds
4. You can then manually fill in the descriptions later

## Need Help?

See the full documentation in `README_ADD_DESCRIPTION.md` for more details, troubleshooting, and advanced usage.
