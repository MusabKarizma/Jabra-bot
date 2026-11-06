import os, threading, yfinance as yf
import pandas as pd
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import ta

BOT_TOKEN = os.getenv("BOT_TOKEN")
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Jabra Signals Bot Live - Gold & EURUSD 🚀"

def analyze_pair(symbol="XAUUSD"):
    yf_symbol = "GC=F" if "XAU" in symbol else "EURUSD=X"
    try:
        data = yf.download(yf_symbol, period="5d", interval="1h", progress=False)
        close = data['Close']
        rsi = float(ta.momentum.RSIIndicator(close).rsi().iloc[-1])
        ema50 = float(ta.trend.EMAIndicator(close, 50).ema_indicator().iloc[-1])
        ema200 = float(ta.trend.EMAIndicator(close, 200).ema_indicator().iloc[-1])
        macd = ta.trend.MACD(close)
        macd_line = float(macd.macd().iloc[-1])
        macd_sig = float(macd.macd_signal().iloc[-1])
        price = float(close.iloc[-1])
        trend = "صاعد 📈" if ema50 > ema200 else "هابط 📉"
        score = 0
        if rsi < 35: score+=2
        elif rsi < 50: score+=1
        if ema50 > ema200: score+=1
        if macd_line > macd_sig: score+=1
        if score >=3: dec="🟢 شراء قوي"
        elif score==2: dec="🟡 شراء حذر"
        elif rsi>70: dec="🔴 تشبع شرائي - انتظر"
        else: dec="⚠️ انتظار"
        return f"🔍 {symbol}\nالسعر: {price:.2f}\nالاتجاه: {trend}\nRSI: {rsi:.1f}\nMACD: {'شراء' if macd_line>macd_sig else 'بيع'}\n\n💡 {dec}"
    except Exception as e:
        return f"خطأ: {e}"

async def start(update, context):
    await update.message.reply_text("أهلا! 👋\n/ذهب لتحليل الذهب\n/يورو لتحليل اليورو\n/تحليل XAUUSD")

async def gold_cmd(update, context):
    await update.message.reply_text("⏳ بحلل الذهب...")
    await update.message.reply_text(analyze_pair("XAUUSD"))

async def euro_cmd(update, context):
    await update.message.reply_text("⏳ بحلل اليورو...")
    await update.message.reply_text(analyze_pair("EURUSD"))

def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ذهب", gold_cmd))
    app.add_handler(CommandHandler("يورو", euro_cmd))
    app.run_polling()

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    app_flask.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))(url, data=data, timeout=10)
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
