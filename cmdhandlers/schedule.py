from cmdhandlers.notion import NotionDatabase
from licenses import getSchDB, getNotionHeaders
import datetime

def today(sigma=0):
    return datetime.datetime.today().weekday()+sigma

def nameDay(day:int):
    return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][day]

def stdSchTime(time:str)->str:
    time = time.split(':')
    start = time[0][0] + ':' + time[0][1:]
    end = time[1][0] + ':' + time[1][1:]
    return start + '-' + end


def orderSchedule(schedule):
    for i, topic in enumerate(schedule.copy()):
        subject, hours = topic
        place = int(hours[0])
        schedule[i] = [place, subject, hours]
    schedule = sorted(schedule, key=lambda x:x[0])
    return [f'{topic[2]} {topic[1]}' for topic in schedule]

def getSchedule(day:int=today()):
    data = NotionDatabase(getSchDB(), getNotionHeaders()).rows
    schedule = []
    for row in data:
        name = row.columns['Name']
        days = row.columns['Day'].value
        hours = row.columns['Hours'].value
        if str(day+1) in days:
            # get the corret hour
            hours = hours.split(sep=' ')
            for hour in hours:
                if f'{day+1}-' in hour:
                    hours = hour[2:]
                    break

            schedule.append([name, stdSchTime(hours)])
    return '\n'.join(orderSchedule(schedule))

def sch(update, context):
    chat_id = update.message.chat_id
    try:
        opt = update.message.text.split(sep=" ")[1]
        if opt == 't':
            sch, day = getSchedule(today(1)), today(1)
        elif opt == 'y':
            sch, day = getSchedule(today(-1)), today(-1)
        elif opt in ['1', '2', '3', '4', '5']:
            sch, day = getSchedule(int(opt)-1), int(opt)-1
    except:
        sch, day = getSchedule(), today()
    if len(sch) > 0:
        context.bot.send_message(chat_id, nameDay(day)+'\n'+sch)
    else:
        context.bot.send_message(chat_id, f'\nNo school on {nameDay(day)} ;D')

def schedule(update, context):
    text = 'Schedule\n\n' + '\n\n'.join([f'{nameDay(i)}\n{getSchedule(i)}' for i in range(0,5)])
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id,text)

