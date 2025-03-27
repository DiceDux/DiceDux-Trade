
import requests
import pandas as pd
from config import COINEX_BASE_URL, COINEX_KLINE_ENDPOINT, CANDLE_HISTORY_LIMIT, TIMEFRAME_MINUTES

def convert_timeframe(minutes: int) -> str:
    mapping = {
        1: "1min", 3: "3min", 5: "5min", 15: "15min", 30: "30min",
        60: "1hour", 120: "2hour", 240: "4hour", 360: "6hour",
        720: "12hour", 1440: "1day"
    }
    return mapping.get(minutes, "4hour")

def get_candle_data(symbol: str, interval: str = "4h") -> pd.DataFrame:
    try:
        url = f"{COINEX_BASE_URL}{COINEX_KLINE_ENDPOINT}"
        params = {
            "market": symbol,
            "period": convert_timeframe(TIMEFRAME_MINUTES),
            "limit": CANDLE_HISTORY_LIMIT
        }
        response = requests.get(url, params=params)
        print(f"🔍 پاسخ API برای {symbol}:\n{response.status_code} | {response.text[:200]}")

        result = response.json()
        if result.get("code") != 0 or "data" not in result:
            print(f"⚠️ پاسخ نامعتبر از API برای {symbol}: {result}")
            return pd.DataFrame()

        rows = result["data"]
        df = pd.DataFrame(rows)
        df["timestamp"] = pd.to_datetime(df["created_at"], unit="ms")
        df = df.rename(columns={
            "open": "open",
            "close": "close",
            "high": "high",
            "low": "low",
            "volume": "volume"
        })

        df = df[["timestamp", "open", "high", "low", "close", "volume"]]
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
        return df

    except Exception as e:
        print(f"❌ خطا در دریافت داده کندل: {e}")
        return pd.DataFrame()
