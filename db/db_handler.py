
import mysql.connector
from datetime import datetime

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'asdJWefnk23@$Jn3235dc',
    'database': 'dicedux_db'
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def insert_trade(symbol, action, entry_price, confidence, features):
    print(f"📥 [insert_trade] شروع درج ترید برای {symbol}")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO trades (symbol, action, entry_price, confidence, entry_time, features)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        now = datetime.utcnow()
        features_str = str(features)  # 👈 تبدیل به رشته
        print("📦 مقدار features برای درج:\n", features_str)
        cursor.execute(sql, (symbol, action, entry_price, confidence, now, features_str))
        conn.commit()
        print("✅ [insert_trade] ترید ذخیره شد.")
    except Exception as e:
        print(f"❌ [insert_trade] خطا در ذخیره ترید: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        if conn.is_connected():
            conn.close()
            print("🧹 [insert_trade] اتصال دیتابیس بسته شد.")

def close_trade(trade_id, exit_price, profit):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE trades
        SET exit_price = %s, profit_usdt = %s, exit_time = %s, status = 'CLOSED'
        WHERE id = %s
    """
    now = datetime.utcnow()
    cursor.execute(sql, (exit_price, profit, now, trade_id))
    conn.commit()
    conn.close()

def update_balance(symbol, balance, open_position=False, open_price=None):
    print(f"⚙️ [db] آپدیت موجودی | symbol={symbol}, balance={balance}, position={open_position}, price={open_price}")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO balances (symbol, balance, open_position, open_price)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                balance = VALUES(balance),
                open_position = VALUES(open_position),
                open_price = VALUES(open_price)
        """
        cursor.execute(sql, (symbol, balance, open_position, open_price))
        conn.commit()
        print("✅ موجودی در دیتابیس ذخیره شد.")
    except Exception as e:
        print(f"❌ خطا در update_balance: {e}")
        raise
    finally:
        if conn.is_connected():
            conn.close()
