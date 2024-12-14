import os
import time
from pymongo import MongoClient
from telethon import TelegramClient, events, Button
from io import BytesIO
from PIL import Image, ImageFilter
import asyncio
import logging

# MongoDB Setup
MONGO_URL = "mongodb+srv://manik:manik11@cluster0.iam3w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Logging setup
logging.basicConfig(level=logging.INFO)

# Telegram Bot Setup
api_id = '26980824'
api_hash = 'fb044056059384d3bea54ab7ce915226'
bot_token = '7041654616:AAHqmt9LKjTL9lRAXj8HT_ZkjaWW9I-hz3Q'
CHANNEL_ID = -1002374330304
USER_ID = 817321875  # Replace with your user ID
BLUR_PERCENTAGE = 10
BLUR_DELAY = 60  # Delay in seconds

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

forwarded_message_ids = {}

# MongoDB Connection
def get_db_connection():
    try:
        client = MongoClient(MONGO_URL)
        db = client['your_database_name']  # Replace with your database name
        collection = db['photos_collection']  # Collection for photos
        collection.create_index([("timestamp", 1)], expireAfterSeconds=2592000)  # TTL: 30 days
        return collection
    except Exception as e:
        logging.error(f"MongoDB connection error: {e}")
        raise

# Helper to blur images
def blur_image(image_data):
    try:
        img = Image.open(image_data)
        img = img.convert("RGB")
        blurred_image = img.filter(ImageFilter.GaussianBlur(BLUR_PERCENTAGE))
        temp_file = "temp_blurred.jpg"
        blurred_image.save(temp_file, format="JPEG")
        return temp_file
    except Exception as e:
        logging.error(f"Error blurring image: {e}")
        raise

# Insert photo data into MongoDB
def insert_photo_data(collection, message_id, delay=False, delay_time=None):
    try:
        timestamp = int(time.time())
        data = {
            "message_id": message_id,
            "media_type": "photo",
            "timestamp": timestamp,
            "status": "pending",
            "blurred_timestamp": None,
            "delay": delay,
            "delay_time": delay_time,
        }
        collection.insert_one(data)
        logging.info(f"Inserted data for photo with message ID {message_id}")
    except Exception as e:
        logging.error(f"Error inserting photo data: {e}")

# Update status to blurred
def update_blurred_status(collection, message_id):
    try:
        collection.update_one(
            {"message_id": message_id},
            {"$set": {"status": "blurred", "blurred_timestamp": int(time.time())}}
        )
        logging.info(f"Photo with message ID {message_id} marked as blurred")
    except Exception as e:
        logging.error(f"Error updating blurred status for message ID {message_id}: {e}")

# Delete photo data
def delete_photo_data(collection, message_id):
    try:
        collection.delete_one({"message_id": message_id})
        logging.info(f"Photo with message ID {message_id} data deleted from database")
    except Exception as e:
        logging.error(f"Error deleting photo data for message ID {message_id}: {e}")

# Forward photo to USER_ID with buttons
@client.on(events.NewMessage(chats=CHANNEL_ID))
async def forward_media_to_user(event):
    if event.photo:
        try:
            logging.info(f"New photo detected in channel (ID: {event.id})")
            forwarded_msg = await client.forward_messages(USER_ID, event.message)
            logging.info("Photo forwarded to USER_ID")

            blur_button_msg = await client.send_message(
                USER_ID,
                "Photo forwarded to you. Do you want to blur it?",
                buttons=[Button.inline("Blur", data=str(event.id)), Button.inline("Delay Blur", data=f"delay_{event.id}")]
            )

            forwarded_message_ids[event.id] = (forwarded_msg.id, blur_button_msg.id)

            collection = get_db_connection()
            insert_photo_data(collection, event.id)

        except Exception as e:
            logging.error(f"Error in forwarding media: {e}")

# Blur photo instantly
async def blur_photo(client, msg_id, collection):
    try:
        async for message in client.iter_messages(CHANNEL_ID, ids=msg_id):
            if message and message.photo:
                logging.info(f"Blurring photo for message ID: {msg_id}")
                photo = await message.download_media(file=BytesIO())
                temp_file = blur_image(photo)

                with open(temp_file, 'rb') as f:
                    await client.edit_message(CHANNEL_ID, msg_id, file=f)
                logging.info(f"Photo replaced in channel for message ID: {msg_id}")

                update_blurred_status(collection, msg_id)
                if msg_id in forwarded_message_ids:
                    forwarded_id, button_id = forwarded_message_ids[msg_id]
                    await client.delete_messages(USER_ID, [forwarded_id, button_id])
                    del forwarded_message_ids[msg_id]

                delete_photo_data(collection, msg_id)
            else:
                logging.warning(f"No photo found for message ID: {msg_id}")
    except Exception as e:
        logging.error(f"Error blurring photo: {e}")

# Handle Blur button click
@client.on(events.CallbackQuery)
async def handle_callback(event):
    try:
        data = event.data.decode('utf-8')
        if data.isdigit():
            msg_id = int(data)
            logging.info(f"Blur button clicked for message ID: {msg_id}")
            collection = get_db_connection()
            await blur_photo(client, msg_id, collection)
            await event.answer("Photo blurred successfully!")
        elif data.startswith('delay_'):
            msg_id = int(data.split('_')[1])
            delay_time = int(time.time()) + BLUR_DELAY
            logging.info(f"Delay Blur button clicked for message ID: {msg_id}, scheduled at {delay_time}")
            collection = get_db_connection()
            insert_photo_data(collection, msg_id, delay=True, delay_time=delay_time)
            await event.answer(f"Photo will be blurred after {BLUR_DELAY} seconds!")
    except Exception as e:
        logging.error(f"Error handling callback: {e}")
        await event.answer("Error processing your request.")

# Process delayed blur tasks
async def process_delay_tasks(collection):
    while True:
        try:
            current_time = int(time.time())
            tasks = collection.find({"delay": True, "delay_time": {"$lte": current_time}})
            for task in tasks:
                msg_id = task["message_id"]
                logging.info(f"Processing delayed blur for message ID: {msg_id}")
                await blur_photo(client, msg_id, collection)
                collection.update_one({"message_id": msg_id}, {"$set": {"delay": False}})
        except Exception as e:
            logging.error(f"Error processing delayed blur tasks: {e}")
        await asyncio.sleep(30)  # Check every 30 seconds

# Start the bot and process delay tasks
async def main():
    try:
        logging.info("Bot started.")
        collection = get_db_connection()  # MongoDB connection
        asyncio.create_task(process_delay_tasks(collection))  # Pass collection to the task
        await client.run_until_disconnected()
    except Exception as e:
        logging.error(f"Bot error: {e}")

# Start the main function without asyncio.run
client.loop.create_task(main())
client.start()
