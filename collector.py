import json
import requests
import os

DATA_FILE = 'game_data.json'
API_URL = 'https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json'

# Fetch latest results from API
try:
    response = requests.get(API_URL)
    data = response.json()
except Exception as e:
    print("Error fetching API:", e)
    exit()

# Ensure expected structure
if 'list' not in data or not data['list']:
    print("No data found in API response.")
    exit()

latest = data['list'][0]

# Extract game info
record = {
    'period': latest['issue'],
    'color': latest['color'],  # Adjust based on actual key from your data
    'big_small': latest.get('bs', '')  # optional
}

# Load or create data file
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        try:
            game_data = json.load(f)
        except json.JSONDecodeError:
            game_data = []
else:
    game_data = []

# Avoid duplicates
if not any(r['period'] == record['period'] for r in game_data):
    game_data.append(record)
    print(f"✔ Added new record: {record}")
else:
    print("ℹ No new data.")

# Save updated list
with open(DATA_FILE, 'w') as f:
    json.dump(game_data, f, indent=2)
