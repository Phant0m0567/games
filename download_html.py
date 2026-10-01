import json
import re
import sys
import time
from collections import Counter
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
ZONES_FILE = ROOT / "zones.json"
HTML_BASE = "https://cdn.jsdelivr.net/gh/freebuisness/html@main"
TOKEN = "{HTML_URL}"


def safe_folder_name(name):
    folder = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name).strip(" .")
    return folder or "game"


def load_games():
    games = json.loads(ZONES_FILE.read_text(encoding="utf-8"))
    games = [
        game
        for game in games
        if isinstance(game.get("id"), int)
        and game["id"] >= 0
        and isinstance(game.get("name"), str)
        and TOKEN in game.get("url", "")
    ]
    folder_names = [safe_folder_name(game["name"]) for game in games]
    folder_counts = Counter(folder_names)

    for game, folder in zip(games, folder_names):
        if folder_counts[folder] > 1:
            folder = f"{folder} ({game['id']})"
        game["_folder"] = folder
        game["_url"] = game["url"].strip().replace(TOKEN, HTML_BASE, 1)
    return games


def fetch(url):
    request = Request(url, headers={"User-Agent": "games-asset-downloader/1.0"})
    for attempt in range(3):
        try:
            with urlopen(request, timeout=60) as response:
                return response.read()
        except (URLError, TimeoutError) as error:
            if attempt == 2:
                raise error
            time.sleep(2**attempt)


def main():
    games = load_games()
    failed = []

    for index, game in enumerate(games, start=1):
        destination = ROOT / game["_folder"] / "index.html"
        source_name = Path(urlparse(game["_url"]).path).name
        if not source_name:
            failed.append((game["id"], "empty HTML URL path"))
            continue

        try:
            content = fetch(game["_url"])
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
            print(f"[{index}/{len(games)}] {game['name']} ({source_name})")
        except (OSError, URLError, TimeoutError) as error:
            failed.append((game["id"], str(error)))
            print(f"[{index}/{len(games)}] FAILED {game['name']}: {error}", file=sys.stderr)

    print(f"Downloaded {len(games) - len(failed)}/{len(games)} HTML files.")
    if failed:
        print(f"Failed IDs: {', '.join(str(game_id) for game_id, _ in failed)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())