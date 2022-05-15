from random import randint
import requests, json
from cmdhandlers.notion import NotionDatabase
from licenses import getCarol, getNotionHeaders, getCarolStkStatus

data = {
    '0':['wow','woow','wooow'],
    '1':['okidoki', 'okay', 'Okidoki', 'Okay', 'Ok', 'ok'],
    '2':['no puede ser', 'No puede ser', 'no puemde ser', 'No puemde ser', 'Not again', 'not again'],
    '3':[],
    '4':['tqm', 'toy proud', 'estoy orgulloso de ti', 'estoy orgullosa de ti', 'heroe', 'poderosa', 'poderoso'],
    '5':['triste', 'sad', 'estoy triste', 'Estoy triste'],
    '6':['kha','que', 'qué?', 'k', 'q', '¿qué', '¿que?', '¿Que?', 'Qué?', 'que?', 'Que?'],
    '7':['Te amo', 'te amo', 't amo', 'no te quiero', 'no tqm'],
    '8':['Como?', 'como?', '¿como?', '¿Como?'],
    '9':['no puede ser', 'No puede ser', 'no puemde ser', 'No puemde ser', 'Not again', 'not again'],
    '10':['nooo'],
    '11':['tengo un plan'],
    '12':[],
    '13':[],
    '14':['gm', 'good morning', 'Good morning', 'morning', 'buenos dias', 'buenos días', 'Buenos días', 'Buenos dias'],
    '15':[],
    '16':['Acepto', 'acepto', 'va', 'vaaa', 'Vaaa', 'Va'],
    '17':[],
    '18':['raw'],
    '19':['no digas eso'],
    '20':['siii'],
    '21':[],
    '22':[],
    '23':['porfis', 'ti'],
    '24':[],
    '25':[],
    '26':['que guapa', 'que guapo', 'hermosa', 'hermoso', 'Hermosa', 'Hermoso', 'beautiful', 'Beautiful'],
    '27':['que guapa', 'que guapo', 'hermosa', 'hermoso', 'Hermosa', 'Hermoso', 'beautiful', 'Beautiful'],
    '28':[],
    '29':['Te extraño', 'te extraño', 'Los extraño', 'los extraño', 'miss u', 'Miss u', 'miss you', 'Miss you', 'I miss you'],
    '30':['NO'],
    '31':['me amas'],
    '32':['Victory', 'victoria', 'muajaja'],
    '33':[],
    '34':[],
    '35':[],
    '36':['kha','que', 'qué?', 'k', 'q', '¿qué', '¿que?', '¿Que?', 'Qué?', 'que?', 'Que?'],
    '37':[],
    '38':[],
    '39':['wow','woow','wooow'],
    '40':['jiji', 'jeje'],
    '41':['Te amo', 'te amo', 't amo', 'no te quiero', 'no tqm'],
    '42':[],
    '43':[],
    '44':[],
    '45':[],
    '46':[],
    '47':[],
    '48':[],
    '49':[],
    '50':['mimido', 'a mimir', 'A mimir', 'voy a mimir', 'a dormir', 'A dormir', 'Voy a mimir', 'Vayan a mimir', 'Vayan a dormir', 'vayan a mimir'],
    '51':['stop', 'Stop'],
    '52':['si puedo', 'I can do it', 'You can do it', 'Tu puedes', 'Tú puedes', 'you can do it']
}

def snowball(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    sticker_id = getStickerContextId(text)
    if sticker_id != 'NO':
        context.bot.send_sticker(chat_id, open(f"./services/snowdata/{sticker_id}.webp", "rb"))


class StkStatus:
    def __init__(self):
        self.stop = NotionDatabase(getCarol(), getNotionHeaders()).rows[0]
        self.stop = self.stop.columns['Tags'].value
    def getStatus(self):
        if self.stop == 'Yes':
            return True
        else:
            return False
    
    def setStatus(self, status):
        updateUrl = f'https://api.notion.com/v1/pages/{getCarolStkStatus()}'
        if status:
            status = 'Yes'
        else:
            status = 'No'

        updateData = {
            "properties":{
                "Tags": {
                    "select": {
                        "name": status
                    }
                }
            }
        }
        data = json.dumps(updateData)
        response = requests.patch(updateUrl, headers=getNotionHeaders(), data=data)
        print('Stickers changed status',response.status_code)


def getStickerContextId(text):
    stop = StkStatus()
    keys = data.keys()
    options = []

    if text == 'Carol stop':
        stop.setStatus(False)
        return '5'
    if text == 'Carol talk':
        stop.setStatus(True)
        return '11'

    if not stop.getStatus():
        return 'NO'
    
    for key in keys:
        words = data[key]
        for word in words:
            if word.lower() in text.lower():
                options.append(key)

    if len(options) == 1:
        return options[0]

    elif len(options) > 1:
        i = randint(0, (len(options)-1))
        return options[i]
    options.clear()

    return 'NO'




def SSnowball(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    if 'kha' in text.lower():
        context.bot.send_sticker(chat_id, open("./snowball/6.webp", "rb"))
