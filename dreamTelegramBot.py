import os
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import argparse
from flask import Flask, request
from telepot.loop import OrderedWebhook
from dreamAnalyzer import *

def sendData(chat_id, bot, response):
    if bot == None:
        return

    bot.sendMessage(chat_id, response)

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
    if len(text.split(" ")) == 1 and text == "Ranking":
        return tagsRanking()
    elif len(text.split(" ")) == 2 and text.split(" ")[0] == "Search":
        return printByTag(text.split(" ")[1])
    else:
        return "Available commands:\nRanking: prints occurrences of repeated dream tags\nSearch [tag]: searches all dreams with the provided tag"

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
