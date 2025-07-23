# collector.py
import requests
import json
import os
from datetime import datetime

DATA_FILE = "game_data.json"
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_30S.json"

def fetch_latest_result():
    try:
        res = requests.get(API_URL)
        data = res.json()
        if not data or "data" not in data:
            print("No data fetched.")
            return

        latest = data["data"][0]
        period = latest.get("issue")
        color = latest.get("color")
        size = latest.get("size")

        # Load existing data
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                all_data = json.load(f)
        else:
            all_data = []

        if all_data and all_data[-1]["period"] == period:
            print("Already up to date.")
            return

        new_entry = {
            "period": period,
            "color": color,
            "size": size,
            "timestamp": datetime.now().isoformat()
        }

        all_data.append(new_entry)

        with open(DATA_FILE, "w") as f:
            json.dump(all_data, f, indent=2)

        print(f"✅ Fetched and saved period {period}")

    except Exception as e:
        print("❌ Error fetching data:", e)

fetch_latest_result()
