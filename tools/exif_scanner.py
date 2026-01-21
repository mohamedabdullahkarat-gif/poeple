from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_gps_info(exif_data):
    """تحويل إحداثيات GPS إلى رابط خرائط جوجل مباشر"""
    gps_info = {}
    for tag, value in exif_data.items():
        decoded = TAGS.get(tag, tag)
        if decoded == "GPSInfo":
            for t in value:
                sub_decoded = GPSTAGS.get(t, t)
                gps_info[sub_decoded] = value[t]
    
    if gps_info:
        try:
            def to_deg(value):
                # تحويل الدرجات والدقائق والثواني إلى عشري
                d = float(value[0])
                m = float(value[1])
                s = float(value[2])
                return d + (m / 60.0) + (s / 3600.0)

            lat = to_deg(gps_info['GPSLatitude'])
            if gps_info.get('GPSLatitudeRef') != 'N': lat = -lat
            
            lon = to_deg(gps_info['GPSLongitude'])
            if gps_info.get('GPSLongitudeRef') != 'E': lon = -lon
            
            # رابط خرائط جوجل المباشر
            return f"📍 **الموقع المكتشف:** [اضغط هنا لفتح الخريطة](https://www.google.com/maps?q={lat},{lon})"
        except Exception:
            return "📍 بيانات الموقع موجودة ولكنها تالفة أو غير مكتملة."
    return "📍 لا توجد إحداثيات موقع (GPS) في هذه الصورة."

def scan_exif(image_path):
    """استخراج بيانات الميتاداتا ومعلومات الصورة الأساسية"""
    try:
        image = Image.open(image_path)
        
        # 1. معلومات الملف الأساسية (تظهر دائماً حتى لو حُذفت الـ EXIF)
        basic_info = [
            "🖼️ **خصائص الصورة الأساسية:**",
            f"🔹 الأبعاد: `{image.width}x{image.height}`",
            f"🔹 الصيغة: `{image.format}`",
            f"🔹 نظام الألوان: `{image.mode}`"
        ]
        
        exif_data = image._getexif()
        
        # إذا لم توجد EXIF نعيد المعلومات الأساسية فقط مع تنبيه
        if not exif_data:
            basic_info.append("\n⚠️ **تنبيه:** تم حذف بيانات الـ EXIF من هذه الصورة (ربما بواسطة تطبيق تواصل اجتماعي).")
            return "\n".join(basic_info)

        # 2. استخراج بيانات الجهاز والوقت
        report = []
        important_tags = {
            'Make': 'الشركة المصنعة',
            'Model': 'موديل الجهاز',
            'Software': 'النظام/البرنامج',
            'DateTime': 'تاريخ الالتقاط',
            'LensModel': 'عدسة الكاميرا'
        }

        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name in important_tags:
                report.append(f"🔹 {important_tags[tag_name]}: `{value}`")

        # 3. دمج النتائج
        final_report = "\n".join(basic_info) + "\n\n🔍 **البيانات المخفية المكتشفة:**\n"
        if report:
            final_report += "\n".join(report)
        else:
            final_report += "• لم يتم العثور على معلومات عن الجهاز."

        # 4. إضافة رابط الموقع
        final_report += f"\n\n{get_gps_info(exif_data)}"
        
        return final_report

    except Exception as e:
        return f"❌ خطأ أثناء تحليل الصورة: {str(e)}"