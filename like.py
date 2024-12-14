from pyrogram import Client, filters

# Bot token and API details
TOKEN = '7041654616:AAHCsdChgpned-dlBEjv-OcOxSi_mY5HRjI'
CHAT_ID = '-1002374330304'
LIKE_EMOJI = '👍'
DISLIKE_EMOJI = '👎'

# Initialize the Client
app = Client("my_bot", bot_token=TOKEN)

@app.on_message(filters.channel)
async def send_reaction(client, message):
    if message.chat.id == int(CHAT_ID):
        await client.send_message(chat_id=message.chat.id, text=LIKE_EMOJI, reply_to_message_id=message.message_id)
        await client.send_message(chat_id=message.chat.id, text=DISLIKE_EMOJI, reply_to_message_id=message.message_id)

if __name__ == "__main__":
    app.run()
