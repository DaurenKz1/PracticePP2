import json
import os

LEADERBOARD_FILE = "leaderboard.json"
SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "red",       # "red", "blue", "green"
    "difficulty": "normal"    # "easy", "normal", "hard"
}



def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return []


def save_leaderboard(entries: list):
    """entries = list of dicts: {name, score, distance, coins}"""
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(entries, f, indent=2)


def add_leaderboard_entry(name: str, score: int, distance: int, coins: int):
    entries = load_leaderboard()
    entries.append({"name": name, "score": score,
                    "distance": distance, "coins": coins})
    entries.sort(key=lambda e: e["score"], reverse=True)
    entries = entries[:10]          # keep top 10
    save_leaderboard(entries)
    return entries



def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
            for k, v in DEFAULT_SETTINGS.items():
                data.setdefault(k, v)
            return data
        except Exception:
            pass
    return dict(DEFAULT_SETTINGS)


def save_settings(settings: dict):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)