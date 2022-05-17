from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from cmdhandlers.bop import bop
from cmdhandlers.schedule import sch, schedule
from cmdhandlers.random import randall, rand
from licenses import getTelegramToken
from services.snowball import snowball
from cmdhandlers.today import today
from cmdhandlers.homework import hm, hmst
import datetime



if __name__ == "__main__":
    updater = Updater(getTelegramToken(), use_context=True)
    dp = updater.dispatcher
    routine = updater.job_queue
    routine.run_daily(today, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(hour=11, minute=43, second=00))
    '''
    commands 
    dp.add_handler(CommandHandler('command', bop))
    '''
    dp.add_handler(CommandHandler('bop', bop))
    dp.add_handler(CommandHandler('sch', sch))
    dp.add_handler(CommandHandler('schedule', schedule))
    dp.add_handler(CommandHandler('randall', randall))
    dp.add_handler(CommandHandler('rand', rand))
    #dp.add_handler(CommandHandler('today', today))
    dp.add_handler(CommandHandler('hm', hm))
    dp.add_handler(CommandHandler('hmst', hmst))
    dp.add_handler(MessageHandler(Filters.text, snowball))
    updater.start_polling()
    updater.idle()


