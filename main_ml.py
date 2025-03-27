import time
from ai.ai_model_runner import predict_signal_from_model
from trading.simulator import execute_trade
from data.price_fetcher import get_candle_data
from db.db_handler import insert_trade, update_balance
import traceback

SYMBOLS = ["BTCUSDT", "ETHUSDT", "DOGEUSDT"]
INTERVAL = "4h"

def run_with_ml():
    print("🚀 DiceDux ML در حال اجرا با مدل یادگیرنده...\n")

    for symbol in SYMBOLS:
        print(f"\n📌 شروع تحلیل برای: {symbol}")
        try:
            df = get_candle_data(symbol, INTERVAL)
            print("✅ دیتا دریافت شد.")

            if df is None or len(df) < 200:
                print(f"⚠️ داده کافی نیست: {len(df) if df is not None else 'None'}")
                continue

            print("🧠 ارسال به مدل برای پیش‌بینی...")
            result = predict_signal_from_model(df, verbose=True)
            print("✅ پیش‌بینی انجام شد.")

            action = result['action']
            confidence = result['confidence']
            price = result['price']
            features = result['features']

            print("📝 تلاش برای ذخیره در دیتابیس...")
            features_str = str(features)  # 👈 اضافه کن
            insert_trade(symbol, action, price, confidence, features_str)
            print("✅ ذخیره در دیتابیس موفق بود.")

            print("▶ تلاش برای اجرای ترید شبیه‌سازی...")
            new_balance = execute_trade(symbol, action, price)
            print(f"✅ ترید شبیه‌سازی موفق | موجودی: {new_balance}")

            print("💾 تلاش برای آپدیت موجودی...")
            update_balance(symbol, new_balance)
            print("✅ موجودی آپدیت شد.")

        except Exception as e:
            print(f"❌ خطای اصلی در تحلیل {symbol}: {e}")
            traceback.print_exc()

        print("🧪 پایان تحلیل این ارز.\n")


if __name__ == "__main__":
    print("✅ وارد حلقه اصلی شدم...")
    try:
        while True:
            print("🔄 شروع یک دور جدید تحلیل...")
            run_with_ml()
            print("✅ تمام ارزها بررسی شدند. 🎯")
            print("🕒 در حال انتظار برای دور بعدی تحلیل...\n")
            time.sleep(60 * 5)
    except KeyboardInterrupt:
        print("⛔ اجرای ربات با دستور دستی متوقف شد.")
