import requests

async def email_lookup_raw(email):
    try:
        # استخدام API مجاني لفحص التسريبات
        url = f"https://api.proxynova.com/haveibeenpwned?email={email}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            breaches = data.get("breaches", 0)
            
            if breaches > 0:
                return (
                    f"⚠️ **هذا الإيميل مسرب!**\n"
                    f"📍 تم العثور عليه في `{breaches}` قاعدة بيانات مسربة.\n"
                    f"💡 ينصح بتغيير كلمة المرور فوراً."
                )
            else:
                return "✅ **أخبار جيدة:** هذا الإيميل غير موجود في قواعد البيانات المسربة المعروفة."
        else:
            return "❌ تعذر الوصول لقاعدة بيانات التسريبات حالياً."
            
    except Exception as e:
        return f"⚠️ حدث خطأ تقني أثناء الفحص: {str(e)}"