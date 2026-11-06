from flask import Flask
import threading, time, json, urllib.request, os

app = Flask(__name__)

# ===== غير ديل بس =====
TOKEN = "9093669107:AAHD39rNMs-r39ESOI8VlwmwGqp-QydmEYU"
CHAT_ID = "8711298563"
# =======================

def send(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = f"chat_id={CHAT_ID}&text={msg}&parse_mode=Markdown".encode()
        urllib.request.urlopen(url, data=data, timeout=10)
        print(f"رسلنا: {msg}")
    except Exception as e:
        print(e)

def get_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    with urllib.request.urlopen(url, timeout=10) as r:
        data = json.loads(r.read().decode())
        return float(data['price'])

def bot_loop():
    time.sleep(5)
    send("✅ *بوت جبرة شغال 24 ساعة يا زعيم!* \nالسيرفر اشتغل")
    buy = get_price()
    print(f"سعر البداية: {buy}")
    
    while True:
        try:
            price = get_price()
            print(f"فحص: {price}")
            if price >= buy * 1.02:
                send(f"🔴 *بيع الآن* - ربح 2%\nالسعر: ${price:.2f}\nسعر الشراء كان: ${buy:.2f}")
                buy = price
            elif price <= buy * 0.98:
                send(f"🟢 *شراء الآن* - نزول 2%\nالسعر: ${price:.2f}")
                buy = price
            time.sleep(300) # يفحص كل 5 دقائق
        except Exception as e:
            print(f"خطأ: {e}")
            time.sleep(60)

# موقع صغير عشان Render ما ينوم البوت
@app.route('/')
def home():
    return "بوت جبرة شغال 24 ساعة ✅"

# شغل البوت في الخلفية
threading.Thread(target=bot_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
