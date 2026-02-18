# Nintendo Switch Games Integration

This document describes how the Switch.Games.Json feature works in Game OS.

## Overview

The application automatically reads Nintendo Switch game metadata from `Data/Switch.Games.Json` and creates individual game files in the `Data/Nintendo - Switch/Games/` directory.

## File Structure

### Switch.Games.Json
Located at: `Data/Switch.Games.Json`

This JSON file contains an array of Nintendo Switch games with the following fields:
- `TitleID`: The unique 16-digit hexadecimal title ID for the game
- `Name`: The full name of the game
- `Genre`: The game's genre
- `Publisher`: The publisher of the game
- `ReleaseDate`: The release date in YYYY-MM-DD format

Example:
```json
[
  {
    "TitleID": "0100000000010000",
    "Name": "Super Mario Odyssey",
    "Genre": "Platform",
    "Publisher": "Nintendo",
    "ReleaseDate": "2017-10-27"
  }
]
```

### Generated Game Files
Location: `Data/Nintendo - Switch/Games/$TitleID`

For each game in Switch.Games.Json, a file is created with the Title ID as the filename. The file contains:
```
[Game Name]
Title ID: [TitleID]
Genre: [Genre]
Publisher: [Publisher]
Release Date: [ReleaseDate]
```

Example file `Data/Nintendo - Switch/Games/0100000000010000`:
```
Super Mario Odyssey
Title ID: 0100000000010000
Genre: Platform
Publisher: Nintendo
Release Date: 2017-10-27
```

## How It Works

1. When the Games/Apps page is initialized, the `SwitchGamesLoader.CreateGameFiles()` method is called
2. The loader reads `Data/Switch.Games.Json` and parses the game metadata
3. For each game, it creates a file named with the game's Title ID in `Data/Nintendo - Switch/Games/`
4. The file contains the game name and metadata in plain text format
5. Files are only created if they don't already exist (avoiding unnecessary I/O)
6. The process runs on a background thread to avoid blocking the UI

## Adding New Games

To add new Nintendo Switch games:

1. Edit `Data/Switch.Games.Json`
2. Add a new game entry with the required fields (TitleID, Name, Genre, Publisher, ReleaseDate)
3. Save the file
4. The next time the application loads the Games/Apps page, the new game file will be created automatically

## Code Components

- **SwitchGamesLoader.cs**: Utility class that handles reading the JSON and creating game files
  - `LoadSwitchGames()`: Reads and deserializes Switch.Games.Json
  - `CreateGameFiles()`: Creates game files on a background thread
  - `CreateGameFilesInternal()`: Internal method that performs the file creation

- **GamesAppsPage.xaml.cs**: Integrated to call the loader during initialization

## Performance Notes

- File creation runs asynchronously on a background thread to prevent UI freezing
- Files are only created if they don't exist, avoiding redundant writes
- The loader gracefully handles missing files and parse errors
