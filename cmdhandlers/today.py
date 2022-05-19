from weather import getWeatherMsg
from schedule import sch
def today(context):
    #logic
    logic_text = sch()'\n'+getWeatherMsg()
    text = f'Helloo, good day Dinamikos\n{logic_text}\nHave a nice day!'

    #chat_id = update.message.chat_id#-690320685
    context.bot.send_message('-690320685', text=text)
