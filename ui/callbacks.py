from telegram import Update
from telegram.ext import ContextTypes
from modes.investigator import start_investigation
# تأكد من استيراد دالة set_state من ملف الحالات الخاص بك
from states import set_state 

async def panel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # مهم جدًا لإيقاف علامة التحميل في التليجرام

    data = query.data
    user_id = query.from_user.id

    if data == "investigate":
        await query.message.reply_text("🔍 بدء وضع Investigator")
        await start_investigation(update, context)

    elif data == "ip":
        # بدلاً من "قريباً"، سنفعل نظام الحالات
        await set_state(user_id, "ip")
        await query.message.reply_text("🌍 **IP OSINT**\nأرسل عنوان الـ IP المراد فحصه:")

    elif data == "email":
        await set_state(user_id, "email")
        await query.message.reply_text("📧 **Email OSINT**\nأرسل البريد الإلكتروني للفحص:")

    elif data == "domain":
        await set_state(user_id, "domain")
        await query.message.reply_text("🌐 **Domain OSINT**\nأرسل رابط الموقع (Domain):")

    elif data == "username":
        await set_state(user_id, "username")
        await query.message.reply_text("👤 **Username OSINT**\nأرسل اسم المستخدم (Username):")

    elif data == "image":
        await set_state(user_id, "image")
        await query.message.reply_text("🖼️ **Image Intelligence**\nأرسل الصورة لتحليل بياناتها:")

    elif data == "hacked_devices":
        # تغيير الحالة لانتظار الإيميل الخاص بالأجهزة
        await set_state(user_id, "waiting_for_hacked_email")
        await query.message.reply_text("📥 **فحص الأجهزة المتصلة**\nمن فضلك أرسل البريد الإلكتروني المرتبط بالأجهزة لعرضها:")