# check.py
import os

DATA_FILE = "game_data.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        print("✅ game_data.json created.")
else:
    print("✅ game_data.json already exists.")
