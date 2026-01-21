from pydub import AudioSegment
import os
import logging

# إعدادات اختيارية لمستخدمي ويندوز (قم بفك التعليق وتعديل المسار إذا واجهت مشكلة)
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"

def apply_hacker_effect(input_path, output_path):
    """
    تطبيق فلتر الصوت الغليظ (Deep Voice) لمحاكاة صوت الهكر.
    """
    try:
        # 1. تحميل الملف الصوتي
        # مكتبة pydub تتعرف تلقائياً على التنسيق إذا كان FFmpeg مثبتاً
        audio = AudioSegment.from_file(input_path)
        
        # 2. تغيير طبقة الصوت (Pitch Shifting)
        # نقوم بخفض معدل العينات (Sample Rate) بنسبة 30% لجعل الصوت ضخماً
        low_pitch_sample_rate = int(audio.frame_rate * 0.70)
        
        # تطبيق التغيير مع الحفاظ على جودة الإطار
        hacker_voice = audio._spawn(audio.raw_data, overrides={
            "frame_rate": low_pitch_sample_rate
        }).set_frame_rate(audio.frame_rate)
        
        # 3. تضخيم الصوت قليلاً (Boost) لزيادة الهيبة
        hacker_voice = hacker_voice + 5 
        
        # 4. إضافة لمسة معدنية (اختياري: تقليل الجودة لمحاكاة الروبوت)
        hacker_voice = hacker_voice.set_frame_rate(16000)
        
        # 5. تصدير الملف النهائي بصيغة mp3 وبجودة عالية
        hacker_voice.export(output_path, format="mp3", bitrate="192k")
        
        logging.info(f"✅ تم معالجة الصوت بنجاح: {output_path}")
        return True

    except Exception as e:
        logging.error(f"❌ خطأ في معالجة الصوت: {e}")
        return False

# دالة إضافية إذا أردت دمج موسيقى خلفية (Background Music) مستقبلاً
def mix_with_background(voice_path, bg_path, output_path):
    try:
        voice = AudioSegment.from_file(voice_path)
        bg = AudioSegment.from_file(bg_path) - 20 # خفض صوت الموسيقى جداً
        
        mixed = voice.overlay(bg, loop=True)
        mixed.export(output_path, format="mp3")
        return True
    except:
        return False