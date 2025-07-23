# collector.py
import requests, time, json, os

DATA_FILE = "game_data.json"
HISTORY_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"
fetched_periods = set()

# Create file if doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f: pass

def fetch_and_store():
    while True:
        try:
            resp = requests.get(HISTORY_URL)
            data = resp.json()
            results = data.get("data", {}).get("list", [])
            new_entries = []

            for item in results:
                period = item.get("issueNumber")
                number = item.get("number")
                color = item.get("color")

                if not period or period in fetched_periods:
                    continue

                entry = {
                    "period": period,
                    "color": color,
                    "number": number
                }

                fetched_periods.add(period)
                new_entries.append(entry)

            if new_entries:
                with open(DATA_FILE, "a") as f:
                    for r in new_entries:
                        f.write(json.dumps(r) + "\n")
                        print(f"[+]{r['period']} - {r['color']}")

            else:
                print("No new data.")

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(30)

if __name__ == "__main__":
    fetch_and_store()
