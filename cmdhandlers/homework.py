from licenses import getNotionHeaders, getHmDB
from cmdhandlers.notion import NotionDatabase
import json, requests


def getHomeworks():
    db = NotionDatabase(getHmDB(), getNotionHeaders()).rows
    homeworks = []
    for row in db:
        id_hm = row.columns['ID'].value
        name = row.columns['Name']
        status = row.columns['Status']
        deadline = row.columns['Deadline'].value.split(sep="=")[0][5:10]
        subject = row.columns['Subject'].value
        text = f'#{id_hm} {name}\n{subject} {deadline} {status}'
        if status.value.lower() != 'sent':
            print(status)
            homeworks.append(text)
    text = '\n\n'.join(homeworks)
    return 'Homework\n--------------------\n'+text

def changeStatus(id_hm, status):
    db = NotionDatabase(getHmDB(), getNotionHeaders()).rows
    homework = ''
    for row in db:
        current_id = row.columns['ID'].value
        if current_id == id_hm:
            homework = row
            break
    if homework == '':
        return
    status_ = ['Not', 'In', 'Almost', 'Sent']
    status = status.capitalize()
    if status not in status_:
        return
    id_ = homework.rowData['id'].replace('-','')
    updateUrl = f'https://api.notion.com/v1/pages/{id_}'
    updateData = {
        "properties":{
            "Status":{
                "select":{
                    "name":status
                }
            }
        }
    }
    data = json.dumps(updateData)
    response = requests.patch(updateUrl, headers=getNotionHeaders(), data=data)

def getHomeworkInfo(id_hm):
    db = NotionDatabase(getHmDB(), getNotionHeaders()).rows
    for row in db:
        current_id = row.columns['ID'].value
        name = row.columns['Name']
        status = row.columns['Status']
        deadline = row.columns['Deadline'].value.split(sep="=")[0][5:10]
        subject = row.columns['Subject'].value
        if current_id == id_hm:
            return f'#{id_hm} {name}\n{subject}-{deadline} {status}'
    return

def hm(update, context):
    chat_id = update.message.chat_id
    try:
        id_hm = update.message.text.split(sep=" ")[1]
        context.bot.send_message(chat_id, getHomeworkInfo(id_hm))
    except:
        context.bot.send_message(chat_id, getHomeworks())

def hmst(update, context):
    chat_id = update.message.chat_id
    try:
        text = update.message.text.split(sep=" ")
        id_hm = text[1]
        status = text[2]
        changeStatus(id_hm, status)
        context.bot.send_message(chat_id, f'Homework {id_hm}\n{status}')
    except:
        context.bot.send_message(chat_id,'That homework is not created yet')

