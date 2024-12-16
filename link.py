from pyrogram import Client, filters
from imgurpython import ImgurClient
import logging
import time

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Telegram API Details
api_id = 26980824
api_hash = 'fb044056059384d3bea54ab7ce915226'
bot_token = "7041654616:AAHCsdChgpned-dlBEjv-OcOxSi_mY5HRjI"
channel_id = -1002374330304  # Replace with your channel ID

# Imgur API Details
imgur_client_id = "your_imgur_client_id"  # Replace with your Imgur Client ID
imgur_client_secret = "your_imgur_client_secret"  # Replace with your Imgur Client Secret

# Initialize Imgur Client
imgur = ImgurClient(imgur_client_id, imgur_client_secret)

# Initialize Pyrogram Client
app = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.chat(channel_id) & filters.photo)
async def handle_photo(client, message):
    try:
        logging.info("Photo received.")
        photo_file = await message.download()
        logging.info("Photo downloaded: %s", photo_file)

        # Upload photo to Imgur
        logging.info("Uploading photo to Imgur...")
        imgur_response = imgur.upload_from_path(photo_file, anon=True)
        imgur_link = imgur_response['link']
        logging.info("Imgur link created: %s", imgur_link)

        # Add link to the caption
        new_caption = (message.caption or "") + f"\n\n[Image Link]({imgur_link})"
        await message.edit_caption(new_caption)
        logging.info("Caption updated with Imgur link.")

    except Exception as e:
        logging.error("Error occurred: %s", str(e))

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply("Bot is active and running!")
    logging.info("Bot started successfully.")

if __name__ == "__main__":
    logging.info("Bot is starting...")
    app.run()
