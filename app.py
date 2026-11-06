import os
import threading
import time
import json
import urllib.request
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID", "") # لو ما عندك خليه فاضي
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Jabra Bot Live ✅"

# ========== 1. دالة الارسال ==========
def send(msg):
    try:
        if not CHAT_ID: return
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = json.dumps({"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}).encode()
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(e)

def get_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    with urllib.request.urlopen(url, timeout=10) as r:
        return float(json.loads(r.read().decode())['price'])

def bot_loop():
    time.sleep(5)
    try:
        send("✅ *بوت جبرة شغال 24 ساعة يا زعيم*\nالسيرفر اشتغل")
    except: pass
    while True:
        try:
            p = get_price()
            print(f"BTC: {p}")
            time.sleep(60)
        except Exception as e:
            print(e)
            time.sleep(10)

# ========== 2. الهاندلرات مفصولة براها ==========
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلا يا زعيم 🔥\nالبوت شغال فل\nجرب:\n/ذهب\n/يورو\nذهب")

async def gold_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        price = get_price()
        await update.message.reply_text(f"💰 BTC الآن: {price}")
    except:
        await update.message.reply_text("سعر الذهب...")

async def euro_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💶 سعر اليورو...")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.strip()
    if "ذهب" in txt:
        await gold_cmd(update, context)
    elif "يورو" in txt:
        await euro_cmd(update, context)
    else:
        await start_cmd(update, context)

# ========== 3. الرن بوت مفصول براهو ==========
def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    # اوامر بالسلاش
    app.add_handler(CommandHandler("start", start_cmd))
    def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    # امر انجليزي فقط
    app.add_handler(CommandHandler("start", start_cmd))
    
    # اي كلام عربي - نستقبلو كرسالة عادية
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    print("Bot polling started...")
    app.run_polling()
    # كلام عادي بدون سلاش
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    print("Bot polling started...")
    app.run_polling()

# ========== 4. التشغيل الرئيسي - ده الصح ==========
def start_flask():
    app_flask.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

if __name__ == '__main__':
    # شغل Flask في ثريد جانبي
    threading.Thread(target=start_flask, daemon=True).start()
    # شغل البوت لووب جانبي
    threading.Thread(target=bot_loop, daemon=True).start()
    
    # شغل بوت التيليجرام في الرئيسي - لازم يكون في الرئيسي!
    print("Starting Telegram bot...")
    run_bot()