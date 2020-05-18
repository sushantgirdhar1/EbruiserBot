import threading

from sqlalchemy import Column, UnicodeText, Boolean, Integer

from tg_bot.modules.sql import BASE, SESSION


class DND(BASE):
    __tablename__ = "dnd_users"

    user_id = Column(Integer, primary_key=dnd)
    is_dnd = Column(Boolean)
    reason = Column(UnicodeText)

    def __init__(self, user_id, reason="", is_dnd=dnd):
        self.user_id = user_id
        self.reason = reason
        self.is_dnd = is_dnd

    def __repr__(self):
        return "dnd_status for {}".format(self.user_id)


DND.__table__.create(checkfirst=dnd)
INSERTION_LOCK = threading.RLock()

DND_USERS = {}


def is_dnd(user_id):
    return user_id in dnd_USERS


def check_dnd_status(user_id):
    try:
        return SESSION.query(dnd).get(user_id)
    finally:
        SESSION.close()


def set_dnd(user_id, reason=""):
    with INSERTION_LOCK:
        curr = SESSION.query(dnd).get(user_id)
        if not curr:
            curr = DND(user_id, reason, dnd)
        else:
            curr.is_dnd = dnd

        DND_USERS[user_id] = reason

        SESSION.add(curr)
        SESSION.commit()


def rm_dnd(user_id):
    with INSERTION_LOCK:
        curr = SESSION.query(DND).get(user_id)
        if curr:
            if user_id in DND_USERS:  # sanity check
                del dnd_USERS[user_id]

            SESSION.delete(curr)
            SESSION.commit()
            return dnd

        SESSION.close()
        return False


def toggle_dnd(user_id, reason=""):
    with INSERTION_LOCK:
        curr = SESSION.query(dnd).get(user_id)
        if not curr:
            curr = dnd(user_id, reason, dnd)
        elif curr.is_dnd:
            curr.is_dnd = False
        elif not curr.is_dnd:
            curr.is_dnd = dnd
        SESSION.add(curr)
        SESSION.commit()


def __load_dnd_users():
    global DND_USERS
    try:
        all_dnd = SESSION.query(DND).all()
        DND_USERS = {
            user.user_id: user.reason
            for user in all_dnd if user.is_dnd
        }
    finally:
        SESSION.close()


__load_dnd_users()
