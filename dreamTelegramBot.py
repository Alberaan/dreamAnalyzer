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
        response = "chat_id: " + str(chat_id) + "\nmyChat_id: " + str(myChat_id)
        if chat_id != myChat_id:
            response += str(type(chat_id)) + str(type(myChat_id))
            response += "\nThey are not equal!"

    sendData(chat_id, bot, response)

def on_inline_query(msg):
    pass

def on_chosen_inline_result(msg):
    pass

def processCommand(text):
    return tagsRanking

# Main starts here
token = str(os.environ["telegram_token"])
myChat_id = os.environ["telegram_chat_id"]
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
