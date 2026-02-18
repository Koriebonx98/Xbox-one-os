# Nintendo Switch Games Folder Organization

This system automatically creates folder structures for Nintendo Switch games based on their Title IDs.

## Overview

- **Switch.Games.json**: Contains the list of Nintendo Switch games with their Title IDs
- **setup_switch_folders.py**: Python script that reads the JSON and creates folders
- **Data/Nintendo - Switch/Games/$TitleID**: Generated folder structure for each game

## Usage

### Adding New Games

1. Edit `Switch.Games.json` and add new game entries:
```json
{
  "TitleID": "0100000000010000",
  "Name": "Game Name"
}
```

2. Run the setup script:
```bash
python3 setup_switch_folders.py
```

This will create a new folder at `Data/Nintendo - Switch/Games/{TitleID}` for each game.

## Title ID Format

Nintendo Switch Title IDs are 16-character hexadecimal strings (e.g., `0100000000010000`).

## Notes

- Empty directories are tracked in git using `.gitkeep` files
- The script will skip existing folders and only create new ones
- Each game folder is created under `Data/Nintendo - Switch/Games/`
