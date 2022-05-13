from cmdhandlers.notion import getNotionDatabase
import datetime
#from notion import getNotionDatabase
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
def getTodayN():
    return datetime.datetime.today().weekday()+1

def orderSchedule(schedule):
    
    for i, topic in enumerate(schedule.copy()):
        materia, order, hrs = topic
        order = int(order[2:])
        schedule[i] = [materia, order, hrs]
    #print(schedule)
    schedule = sorted(schedule, key=lambda x:x[1])
    schedule = [f'{topic[2]} {topic[0]}' for topic in schedule]
    return schedule

def normTime(time):
    time = time[2:]
    time = time.split(sep=':')
    norm_time = []
    for hour in time:
        h = hour[0]
        m = hour[1:]
        norm = f'{h}:{m}'
        norm_time.append(norm)
    return '-'.join(norm_time)

def sch_day_q(day):
    results = getNotionDatabase()
    schedule = []
    for result in results:
        ords = ''
        hrs = ''
        properties = result['properties']
        try:
            days = properties['Day']['rich_text'][0]['text']['content'].split(sep=' ')
            orders = properties['Order']['rich_text'][0]['text']['content'].split(sep=' ')
            hours = properties['Hours']['rich_text'][0]['text']['content'].split(sep=' ')
        except:
            days = []
            orders = []
            hours = []
        
        days = [int(day) for day in days]
        
        name = properties['Name']['title'][0]['text']['content']
        

        if len(orders)> 0:
            for order in orders:
                if int(order[0]) == day:
                    ords = order
                    break
        if len(hours) > 0:
            for time in hours:
                if int(time[0]) == day:
                    hrs = normTime(time)
                    
                    break
        if day in days:
            schedule.append([name, ords, hrs])

        #print(name, days)
        #schedule.append(name)
    return orderSchedule(schedule)

def sch_tdy_q():
    return sch_day_q(getTodayN())


def sch(update, context):
    day = update.message.text[5:7]
    nro_day = 0
    if day == '-1':
        nro_day = getTodayN()-1
        schedule = sch_day_q(nro_day)
    elif day == '+1':
        nro_day = getTodayN()+1
        schedule = sch_day_q(nro_day)
    elif day != '':
        nro_day = int(day)
        schedule = sch_day_q(nro_day)
    else:
        nro_day = getTodayN()
        schedule = sch_day_q(nro_day)
    text = days[nro_day-1] + '\n'
    text += '\n'.join(schedule)

    chat_id = update.message.chat_id
    context.bot.send_message(chat_id, text=text)

def schedule(update, context):
    text = 'Schedule\n\n'
    for i, day in enumerate(days):
        text += f'{day}\n'
        text += '\n'.join(sch_day_q(i+1))
        text += '\n\n'

    chat_id = update.message.chat_id
    context.bot.send_message(chat_id, text=text)


#print(sch_tdy_q())
