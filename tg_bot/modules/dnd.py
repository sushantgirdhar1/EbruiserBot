import random
from typing import Optional

from telegram import Message, Update, Bot, User
from telegram import MessageEntity, ParseMode
from telegram.error import BadRequest
from telegram.ext import Filters, MessageHandler, run_async

from tg_bot import dispatcher
from tg_bot.modules.disable import DisableAbleCommandHandler, DisableAbleRegexHandler
from tg_bot.modules.sql import dnd_sql as sql
from tg_bot.modules.users import get_user_id


DND_GROUP = 7
DND_REPLY_GROUP = 8


@run_async
def dnd(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)
    if len(args) >= 2:
        reason = args[1]
    else:
        reason = ""

    sql.set_dnd(update.effective_user.id, reason)
    fname = update.effective_user.first_name
    update.effective_message.reply_text("{} is now on DND Mode!".format(fname))

    
@run_async
def no_longer_dnd(bot: Bot, update: Update):
    user = update.effective_user  # type: Optional[User]
    chat = update.effective_chat  # type: Optional[Chat]
    message = update.effective_message  # type: Optional[Message]

    if not user:  # ignore channels
        return

    res = sql.rm_dnd(user.id)
    if res:
        if message.new_chat_members:  #dont say msg
            return
        firstname = update.effective_user.first_name
        try:        
            options = [
            '{} is back online!',
            '{} is back!',
            '{} is in chat. DND is off then!',
            '{} kek you are here .!',
            '{} turned DND off.',
            '{} is finally here and DND off!',
            'Welcome back, After Studying! {}',
            'Where is {}?\nIn the chat!'
                    ]
            chosen_option = random.choice(options)
            update.effective_message.reply_text(chosen_option.format(firstname))
        except:
            return


@run_async
def reply_dnd(bot: Bot, update: Update):
    message = update.effective_message  # type: Optional[Message]
    userc = update.effective_user  # type: Optional[User]
    userc_id = userc.id
    if message.entities and message.parse_entities(
        [MessageEntity.TEXT_MENTION, MessageEntity.MENTION]):
        entities = message.parse_entities(
            [MessageEntity.TEXT_MENTION, MessageEntity.MENTION])

        chk_users = []
        for ent in entities:
            if ent.type == MessageEntity.TEXT_MENTION:
                user_id = ent.user.id
                fst_name = ent.user.first_name

                if user_id in chk_users:
                    return
                chk_users.append(user_id)
                
            if ent.type == MessageEntity.MENTION:
                user_id = get_user_id(message.text[ent.offset:ent.offset +
                                                   ent.length])
                if not user_id:
                    # Should never happen, since for a user to become dnd they must have spoken. Maybe changed username?
                    return
                
                if user_id in chk_users:
                    return
                chk_users.append(user_id)

                try:
                    chat = bot.get_chat(user_id)
                except BadRequest:
                    print("Error: Could not fetch userid {} for dnd module".
                          format(user_id))
                    return
                fst_name = chat.first_name

            else:
                return

            check_dnd(bot, update, user_id, fst_name, userc_id)
            
    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        fst_name = message.reply_to_message.from_user.first_name
        check_dnd(bot, update, user_id, fst_name, userc_id)


def check_dnd(bot, update, user_id, fst_name, userc_id):
    chat = update.effective_chat  # type: Optional[Chat]
    if sql.is_dnd(user_id):
        user = sql.check_dnd_status(user_id)
        if not user.reason:
            if int(userc_id) == int(user_id):
                return
            res = "{} is on study mode".format(fst_name)
            update.effective_message.reply_text(res)
        else:
            if int(userc_id) == int(user_id):
                return
            res = "{} is on study mode.\nReason: {}".format(fst_name, user.reason)
            update.effective_message.reply_text(res)


__help__ = """
DND means Do Not Disturb . if you mark yourself dnd . Bot will mark youself as dnd . and if someone tag you or mentions you , Bot will automatically replies to the person that you are on *Study Mode* . Whenever u come back online and message in group , then bot will turn DND Mode i.e Study Mode off automatically .
Note: Once Dnd , then bot will trigger dnd on all the groups , where Bot is Present .

*Availaible Commands:*
 - /dnd <reason>: mark yourself as DND(Do Not Disturb).
"""

DND_HANDLER = DisableAbleCommandHandler("dnd", dnd)
DND_REGEX_HANDLER = DisableAbleRegexHandler("(?i)brb", dnd, friendly="dnd")
NO_DND_HANDLER = MessageHandler(Filters.all & Filters.group, no_longer_dnd)
DND_REPLY_HANDLER = MessageHandler(Filters.all & Filters.group, reply_dnd)

dispatcher.add_handler(DND_HANDLER, DND_GROUP)
dispatcher.add_handler(DND_REGEX_HANDLER, DND_GROUP)
dispatcher.add_handler(NO_DND_HANDLER, DND_GROUP)
dispatcher.add_handler(DND_REPLY_HANDLER, DND_REPLY_GROUP)

__mod_name__ = "StudyMode"
__command_list__ = ["dnd"]
__handlers__ = [(DND_HANDLER, DND_GROUP), (DND_REGEX_HANDLER, DND_GROUP), (NO_DND_HANDLER, DND_GROUP),
                (DND_REPLY_HANDLER, DND_REPLY_GROUP)]
