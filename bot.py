import logging
import os
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

# تعريف مراحل المحادثة
ASK_NAME, ASK_ISSUE = range(2)

# إعدادات البوت
def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 مرحبًا! ما اسمك؟")
    return ASK_NAME  # انتقال إلى المرحلة التالية

def ask_name(update: Update, context: CallbackContext):
    user_name = update.message.text
    context.user_data["name"] = user_name  # حفظ الاسم
    update.message.reply_text(f"مرحبًا {user_name}! كيف يمكنني مساعدتك؟")
    return ASK_ISSUE  # انتقال إلى المرحلة التالية

def ask_issue(update: Update, context: CallbackContext):
    user_issue = update.message.text
    user_name = context.user_data.get("name")  # استرجاع الاسم المخزن
    update.message.reply_text(f"شكرًا لك {user_name}! سيتم مراجعة مشكلتك: \"{user_issue}\"")
    return ConversationHandler.END  # إنهاء المحادثة

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("❌ تم إلغاء المحادثة.")
    return ConversationHandler.END  # إنهاء المحادثة

def run_telegram_bot():
    TOKEN = "YOUR_BOT_TOKEN"
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # تعريف المحادثة
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_NAME: [MessageHandler(Filters.text & ~Filters.command, ask_name)],
            ASK_ISSUE: [MessageHandler(Filters.text & ~Filters.command, ask_issue)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

# تشغيل سيرفر وهمي لمنع Render من إيقاف الخدمة
def run_fake_server():
    PORT = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", PORT), SimpleHTTPRequestHandler)
    logging.info(f"Running fake server on port {PORT}...")
    server.serve_forever()

if __name__ == "__main__":
    # تشغيل البوت في Thread منفصل
    threading.Thread(target=run_telegram_bot).start()
    run_fake_server()  # تشغيل سيرفر وهمي
