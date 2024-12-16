import requests
import logging
from pyrogram import Client, filters
import asyncio

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Your bot token and channel info
API_ID = '26980824'
API_HASH = 'fb044056059384d3bea54ab7ce915226'
BOT_TOKEN = '7041654616:AAHCsdChgpned-dlBEjv-OcOxSi_mY5HRjI'
CHANNEL_ID = '-1002374330304'  # Channel username or channel ID

# Function to upload the photo to Telegraph and get the link
def upload_to_telegraph(photo_url):
    try:
        logger.info(f"Uploading photo to Telegraph from URL: {photo_url}")
        url = 'https://telegra.ph/upload'
        files = {'file': requests.get(photo_url).content}
        response = requests.post(url, files=files)
        data = response.json()
        if 'error' not in data:
            logger.info("Photo uploaded successfully to Telegraph.")
            return f"https://telegra.ph{data[0]['src']}"
        else:
            logger.error(f"Error uploading photo: {data.get('error')}")
    except Exception as e:
        logger.error(f"Exception while uploading photo: {e}")
    return None

# Pyrogram Client setup
app = Client("my_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# Function to handle photo messages sequentially
async def process_photos_sequentially(client, messages):
    for message in messages:
        logger.info(f"Processing photo with message ID {message.message_id}")
        
        try:
            # Download the file locally
            file = await message.download()
            file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file}"
            
            # Log the photo URL being uploaded
            logger.info(f"File URL: {file_url}")
            
            # Generate the Telegraph link for the photo
            telegraph_link = await app.loop.run_in_executor(None, upload_to_telegraph, file_url)
            
            if telegraph_link:
                # Log link creation
                logger.info(f"Telegraph link created: {telegraph_link}")
                
                # Update the caption of the photo with the Telegraph link
                await message.edit_caption(f"Here's the image: {telegraph_link}")
                logger.info(f"Updated caption for message {message.message_id} with link: {telegraph_link}")
            else:
                logger.warning(f"Failed to generate Telegraph link for message {message.message_id}")
        except Exception as e:
            logger.error(f"Error processing message {message.message_id}: {e}")

# Handler to process the photo messages sequentially
@app.on_message(filters.photo & filters.chat(CHANNEL_ID))
async def handle_photo(client, message):
    logger.info(f"New photo received: {message.message_id}")
    
    # Store the message temporarily for processing later
    await process_photos_sequentially(client, [message])

# Run the bot
app.run()
