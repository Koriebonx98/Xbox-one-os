# Add Description to Switch Games

This Python script automatically adds a blank "Description" field to all games in a Switch games JSON file.

## Requirements

- Python 3.6 or higher
- No external dependencies required (uses only standard library)

## Usage

### Basic Usage (Update file in-place with backup)

```bash
python add_description_to_games.py <input_json_file>
```

This will:
1. Create a backup of the original file (with `.backup` extension)
2. Add "Description" field to all game entries in the file
3. Update the original file with the modified data

**Example:**
```bash
python add_description_to_games.py switch_games.json
```

After running, you'll have:
- `switch_games.json` - Updated file with Description fields
- `switch_games.json.backup` - Original file backup

### Save to New File (Keep original unchanged)

```bash
python add_description_to_games.py <input_json_file> <output_json_file>
```

This will:
1. Read the input file
2. Add "Description" field to all game entries
3. Save the result to a new output file
4. Leave the original file unchanged

**Example:**
```bash
python add_description_to_games.py switch_games.json switch_games_with_descriptions.json
```

## Supported JSON Formats

The script automatically detects and handles various JSON structures:

### Array of Game Objects
```json
[
    {
        "Name": "Game 1",
        "Genre": "Action"
    },
    {
        "Name": "Game 2",
        "Genre": "RPG"
    }
]
```

### Nested Object Structure
```json
{
    "games": [
        {
            "title": "Game 1",
            "year": 2020
        }
    ]
}
```

### Any Depth of Nesting
The script recursively processes all levels of the JSON structure.

## How It Works

1. The script reads your JSON file
2. It searches for objects that look like game entries (have fields like "Name", "title", "GameName", etc.)
3. For each game entry found, it adds a `"Description": ""` field if it doesn't already exist
4. The modified data is written back to the file (or a new file)
5. A summary is displayed showing how many games were processed

## Game Detection

The script identifies game entries by looking for common field names:
- `Name` or `name`
- `Title` or `title`
- `GameName` or `game_name`

If an object contains any of these fields, it's considered a game entry and will get a Description field.

## Notes

- The Description field is set to an empty string `""` by default
- Existing Description fields are NOT overwritten
- The script maintains the original JSON formatting and structure
- UTF-8 encoding is used for all files
- Backup files are created with `.backup` extension

## Example Output

**Before:**
```json
[
    {
        "Name": "The Legend of Zelda: Breath of the Wild",
        "Genre": "Action-Adventure"
    }
]
```

**After:**
```json
[
    {
        "Name": "The Legend of Zelda: Breath of the Wild",
        "Genre": "Action-Adventure",
        "Description": ""
    }
]
```

## For 4000+ Games

The script is optimized to handle large JSON files with thousands of game entries. Processing time will vary based on:
- File size
- JSON structure complexity
- System performance

For a file with ~4000 games, expect processing to complete in a few seconds.

## Troubleshooting

### "File not found" error
Make sure the input file path is correct and the file exists.

### "Failed to parse JSON" error
The input file must be valid JSON. Check the file for syntax errors.

### Permission errors
Ensure you have read/write permissions for the files and directories.

## After Running the Script

Once the script completes:
1. The blank "Description" fields are ready for you to fill in
2. You can edit the JSON file and add descriptions manually
3. Or use another script/tool to populate the descriptions from a database or API
