import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext

# تعريف مراحل المحادثة
ASK_NAME, ASK_ISSUE = range(2)

# إعدادات البوت
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("👋 مرحبًا! ما اسمك؟")
    return ASK_NAME  # انتقال إلى المرحلة التالية

async def ask_name(update: Update, context: CallbackContext) -> int:
    user_name = update.message.text
    context.user_data["name"] = user_name  # حفظ الاسم
    await update.message.reply_text(f"مرحبًا {user_name}! كيف يمكنني مساعدتك؟")
    return ASK_ISSUE  # انتقال إلى المرحلة التالية

async def ask_issue(update: Update, context: CallbackContext) -> int:
    user_issue = update.message.text
    user_name = context.user_data.get("name")  # استرجاع الاسم المخزن
    await update.message.reply_text(f"شكرًا لك {user_name}! سيتم مراجعة مشكلتك: \"{user_issue}\"")
    return ConversationHandler.END  # إنهاء المحادثة

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("❌ تم إلغاء المحادثة.")
    return ConversationHandler.END  # إنهاء المحادثة

# تشغيل البوت
def run_telegram_bot():
    TOKEN = "YOUR_BOT_TOKEN"  # تأكد من إدخال التوكن الصحيح هنا
    application = Application.builder().token(TOKEN).build()

    # تعريف المحادثة
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
            ASK_ISSUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_issue)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    application.add_handler(conv_handler)
    application.run_polling()

# تشغيل خادم وهمي لمنع توقف الخدمة
def run_fake_server():
    PORT = int(os.environ.get("PORT", 8080))  # المنفذ الذي سيتم ربطه مع الخدمة
    server = HTTPServer(("0.0.0.0", PORT), SimpleHTTPRequestHandler)
    print(f"Running fake server on port {PORT}...")
    server.serve_forever()

# تشغيل كل شيء في خيوط منفصلة
if __name__ == "__main__":
    threading.Thread(target=run_telegram_bot).start()  # تشغيل البوت في خيط منفصل
    run_fake_server()  # تشغيل الخادم الوهمي
