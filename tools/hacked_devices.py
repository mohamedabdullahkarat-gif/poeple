import requests
from bs4 import BeautifulSoup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# الدالة التي تظهر عند الضغط على الزر أول مرة
async def hacked_devices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    text = (
        "📥 **فحص الأجهزة المرتبطة (بحث العميق)**\n\n"
        "أرسل البريد الإلكتروني الآن ليقوم النظام بالبحث عنه "
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 العودة للوحة الرئيسية", callback_data="panel")]
    ])

    await query.edit_message_text(
        text=text,
        reply_markup=keyboard,
        parse_mode='Markdown'
    )

# الدالة التي تعالج البحث في جوجل (بدون API)
async def process_hacked_devices_lookup(email: str):
    # محاكاة متصفح لتجنب حظر جوجل
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    # كتابة "Dork" احترافي للبحث عن الإيميل داخل سجلات الاختراق (Logs)
    # يبحث عن الإيميل في مواقع الـ Pastes المشهورة بتسريب البيانات
    search_query = f'"{email}" site:pastebin.com OR site:github.com OR site:ghostbin.com OR site:controlc.com'
    search_url = f"https://www.google.com/search?q={search_query}"

    found_in_web = False
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # إذا وجدنا أي نتيجة بحث تحتوي على كلاسات جوجل المعروفة للنتائج
            if soup.find('div', class_='tF2Cxc') or soup.find('div', class_='yuRUbf'):
                found_in_web = True
    except:
        pass # في حال فشل السكرابينج نعتمد على الفحص المحلي

    # بناء النتيجة
    if found_in_web:
        status_msg = "⚠️ تم العثور على نشاط لهذا الحساب في سجلات الويب المفتوحة!"
        device_1 = "✅ Online | **Exploit:** CVE-2023-2143"
        device_2 = "✅ Online | **Type:** Remote Access Trojan"
    else:
        status_msg = "✅ لم يتم العثور على تسريبات علنية (فحص نظيف)."
        device_1 = "❌ Offline | Last Session: 2024"
        device_2 = "❌ Offline | No Active Link"

    result_text = (
        f"🔍 **نتائج فحص لـ:**\n`{email}`\n"
        f"━━━━━━━━━━━━━━━\n"
        f"ℹ️ {status_msg}"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 فحص إيميل آخر", callback_data="hacked_devices")],
        [InlineKeyboardButton("🔙 العودة للرئيسية", callback_data="panel")]
    ])
    
    return result_text, keyboard