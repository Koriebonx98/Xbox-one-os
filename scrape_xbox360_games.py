#!/usr/bin/env python3
"""
Script to scrape cover images for Xbox 360 games using the SteamGridDB API.
Reads Xbox 360.Games.json, creates a directory for each game under
Data/Game Cover/Microsoft - Xbox 360/<GameTitle>/, downloads the cover
image as Cover.png/jpg into that directory, and updates the 'image' field
in the JSON with the local file path.

Only processes games whose 'image' field is blank — skips any game that
already has a cover path recorded.  If no cover can be found on SteamGridDB
for a particular game the entry is left with an empty 'image' field so it
can be retried on the next run.

Requires internet access to reach api.steamgriddb.com.

A log file (scrape_xbox360_games.log) is written alongside console output
so every step is recorded for later inspection.
"""

import json
import logging
import os
import sys
import time
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Logging setup — writes to both stdout and a log file
# ---------------------------------------------------------------------------
LOG_FILE = "scrape_xbox360_games.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)

# SteamGridDB API configuration
# Set the STEAMGRIDDB_API_KEY environment variable before running.
# A free API key can be obtained from https://www.steamgriddb.com/profile/preferences/api
STEAMGRIDDB_API_KEY = os.environ.get("STEAMGRIDDB_API_KEY", "")
STEAMGRIDDB_BASE_URL = "https://www.steamgriddb.com/api/v2"

# Delay between API requests to respect rate limits (seconds)
REQUEST_DELAY = 0.3

# Input / output files
XBOX360_JSON_FILE = "Xbox 360.Games.json"

# Directory where per-game cover folders are created (matches Game-OS convention)
GAMES_BASE_DIR = Path("Data/Game Cover/Microsoft - Xbox 360")


def steamgriddb_headers():
    """Return the authentication headers required by SteamGridDB."""
    return {"Authorization": f"Bearer {STEAMGRIDDB_API_KEY}"}


def search_game(game_title):
    """
    Search SteamGridDB for a game by title.

    Returns the first matching game's ID, or None if nothing is found.
    """
    url = f"{STEAMGRIDDB_BASE_URL}/search/autocomplete/{requests.utils.quote(game_title)}"
    try:
        response = requests.get(url, headers=steamgriddb_headers(), timeout=15)
        response.raise_for_status()
        data = response.json()
        if data.get("success") and data.get("data"):
            return data["data"][0]["id"]
    except requests.exceptions.RequestException as exc:
        log.warning("Search request failed for '%s': %s", game_title, exc)
    except (KeyError, ValueError) as exc:
        log.warning("Unexpected search response for '%s': %s", game_title, exc)
    return None


def get_cover_url(game_id):
    """
    Fetch the best available cover (grid image) for a SteamGridDB game ID.

    Tries portrait covers (600x900) first, then falls back to any available grid.
    Returns a URL string, or an empty string if nothing is found.
    """
    # Prefer portrait/box-art style grids
    for dimensions in ("600x900", "342x482", "660x930"):
        url = f"{STEAMGRIDDB_BASE_URL}/grids/game/{game_id}"
        params = {"dimensions": dimensions, "limit": 1}
        try:
            response = requests.get(
                url, headers=steamgriddb_headers(), params=params, timeout=15
            )
            response.raise_for_status()
            data = response.json()
            if data.get("success") and data.get("data"):
                return data["data"][0]["url"]
        except requests.exceptions.RequestException as exc:
            log.warning("Grid request failed (game_id=%s): %s", game_id, exc)
            break
        except (KeyError, ValueError):
            pass

    # Final fallback: any grid without dimension filter
    url = f"{STEAMGRIDDB_BASE_URL}/grids/game/{game_id}"
    try:
        response = requests.get(
            url, headers=steamgriddb_headers(), params={"limit": 1}, timeout=15
        )
        response.raise_for_status()
        data = response.json()
        if data.get("success") and data.get("data"):
            return data["data"][0]["url"]
    except requests.exceptions.RequestException as exc:
        log.warning("Fallback grid request failed (game_id=%s): %s", game_id, exc)
    except (KeyError, ValueError):
        pass

    return ""


def sanitize_dirname(name):
    """Replace characters that are invalid in directory names with a dash."""
    invalid = r'\/:*?"<>|'
    for ch in invalid:
        name = name.replace(ch, "-")
    return name.strip(". ")


def create_game_directory(game_title):
    """
    Create the Data/Game Cover/Microsoft - Xbox 360/<GameTitle>/ directory.
    The title is sanitized to remove characters that are invalid in path names.
    Returns the Path object for the directory.
    """
    game_dir = GAMES_BASE_DIR / sanitize_dirname(game_title)
    try:
        game_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        log.warning("Could not create directory for '%s': %s", game_title, exc)
    return game_dir


