from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def panel_keyboard():
    keyboard = [
        # الصفوف الأولى (كما هي في تصميمك)
        [
            InlineKeyboardButton("🛠️ إنشاء فيروس", callback_data="virus"),
            InlineKeyboardButton("💻 جهازك مخترق أم لا", callback_data="hacked_devices")
        ],
        [
            InlineKeyboardButton("🎧 تغيير صوتك الي صوت هكر", callback_data="audio_rec"),
            InlineKeyboardButton("📍 إيجاد موقع الضحية", callback_data="iplogger")
        ],
        [
            InlineKeyboardButton("🔍 فحص إمكانيات جهزي المستخدم هنا", callback_data="server_scan")
        ],
        [
            InlineKeyboardButton("🔐 إنشاء كلمة مرور قوية", callback_data="pass_gen")
        ],
        [
            InlineKeyboardButton("📧 إنشاء إيميل وهمي", callback_data="temp_mail_name"),
            InlineKeyboardButton("☎️ إنشاء اتصال وهمي", callback_data="fake_call"),
            InlineKeyboardButton("☎️ إرسال رسالة وهمي", callback_data="fake_sms")
        ],
        [
            InlineKeyboardButton("👤 بحث عن مستخدم", callback_data="user_search"),
            InlineKeyboardButton("📊 بحث بيانات الصورة (EXIF)", callback_data="exif_data")
        ],
        [
            InlineKeyboardButton("🖼️ البحث بالصور", callback_data="img_search"),
            InlineKeyboardButton("🚫 كشف المواقع المزيفة", callback_data="phishing_check")
        ],
        [
            InlineKeyboardButton("🧬 تحليل ملفات (فحص فيروسات)", callback_data="virus_total")
        ],

    ] # تأكد من وجود الفواصل بين كل [] والأخرى بالأعلى

    return InlineKeyboardMarkup(keyboard)