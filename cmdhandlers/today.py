
def today(update, context):
    #logic
    logic_text = ''
    text = f'Helloo, good day Dinamikos {logic_text} Have a nice day!'

    chat_id = update.message.chat_id
    context.bot.send_message(chat_id, text=text)
