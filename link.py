from pyrogram import Client, filters
import requests

# Yeh Telegram bot ka token hai
API_ID = '26980824'
API_HASH = 'fb044056059384d3bea54ab7ce915226'
BOT_TOKEN = '7041654616:AAHCsdChgpned-dlBEjv-OcOxSi_mY5HRjI'
TELEGRAPH_ACCESS_TOKEN = '-1002374330304'

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.photo & filters.private)
async def photo_handler(client, message):
    await message.reply_text('Photo mili! Ab link create kar raha hoon...')
    
    # Photo URL prapt karte hain
    photo = await client.download_media(message.photo.file_id)
    
    with open(photo, "rb") as file:
        files = {"file": file}
        response = requests.post("https://telegra.ph/upload", files=files)
    
    response_json = response.json()
    telegraph_url = "https://telegra.ph" + response_json[0]['src']
    
    # Original message ka caption update karte hain
    await message.edit_caption(caption=f'Link create kar diya: {telegraph_url}')
    
app.run()
