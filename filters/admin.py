from data.config import ADMINS

def is_admin(chat_id):
    if str(chat_id) in ADMINS:
        return True
    else: 
        return False


