# predict.py
import json, os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

DATA_FILE = "game_data.json"

# Map color to number
color_map = {
    "red": 0,
    "green": 1,
    "green,violet": 2,
    "red,violet": 3,
    "violet": 4
}

def clean_color(c):
    return c.strip().lower() if c else ""

def load_data():
    if not os.path.exists(DATA_FILE):
        print("No data found.")
        return pd.DataFrame()

    with open(DATA_FILE, "r") as f:
        lines = f.readlines()
        data = [json.loads(l) for l in lines if l.strip()]
        for d in data:
            d["color"] = clean_color(d.get("color", ""))
        return pd.DataFrame(data)

def prepare_model(df):
    df = df[df["color"].isin(color_map)]
    df["color_num"] = df["color"].map(color_map)
    df["number"] = pd.to_numeric(df["number"], errors="coerce")
    df = df.dropna()

    # Create features from past N rounds
    N = 5
    for i in range(1, N + 1):
        df[f"color_num_{i}"] = df["color_num"].shift(i)
        df[f"number_{i}"] = df["number"].shift(i)

    df = df.dropna()

    features = [col for col in df.columns if col.startswith("color_num_") or col.startswith("number_")]
    X = df[features]
    y = df["color_num"]

    return train_test_split(X, y, test_size=0.1, random_state=42), df

def predict_next():
    df = load_data()
    if df.empty:
        print("No data to train on.")
        return

    (X_train, X_test, y_train, y_test), df_cleaned = prepare_model(df)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Use last N rows for prediction
    last = df_cleaned.tail(5)
    predict_input = {}

    for i in range(1, 6):
        predict_input[f"color_num_{i}"] = color_map.get(clean_color(last.iloc[-i]["color"]), 0)
        predict_input[f"number_{i}"] = float(last.iloc[-i]["number"])

    X_pred = pd.DataFrame([predict_input])
    pred = model.predict(X_pred)[0]

    inverse_color_map = {v: k for k, v in color_map.items()}
    next_period = str(int(df_cleaned["period"].max()) + 1)

    print("\n=== Prediction Result ===")
    print(f"Next Period    : {next_period}")
    print(f"Predicted Color: {inverse_color_map[pred]}")

if __name__ == "__main__":
    predict_next()
