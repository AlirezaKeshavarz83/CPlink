import logging

import os
from re import MULTILINE
import telegram

from telegram import (
    Update,
    InlineQueryResultArticle,
    InputTextMessageContent
)

from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    InlineQueryHandler,
    CallbackQueryHandler
)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def codeforces(s):
    j = -1
    for i in range(len(s)):
        if('a' <= s[i] <= 'z' or 'A' <= s[i] <= 'Z'):
            if(j != -1):
                return 0
            j = i
    for i in range(len(s)):
        if i == j or (not '0' <= s[i] <= '9'):
            return 0
    return "https://codeforces.com/contest/" + s[:j] + "/problem/" + s[j:]
def atcoder(s):
    if(len(s) < 5):
        return 0
    if(s[0] != 'a' or s[2] != 'c'):
        return 0
    if(not ('a' <= s[-1] <= 'z' or 'A' <= s[-1] <= 'Z')):
        return 0
    for i in range(3, len(s) - 1):
        if(not '0' <= s[i] <= '9'):
            return 0
    return "https://atcoder.jp/contests/" + s[:-1] + "/tasks/" + s[:-1] + "_" + s[-1]
    

token = os.getenv("token")
print('"' + token + '"')
updater = Updater(token, use_context=True)
admin = os.getenv("admin")

def start(update : Update, context : CallbackContext):
    user = update.message.from_user
    user_id = user.id
    context.bot.send_message(chat_id=admin, text= ": <a href=\"tg://user?id=" + user_id + "\">" + user.full_name + "</a>", parse_mode="HTML")
    update.message.reply_text("سلام")

def handle(update : Update, context : CallbackContext):
    user = update.message.from_user
    user_id = user.id
    text = update.message.text
    if codeforces(text):
        update.message.reply_text(codeforces(text))
    if atcoder(text):
        update.message.reply_text(atcoder(text))
    return


dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.all & ~Filters.command & ~Filters.update.edited_message, handle))

updater.start_polling()

updater.idle()
