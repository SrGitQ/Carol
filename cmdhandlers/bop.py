import requests 
import re

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    return contents['url']

def bop(update, context):
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=get_url())
