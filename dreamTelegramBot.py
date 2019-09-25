import os
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import argparse
from flask import Flask, request
from telepot.loop import OrderedWebhook
from dreamAnalyzer import *
import re

def renderID(my_keyboard, line):
    if len(line) <1:
        return
    
    result = re.findall(r'^<id>(.*)<\/id>$', line)[0]
    my_keyboard.append([InlineKeyboardButton(text="View dream: " + result, callback_data="Read " + result)])
    
    return my_keyboard

def renderDate(my_keyboard, line):
    if len(line) <1:
        return
    
    result = re.findall(r'^<date>(.*)<\/date>$', line)[0]
    my_keyboard.append([InlineKeyboardButton(text="View dreams in " + result, callback_data="Date " + result)])
    
    return my_keyboard
    
def sendData(chat_id, bot, response):
    if bot == None:
        return
    
    my_keyboard = []
    textToSend = ""
    
    for line in response.split("\n"):
        if ("<id>" in line) and ("</id>" in line):
            my_keyboard = renderID(my_keyboard, line)
        elif ("<date>" in line) and ("</date>" in line):
            my_keyboard = renderDate(my_keyboard, line)
        else:
            textToSend += line + "\n"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=my_keyboard)
    bot.sendMessage(chat_id, textToSend, reply_markup=keyboard)

def on_callback_query(msg):
    return

#def handle(msg):
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text' and chat_id == myChat_id:
        response = processCommand(msg["text"])
    else:
        response = "error"

    sendData(chat_id, bot, response)

def on_inline_query(msg):
    pass

def on_chosen_inline_result(msg):
    pass

def processCommand(text):
    if text.split(" ")[0] == "Ranking":
        return tagsRanking(text)        
    elif text.split(" ")[0] == "Filter":
        return printByTag(text)
    elif text.split(" ")[0] == "Read":
        return printById(text)
    elif text.split(" ")[0] == "Date":
        return notesByDate(text)
    else:
        return printHelp()

# Main starts here
token = str(os.environ["telegram_token"])
myChat_id = int(os.environ["telegram_chat_id"])
bot = telepot.Bot(token) # Bot is created from the telepot class
app = Flask(__name__)
URL = str(os.environ["telegram_url"])
webhook = OrderedWebhook(bot, {'chat': on_chat_message,
                               'callback_query': on_callback_query,
                               'inline_query': on_inline_query,
                               'chosen_inline_result': on_chosen_inline_result})

@app.route('/', methods=['GET', 'POST'])
def pass_update():
    webhook.feed(request.data)
    return 'OK'

if __name__ == '__main__':
    app.run()
    printf("Executed the run")
    
if __name__ != '__main__':
    try:
        bot.setWebhook(URL)
    # Sometimes it would raise this error, but webhook still set successfully.
    except telepot.exception.TooManyRequestsError:
        pass

    webhook.run_as_thread()
