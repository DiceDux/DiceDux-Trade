
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

with open("models/model.pkl", "rb") as f:
    model = pickle.load(f)

def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["rsi"] = df["close"].diff().apply(lambda x: x if x > 0 else 0).rolling(14).mean()
    df["ema20"] = df["close"].ewm(span=20).mean()
    df["ch"] = df["high"] - df["low"]
    df["atr"] = df["ch"].rolling(14).mean()
    df = df.dropna()
    return df

def predict_signal_from_model(df, verbose=False):
    df = extract_features(df)
    latest = df[["rsi", "ema20", "ch", "atr", "volume"]].tail(1)
    prediction = model.predict(latest)[0]
    confidence = max(model.predict_proba(latest)[0])

    action = "BUY" if prediction == 1 else "SELL"

    if verbose:
        print("🧠 ویژگی‌های ورودی مدل:")
        print(latest)
        print(f"📢 تصمیم مدل: {action} | اعتماد: {round(confidence, 2)}")

    return {
        "action": action,
        "confidence": round(confidence, 2),
        "price": float(df["close"].iloc[-1]),
        "features": latest.to_json(orient="records")
    }
