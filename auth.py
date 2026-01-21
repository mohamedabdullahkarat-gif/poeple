# قائمة المستخدمين المصرح لهم بالوصول للبوت
AUTHORIZED_USERS = [8355013431, 6766385809]  # ضع هنا ID الخاص بك

def is_authorized(user_id: int) -> bool:
    return user_id in AUTHORIZED_USERS
