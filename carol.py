import logging
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from cmdhandlers.bop import bop
from cmdhandlers.sch import sch
from cmdhandlers.sch import schedule
from cmdhandlers.random import randall
from cmdhandlers.random import rand
from licenses import getTelegramToken
from services.snowball import snowball



if __name__ == "__main__":
    updater = Updater(getTelegramToken(), use_context=True)
    dp = updater.dispatcher
    
    '''
    commands 
    dp.add_handler(CommandHandler('command', bop))
    '''
    dp.add_handler(CommandHandler('bop', bop))
    dp.add_handler(CommandHandler('sch', sch))
    dp.add_handler(CommandHandler('schedule', schedule))
    dp.add_handler(CommandHandler('randall', randall))
    dp.add_handler(CommandHandler('rand', rand))
    #dp.add_handler(CommandHandler('snball', snowball))
    dp.add_handler(MessageHandler(Filters.text, snowball))
    updater.start_polling()
    updater.idle()


