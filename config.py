# config.py

# 🔧 تنظیمات کلی ربات DiceDux Trade

# حالت اجرا: "simulation" یا "real"
TRADE_MODE = "simulation"

# لیست ارزهایی که ربات روی آن‌ها کار می‌کند
SYMBOLS = ["BTCUSDT", "ETHUSDT", "DOGEUSDT"]

# تایم‌فریم تحلیل (دقیقه‌ای)
TIMEFRAME_MINUTES = 240  # یعنی 4 ساعته

# تنظیمات CoinEx API
COINEX_BASE_URL = "https://api.coinex.com/v2"
COINEX_KLINE_ENDPOINT = "/spot/kline"
COINEX_API_KEY = "F5498FB9C0A34C23B3FE704FE174105C"
COINEX_API_SECRET = "AA4173A9CE1E147E9B8725C2F8E3D987D95ED8AF095ECD16"

# مقدار سرمایه مجازی در حالت شبیه‌سازی (هر ارز)
INITIAL_BALANCE = 1000

# تعداد کندل گذشته برای تحلیل
CANDLE_HISTORY_LIMIT = 200
