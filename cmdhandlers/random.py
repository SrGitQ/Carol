import random

dinamikos_team = ['Juan', 'Isabel', 'Mayte', 'Osiris', 'Victor']


def randall(update, context):
    data = dinamikos_team.copy()
    text = ''
    random.shuffle(data)
    for i in range(1, 6):
        text += f'{i} - {data[i-1]}\n'

    chat_id = update.message.chat_id
    context.bot.send_message(chat_id, text=text)

def rand(update, context):
    data = dinamikos_team.copy()
    random.shuffle(data)

    chat_id = update.message.chat_id
    context.bot.send_message(chat_id, text=data[0])
