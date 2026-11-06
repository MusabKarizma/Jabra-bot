

 import os
import threading
import time
import json
import urllib.request
from flask import Flask
from telegram.ext import Application, CommandHandler

BOT_TOKEN = os.environ.get("BOT_TOKEN")
app_flask = Flask(__name__)

def send(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = json.dumps({"chat_id": "YOUR_CHAT_ID", "text": msg, "parse_mode": "Markdown"}).encode()
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req, timeout=10)
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
    send("✅ *بوت جبرة شغال 24 ساعة يا زعيم* \nالسيرفر اشتغل")
    while True:
        try:
            buy = get_price()
            print(f"سعر البداية: {buy}")
            time.sleep(60)
        except Exception as e:
            print(e)
            time.sleep(10)

async def gold_cmd(update, context):
    await update.message.reply_text("ذهب")

async def euro_cmd(update, context):
    await update.message.reply_text("يورو")

def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("ذهب", gold_cmd))
    app.add_handler(CommandHandler("يورو", euro_cmd))
    app.run_polling()

if __name__ == '__main__':
    threading.Thread(target=bot_loop, daemon=True).start()
    threading.Thread(target=run_bot, daemon=True).start()
    app_flask.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

@app_flask.route('/')
def home():
    return "Bot Running"