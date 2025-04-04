import os
import threading
import logging
from http.server import SimpleHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# إعداد التوكن
TOKEN = os.getenv("TOKEN")

# تشغيل بوت تيليغرام
def start(update: Update, context: CallbackContext):
    update.message.reply_text("مرحبًا! اختر خيارًا:\n1️⃣ الدعم الفني\n2️⃣ تتبع الطلب\n3️⃣ الاتصال بنا")

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "1":
        update.message.reply_text("✅ تم اختيار الدعم الفني. يرجى إرسال مشكلتك.")
    elif text == "2":
        update.message.reply_text("📦 أدخل رقم الطلب لتتبع شحنتك.")
    elif text == "3":
        update.message.reply_text("📞 يمكنك التواصل معنا على الرقم: +962XXXXXXXXX")
    else:
        update.message.reply_text("❌ خيار غير صحيح! يرجى اختيار 1 أو 2 أو 3.")

def run_telegram_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

# تشغيل سيرفر وهمي لمنع Render من إيقاف الخدمة
def run_fake_server():
    PORT = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", PORT), SimpleHTTPRequestHandler)
    logging.info(f"Running fake server on port {PORT}...")
    server.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_telegram_bot).start()
    run_fake_server()  # تشغيل سيرفر وهمي