def download_cover(cover_url, game_dir):
    """
    Download a cover image from cover_url and save it into game_dir.

    The filename is Cover.png, Cover.jpg, or Cover.webp based on the
    Content-Type header returned by the server.

    Returns the local path string (relative to the repo root) on success,
    or an empty string if the download fails.
    """
    ext_map = {
        "image/png": ".png",
        "image/jpeg": ".jpg",
        "image/jpg": ".jpg",
        "image/webp": ".webp",
    }
    try:
        response = requests.get(cover_url, timeout=30, stream=True)
        response.raise_for_status()
        content_type = response.headers.get("Content-Type", "").split(";")[0].strip().lower()
        ext = ext_map.get(content_type, ".png")
        cover_file = game_dir / f"Cover{ext}"
        with open(cover_file, "wb") as fh:
            for chunk in response.iter_content(chunk_size=8192):
                fh.write(chunk)
        return str(cover_file)
    except requests.exceptions.RequestException as exc:
        log.warning("Failed to download cover from %s: %s", cover_url, exc)
    except OSError as exc:
        log.warning("Failed to save cover to %s: %s", game_dir, exc)
    return ""


def main():
    """Main entry point."""
    log.info("=== Xbox 360 cover scraper started ===")
    log.info("Log file: %s", Path(LOG_FILE).resolve())

    if not STEAMGRIDDB_API_KEY:
        log.error(
            "STEAMGRIDDB_API_KEY environment variable is not set. "
            "Get a free API key at https://www.steamgriddb.com/profile/preferences/api"
        )
        return 1

    # Load the Xbox 360 games JSON
    json_path = Path(XBOX360_JSON_FILE)
    if not json_path.exists():
        log.error("%s not found.", XBOX360_JSON_FILE)
        return 1

    with open(json_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    games = data.get("games", [])
    if not games:
        log.error("No games found in JSON.")
        return 1

    total = len(games)
    log.info("Loaded %d Xbox 360 games from %s", total, XBOX360_JSON_FILE)
    log.info("Saving covers under %s ...", GAMES_BASE_DIR)

    updated = 0
    skipped = 0
    no_match = 0
    failed_downloads = 0
    save_interval = 50  # persist JSON progress every N successful downloads

    for idx, game in enumerate(games, start=1):
        game_title = game.get("title", "").strip()

        if not game_title:
            log.warning("[%d/%d] Skipping entry with missing title", idx, total)
            skipped += 1
            continue

        # Already has a cover — keep it
        existing_image = game.get("image", "")
        if existing_image and json_path.parent.joinpath(existing_image).resolve().exists():
            log.debug(
                "[%d/%d] %s — local cover already exists, skipping",
                idx, total, game_title,
            )
            skipped += 1
            continue

        log.info("[%d/%d] Processing: %s", idx, total, game_title)

        # Search SteamGridDB for the game
        sgdb_id = search_game(game_title)
        time.sleep(REQUEST_DELAY)

        if sgdb_id is None:
            log.info("  -> No match found on SteamGridDB for '%s'", game_title)
            # Leave image blank so the game can be retried next run
            no_match += 1
            continue

        log.info("  -> SteamGridDB game_id=%s, fetching cover...", sgdb_id)

        # Fetch the cover URL
        cover_url = get_cover_url(sgdb_id)
        time.sleep(REQUEST_DELAY)

        if cover_url:
            log.info("  -> Cover URL: %s", cover_url)
            # Create the per-game directory only once we have a cover to save
            game_dir = create_game_directory(game_title)
            local_path = download_cover(cover_url, game_dir)
            if local_path:
                game["image"] = local_path
                log.info("  -> Cover saved: %s", local_path)
                updated += 1
                # Periodically persist progress so a crash loses at most save_interval entries
                if updated % save_interval == 0:
                    with open(json_path, "w", encoding="utf-8") as fh:
                        json.dump(data, fh, indent=2, ensure_ascii=False)
                    log.info("  [checkpoint] Saved progress (%d covers so far)", updated)
            else:
                log.warning("  -> Cover download failed, will retry next run")
                failed_downloads += 1
        else:
            log.info("  -> No cover image available (game_id=%s)", sgdb_id)
            no_match += 1

    # Save the updated JSON
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)

    log.info("=== Scrape complete ===")
    log.info("  Total games      : %d", total)
    log.info("  Covers downloaded: %d", updated)
    log.info("  Download failures: %d", failed_downloads)
    log.info("  No API match     : %d", no_match)
    log.info("  Skipped          : %d", skipped)
    log.info("  Saved to         : %s", XBOX360_JSON_FILE)
    log.info("  Log written      : %s", LOG_FILE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
