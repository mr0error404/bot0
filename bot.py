from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = "7530431758:AAHYOCjjp9fZ7K-PyGskQuLEsUbJIqsg_Hw"  # ضع التوكن الخاص بك هنا

def start(update: Update, context: CallbackContext):
    update.message.reply_text("مرحبًا! اختر خدمة:\n1️⃣ الدعم الفني\n2️⃣ تتبع الطلب\n3️⃣ الاتصال بنا")

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

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

updater.start_polling()
updater.idle()
