import time
from telegram import Bot, Update, ParseMode
from telegram.ext import run_async
from tg_bot import dispatcher
from tg_bot.modules.disable import DisableAbleCommandHandler
from tg_bot.modules.helper_funcs.chat_status import user_admin

#sleep how many times after each edit in 'police' 
EDIT_SLEEP = 2
#edit how many times in 'police' 
EDIT_TIMES = 3

police_siren = [
            "🔴🔴🔴⬜️⬜️⬜️🔵🔵🔵\n🔴🔴🔴⬜️⬜️⬜️🔵🔵🔵\n🔴🔴🔴⬜️⬜️⬜️🔵🔵🔵",
            "🔵🔵🔵⬜️⬜️⬜️🔴🔴🔴\n🔵🔵🔵⬜️⬜️⬜️🔴🔴🔴\n🔵🔵🔵⬜️⬜️⬜️🔴🔴🔴"
]

fbi_ig = [
  "\O_O",
  "O_O/"
]

@user_admin
@run_async
def police(bot: Bot, update: Update):
    msg = update.effective_message.reply_text('Police is coming!')
    for x in range(EDIT_TIMES):
        msg.edit_text(police_siren[x%2]) 
        time.sleep(EDIT_SLEEP)
    msg.edit_text('Police is here!')

@user_admin
@run_async
def fbi(bot: Bot, update: Update):
    msg = update.effective_message.reply_text('FBI is coming!')
    for x in range(EDIT_TIMES):
        msg.edit_text(fbi_ig[x%2]) 
        time.sleep(EDIT_SLEEP)
    msg.edit_text('Police is here!')
    
__help__ = """
Some of the *Animation* Stuff
- /police : Sends a police emoji animation. 
- /fbi : Send O\_O animation
- /love ❣️
- /hack 👨‍💻
- /bombs 💣
- /moonanimation 🌚
- /clockanimation 🕛
- /earthanimation 🌍

Some of the *Fun* Stuff
 - /runs: reply a random string from an array of replies.
 - /slap: slap a user, or get slapped if not a reply.
 - /shrug : get shrug XD.
 - /table : get flip/unflip :v.
 - /decide : Randomly answers yes/no/maybe
 - /toss : Tosses A coin
 - /bluetext : check urself :V
 - /roll : Roll a dice.
 - /rlg : Join ears,nose,mouth and create an emo ;-;
 - /react: Reacts with a random reaction
"""
    
POLICE_HANDLER = DisableAbleCommandHandler("police", police)
FBI_HANDLER = DisableAbleCommandHandler("fbi", fbi)
dispatcher.add_handler(POLICE_HANDLER)    
dispatcher.add_handler(FBI_HANDLER)

__mod_name__ = "Fun"
__command_list__ = ["police", "fbi"]	
__handlers__ = [POLICE_HANDLER, FBI_HANDLER]
