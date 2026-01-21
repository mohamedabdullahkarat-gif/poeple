from telegram import Update
from telegram.ext import ContextTypes
from ui.keyboards import panel_keyboard
from auth import is_authorized

async def panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # تحديد مصدر الرسالة (سواء ضغطة زر أو رسالة نصية)
    query = update.callback_query
    
    # التحقق من الصلاحية
    if not is_authorized(user_id):
        if query:
            await query.answer("❌ البوت خاص", show_alert=True)
        else:
            await update.message.reply_text("❌ البوت خاص")
        return

    text = "هذا البوت هو مساعدك الرقمي الشامل، المصمم خصيصاً لخبراء الأمن السيبراني وطلاب تقنية المعلومات."

    if query:
        # إذا جاء الطلب من ضغطة زر (مثل زر "العودة")
        await query.answer()
        await query.edit_message_text(
            text=text,
            reply_markup=panel_keyboard()
        )
    else:
        # إذا جاء الطلب من أمر نصي (مثل /start أو /panel)
        await update.message.reply_text(
            text=text,
            reply_markup=panel_keyboard()
        )