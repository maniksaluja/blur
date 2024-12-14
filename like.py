from pyrofork import Client, filters

TOKEN = '7041654616:AAHCsdChgpned-dlBEjv-OcOxSi_mY5HRjI'
CHAT_ID = '-1002374330304'
LIKE_EMOJI = '👍'
DISLIKE_EMOJI = '👎'

app = Client(TOKEN)

@app.on_message(filters.channel_post)
async def send_reaction(update, context):
    message = update.channel_post
    if message:
        await context.bot.send_message(chat_id=message.chat_id, text=LIKE_EMOJI, reply_to_message_id=message.message_id)
        await context.bot.send_message(chat_id=message.chat_id, text=DISLIKE_EMOJI, reply_to_message_id=message.message_id)

app.run()
