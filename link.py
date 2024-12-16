import requests
from pyrogram import Client, filters

# Your bot token and channel info
API_ID = '26980824'
API_HASH = 'fb044056059384d3bea54ab7ce915226'
BOT_TOKEN = '7041654616:AAHCsdChgpned-dlBEjv-OcOxSi_mY5HRjI'
CHANNEL_ID = '-1002374330304'  # Channel username or channel ID

# Function to upload the photo to Telegraph and get the link
def upload_to_telegraph(photo_url):
    url = 'https://telegra.ph/upload'
    files = {'file': requests.get(photo_url).content}
    response = requests.post(url, files=files)
    data = response.json()
    if 'error' not in data:
        return f"https://telegra.ph{data[0]['src']}"
    return None

# Pyrogram Client setup
app = Client("my_bot", bot_token=BOT_TOKEN)

# Handler to process the photo message
@app.on_message(filters.photo & filters.chat(CHANNEL_ID))
async def handle_photo(client, message):
    # Get the file ID of the photo
    file = await message.download()  # Download the file
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file}"
    
    # Generate the Telegraph link for the photo
    telegraph_link = upload_to_telegraph(file_url)
    if telegraph_link:
        # Update the caption of the photo with the Telegraph link
        await message.edit_caption(f"Here's the image: {telegraph_link}")

# Run the bot
app.run()
