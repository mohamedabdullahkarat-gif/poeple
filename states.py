import time

STATE = {}
TIMEOUT = 90  # ثواني قبل انتهاء الجلسة

async def set_state(user_id, state):
    STATE[user_id] = {"state": state, "time": time.time()}

async def get_state(user_id):
    data = STATE.get(user_id)
    if not data:
        return None
    if time.time() - data["time"] > TIMEOUT:
        STATE.pop(user_id, None)
        return None
    return data["state"]

async def clear_state(user_id):
    STATE.pop(user_id, None)
