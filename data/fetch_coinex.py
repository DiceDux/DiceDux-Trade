import requests
import pandas as pd
from datetime import datetime
from config import COINEX_BASE_URL, CANDLE_HISTORY_LIMIT, TIMEFRAME_MINUTES

def convert_timeframe(minutes: int) -> str:
    mapping = {
        1: "1min", 3: "3min", 5: "5min", 15: "15min", 30: "30min",
        60: "1hour", 120: "2hour", 240: "4hour", 360: "6hour",
        720: "12hour", 1440: "1day"
    }
    return mapping.get(minutes, "4hour")

def fetch_candles(symbol: str):
    url = f"{COINEX_BASE_URL}/spot/kline"
    period = convert_timeframe(TIMEFRAME_MINUTES)

    params = {
        "market": symbol.upper(),
        "period": period,
        "limit": CANDLE_HISTORY_LIMIT
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        # ✅ بررسی اولیه وضعیت HTTP
        if response.status_code != 200:
            print(f"❌ پاسخ HTTP نامعتبر برای {symbol}: {response.status_code}")
            return pd.DataFrame()

        # ✅ بررسی محتوا قبل از json()
        if not response.text.strip().startswith("{"):
            print(f"❌ پاسخ متنی نامعتبر برای {symbol}: {response.text[:100]}")
            return pd.DataFrame()

        result = response.json()

        if result.get("code") != 0 or not result.get("data"):
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
        print(f"❌ خطا در دریافت داده برای {symbol}: {e}")
        return pd.DataFrame()
