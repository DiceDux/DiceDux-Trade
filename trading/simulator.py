# trading/simulator.py

import json
import os
from config import INITIAL_BALANCE

SIM_FILE = "simulation_trades.json"

if not os.path.exists(SIM_FILE):
    with open(SIM_FILE, "w") as f:
        json.dump({"balances": {}, "trades": []}, f, indent=4)
        

def load_state():
    print("📂 شروع اجرای load_state() ...")
    with open(SIM_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    print("📂 باز کردن فایل simulation_trades.json ...")
    with open(SIM_FILE, "w") as f:
        json.dump(state, f, indent=4)

def execute_trade(symbol: str, action: str, price: float):
    print("📂 بررسی وجود فایل simulation_trades.json ...")
    print(f"✅ مسیر فایل: {os.path.abspath(SIM_FILE)}")
    print(f"✅ فایل موجوده؟ {os.path.exists(SIM_FILE)}")
    print(f"⚙️ [simulate] شروع ترید | symbol={symbol}, action={action}, price={price}")

    try:
        state = load_state()
        balances = state["balances"]
        trades = state["trades"]

        if symbol not in balances:
            balances[symbol] = INITIAL_BALANCE
            print(f"💰 موجودی اولیه تنظیم شد: {INITIAL_BALANCE}")

        if action == "buy":
            trades.append({"symbol": symbol, "action": "buy", "price": price})
            print("🛒 ثبت خرید در لیست معاملات")
        elif action == "sell":
            last_buy = next((t for t in reversed(trades) if t["symbol"] == symbol and t["action"] == "buy"), None)
            if last_buy:
                profit = (price - last_buy["price"]) / last_buy["price"]
                balances[symbol] *= (1 + profit)
                trades.append({
                    "symbol": symbol,
                    "action": "sell",
                    "price": price,
                    "profit_%": round(profit * 100, 2),
                    "new_balance": round(balances[symbol], 2)
                })
                print(f"💸 فروش انجام شد | سود: {round(profit * 100, 2)}%")
            else:
                trades.append({
                    "symbol": symbol,
                    "action": "sell",
                    "price": price,
                    "warning": "no previous buy found"
                })
                print("⚠️ فروش بدون خرید قبلی انجام شد")

        state["balances"] = balances
        state["trades"] = trades
        save_state(state)
        print(f"✅ ترید ذخیره شد | موجودی: {round(balances[symbol], 2)}")

        return round(balances[symbol], 2)

    except Exception as e:
        print(f"❌ خطا در execute_trade: {e}")
        raise
