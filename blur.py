import os
import time
from pymongo import MongoClient
from telethon import TelegramClient, events, Button
from io import BytesIO
from PIL import Image, ImageFilter
import asyncio

# MongoDB setup
MONGO_URL = "mongodb+srv://manik:manik11@cluster0.iam3w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URL)
db = client['your_database_name']
collection = db['photos_collection']
collection.create_index([("timestamp", 1)], expireAfterSeconds=2592000)  # TTL index

# Telegram Bot setup
api_id = '26980824'
api_hash = 'fb044056059384d3bea54ab7ce915226'
bot_token = '7041654616:AAHqmt9LKjTL9lRAXj8HT_ZkjaWW9I-hz3Q'
CHANNEL_ID = -1002374330304
USER_ID = 817321875
BLUR_PERCENTAGE = 80
BLUR_DELAY = 60

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
forwarded_message_ids = {}

# Image Blurring
def blur_image(image_data):
    img = Image.open(image_data)
    img = img.convert("RGB")
    blurred_image = img.filter(ImageFilter.GaussianBlur(BLUR_PERCENTAGE))
    temp_file = "temp_blurred.jpg"
    blurred_image.save(temp_file, format="JPEG")
    return temp_file

# MongoDB Operations
def insert_photo_data(message_id):
    collection.insert_one({
        "message_id": message_id,
        "media_type": "photo",
        "timestamp": int(time.time()),
        "status": "pending",
        "blurred_timestamp": None
    })

def update_blurred_status(message_id):
    collection.update_one({"message_id": message_id}, {"$set": {"status": "blurred", "blurred_timestamp": int(time.time())}})

def delete_photo_data(message_id):
    collection.delete_one({"message_id": message_id})

# Event Handlers
@client.on(events.NewMessage(chats=CHANNEL_ID))
async def forward_media_to_user(event):
    if event.photo:
        print(f"New photo detected (ID: {event.id})")
        forwarded_msg = await client.forward_messages(USER_ID, event.message)
        blur_button_msg = await client.send_message(
            USER_ID,
            "Photo forwarded. Choose an action:",
            buttons=[
                Button.inline("Blur", data=f"blur_{event.id}"),
                Button.inline("Delay Blur", data=f"delay_{event.id}")
            ]
        )
        forwarded_message_ids[event.id] = (forwarded_msg.id, blur_button_msg.id)
        insert_photo_data(event.id)

@client.on(events.CallbackQuery)
async def handle_blur_action(event):
    try:
        data = event.data.decode('utf-8')
        action, msg_id = data.split('_')
        msg_id = int(msg_id)
        print(f"Action '{action}' selected for message ID: {msg_id}")

        async for message in client.iter_messages(CHANNEL_ID, ids=msg_id):
            if not message or not message.photo:
                await event.answer("Photo not found!")
                return

            photo = await message.download_media(file=BytesIO())
            if action == "delay":
                await event.answer(f"Blurring in {BLUR_DELAY} seconds.")
                await asyncio.sleep(BLUR_DELAY)
            elif action == "blur":
                await event.answer("Blurring photo...")

            temp_file = blur_image(photo)
            try:
                with open(temp_file, 'rb') as f:
                    await client.edit_message(CHANNEL_ID, msg_id, file=f)
                update_blurred_status(msg_id)
                print("Photo blurred and replaced.")
            finally:
                if os.path.exists(temp_file):
                    os.remove(temp_file)

            if msg_id in forwarded_message_ids:
                fwd_id, btn_id = forwarded_message_ids.pop(msg_id, (None, None))
                await client.delete_messages(USER_ID, [fwd_id, btn_id])
                print("DM messages deleted.")

            delete_photo_data(msg_id)
            break
    except Exception as e:
        print(f"Error: {e}")
        await event.answer("An error occurred.")

client.start()
client.run_until_disconnected()
