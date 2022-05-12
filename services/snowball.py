data = {
    '0':[],
    '1':[],
    '2':[],
    '3':[],
    '4':[],
    '5':[],
    '6':['kha'],
    '7':[],
    '8':[],
    '9':[],
    '10':[],
    '11':[],
    '12':[],
    '13':[],
    '14':[],
    '15':[],
    '16':[],
    '17':[],
    '18':[],
    '19':[],
    '20':[],
    '21':[],
    '22':[],
    '23':[],
    '24':[],
    '25':[],
    '26':[],
    '27':[],
    '28':[],
    '29':[],
    '30':[],
    '31':[],
    '32':[],
    '33':[],
    '34':[],
    '35':[],
    '36':[],
    '37':[],
    '38':[],
    '39':[],
    '40':[],
    '41':[],
    '42':[],
    '43':[],
    '44':[],
    '45':[],
    '46':[],
    '47':[],
    '48':[],
    '49':[],
    '50':[],
    '51':[],
    '52':[]
}

def snowball(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    sticker_id = getStickerContextId(text)
    if sticker_id != 'NO':
        context.bot.send_sticker(chat_id, open(f"./services/snowdata/{sticker_id}.webp", "rb"))

def getStickerContextId(text):
    keys = data.keys()
    for key in keys:
        words = data[key]
        for word in words:
            if word in text.lower():
                return key
    return 'NO'




def SSnowball(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    if 'kha' in text.lower():
        context.bot.send_sticker(chat_id, open("./snowball/6.webp", "rb"))
