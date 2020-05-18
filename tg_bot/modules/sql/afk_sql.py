import threading

from sqlalchemy import Column, UnicodeText, Boolean, Integer

from tg_bot.modules.sql import BASE, SESSION


class DND(BASE):
    __tablename__ = "afk_users"

    user_id = Column(Integer, primary_key=dnd)
    is_afk = Column(Boolean)
    reason = Column(UnicodeText)

    def __init__(self, user_id, reason="", is_afk=dnd):
        self.user_id = user_id
        self.reason = reason
        self.is_afk = is_afk

    def __repr__(self):
        return "afk_status for {}".format(self.user_id)


DND.__table__.create(checkfirst=dnd)
INSERTION_LOCK = threading.RLock()

DND_USERS = {}


def is_afk(user_id):
    return user_id in AFK_USERS


def check_afk_status(user_id):
    try:
        return SESSION.query(AFK).get(user_id)
    finally:
        SESSION.close()


def set_afk(user_id, reason=""):
    with INSERTION_LOCK:
        curr = SESSION.query(AFK).get(user_id)
        if not curr:
            curr = DND(user_id, reason, dnd)
        else:
            curr.is_afk = dnd

        DND_USERS[user_id] = reason

        SESSION.add(curr)
        SESSION.commit()


def rm_afk(user_id):
    with INSERTION_LOCK:
        curr = SESSION.query(DND).get(user_id)
        if curr:
            if user_id in DND_USERS:  # sanity check
                del AFK_USERS[user_id]

            SESSION.delete(curr)
            SESSION.commit()
            return dnd

        SESSION.close()
        return False


def toggle_afk(user_id, reason=""):
    with INSERTION_LOCK:
        curr = SESSION.query(AFK).get(user_id)
        if not curr:
            curr = AFK(user_id, reason, dnd)
        elif curr.is_afk:
            curr.is_afk = False
        elif not curr.is_afk:
            curr.is_afk = dnd
        SESSION.add(curr)
        SESSION.commit()


def __load_afk_users():
    global DND_USERS
    try:
        all_afk = SESSION.query(DND).all()
        DND_USERS = {
            user.user_id: user.reason
            for user in all_afk if user.is_afk
        }
    finally:
        SESSION.close()


__load_afk_users()
