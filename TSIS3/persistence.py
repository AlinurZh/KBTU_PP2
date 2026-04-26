import json 
import os 

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

def load_settings():
    default_settings = {
        "sound": True,
        "car_color": "blue",
        "difficulty": "normal"
    }
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    
    save_settings(default_settings)
    return default_settings

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as file:
            return json.load(file)
    
    return []

def save_score(name, score, distance):
    leaderboard = load_leaderboard()

    leaderboard.append({
        "name": name,
        "score": score,
        "distance": int(distance)
    })

    leaderboard = sorted(
        leaderboard,
        key=lambda item: item["score"],
        reverse=True
    )

    leaderboard[:10]

    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(leaderboard, file, indent=4)