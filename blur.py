import os
import time
from pymongo import MongoClient
from telethon import TelegramClient, events, Button
from io import BytesIO
from PIL import Image, ImageFilter
import asyncio

# MongoDB URL and connection setup
MONGO_URL = "mongodb+srv://manik:manik11@cluster0.iam3w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URL)
db = client['your_database_name']  # Replace with your database name
collection = db['photos_collection']  # Collection for photos

# MongoDB TTL index (30 days)
collection.create_index([("timestamp", 1)], expireAfterSeconds=2592000)  # TTL of 30 days (in seconds)

# Telegram Bot API setup
api_id = '26980824'
api_hash = 'fb044056059384d3bea54ab7ce915226'
bot_token = '7041654616:AAHqmt9LKjTL9lRAXj8HT_ZkjaWW9I-hz3Q'
CHANNEL_ID = -1002374330304
USER_ID = 817321875  # Replace with your user ID
BLUR_PERCENTAGE = 80  # Adjust blur intensity here (higher for stronger blur)
BLUR_DELAY = 60  # Time delay before applying blur (in seconds, set to 60 seconds)

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Store forwarded and blur button message IDs for each event
forwarded_message_ids = {}

# Helper function to blur images
def blur_image(image_data):
    img = Image.open(image_data)
    img = img.convert("RGB")  # Ensure compatibility for JPEG
    blurred_image = img.filter(ImageFilter.GaussianBlur(BLUR_PERCENTAGE))
    temp_file = "temp_blurred.jpg"
    blurred_image.save(temp_file, format="JPEG")
    return temp_file

# Insert photo data into MongoDB
def insert_photo_data(message_id, file_path=None):
    timestamp = int(time.time())  # Current timestamp
    
    data = {
        "message_id": message_id,
        "media_type": "photo",  # Fixed for photo
        "timestamp": timestamp,
        "status": "pending",  # Initially set to pending
        "blurred_timestamp": None,  # No blur initially
        "file_path": file_path  # Optional, store file path if needed
    }
    
    collection.insert_one(data)
    print(f"Inserted data for photo with message ID {message_id}")

# Update status to blurred after photo blur
def update_blurred_status(message_id):
    collection.update_one(
        {"message_id": message_id},
        {"$set": {"status": "blurred", "blurred_timestamp": int(time.time())}}
    )
    print(f"Photo with message ID {message_id} marked as blurred")

# Delete photo data after blur operation is complete
def delete_photo_data(message_id):
    collection.delete_one({"message_id": message_id})
    print(f"Photo with message ID {message_id} data deleted from database")

# Telegram Event to forward media to user
@client.on(events.NewMessage(chats=CHANNEL_ID))
async def forward_media_to_user(event):
    if event.photo:
        print(f"New photo detected in channel (ID: {event.id})")

        # Forward message to user
        forwarded_msg = await client.forward_messages(USER_ID, event.message)
        print("Photo forwarded to USER_ID")

        # Send a blur button after forwarding
        blur_button_msg = await client.send_message(
            USER_ID,
            "Photo forwarded to you. Do you want to blur it?",
            buttons=[Button.inline("Blur", data=str(event.id)), Button.inline("Delay Blur", data=f"delay_{event.id}")]
        )

        # Save forwarded and blur button message IDs
        forwarded_message_ids[event.id] = (forwarded_msg.id, blur_button_msg.id)

        # Insert photo data into MongoDB
        insert_photo_data(event.id)

# Callback to handle blur button click
@client.on(events.CallbackQuery)
async def blur_media(event):
    if event.data:
        msg_id = int(event.data.decode('utf-8'))
        print(f"Blur button clicked for message ID: {msg_id}")

        # Fetch original photo
        try:
            async for message in client.iter_messages(CHANNEL_ID, ids=msg_id):
                if message and message.photo:
                    print("Original photo found in channel")
                    photo = await message.download_media(file=BytesIO())
                    await event.answer("Photo blurred successfully!")

                    # Apply blur and replace the photo in the channel
                    temp_file = blur_image(photo)
                    try:
                        with open(temp_file, 'rb') as f:
                            await client.edit_message(CHANNEL_ID, msg_id, file=f)
                        print("Photo replaced in channel")

                        # Update MongoDB status to blurred
                        update_blurred_status(msg_id)

                        # Delete forwarded and blur button messages from user's DM
                        if msg_id in forwarded_message_ids:
                            forwarded_id, button_id = forwarded_message_ids[msg_id]
                            try:
                                await client.delete_messages(USER_ID, [forwarded_id, button_id])
                                print("Blur button and forwarded message deleted from user DM")
                            except Exception as e:
                                print(f"Error deleting messages from user DM: {e}")
                            finally:
                                del forwarded_message_ids[msg_id]

                    except Exception as e:
                        await event.answer("Failed to replace photo in channel.")
                        print(f"Error replacing photo in channel: {e}")

                    # Delete the photo data after blur operation
                    delete_photo_data(msg_id)
                else:
                    await event.answer("No photo found for blurring!")
                    return
        except Exception as e:
            await event.answer("Failed to fetch photo for blurring.")
            print(f"Error fetching photo: {e}")

# Callback to handle delay blur button click (Delay time is set in BLUR_DELAY)
@client.on(events.CallbackQuery)
async def delay_blur_media(event):
    if event.data:
        msg_id = int(event.data.decode('utf-8').split('_')[1])
        print(f"Delay Blur button clicked for message ID: {msg_id}")

        # Fetch original photo
        try:
            async for message in client.iter_messages(CHANNEL_ID, ids=msg_id):
                if message and message.photo:
                    print("Original photo found in channel")
                    photo = await message.download_media(file=BytesIO())
                    await event.answer(f"Photo will be blurred after {BLUR_DELAY} seconds!")

                    # Wait for delay time before blurring
                    await asyncio.sleep(BLUR_DELAY)  # Time delay before applying blur

                    # Apply blur after delay
                    temp_file = blur_image(photo)
                    # Replace the original photo in the channel
                    try:
                        with open(temp_file, 'rb') as f:
                            await client.edit_message(CHANNEL_ID, msg_id, file=f)
                        print("Photo replaced in channel")

                        # Update MongoDB status to blurred
                        update_blurred_status(msg_id)

                        # Delete forwarded and blur button messages from user's DM
                        if msg_id in forwarded_message_ids:
                            forwarded_id, button_id = forwarded_message_ids[msg_id]
                            try:
                                await client.delete_messages(USER_ID, [forwarded_id, button_id])
                                print("Blur button and forwarded message deleted from user DM")
                            except Exception as e:
                                print(f"Error deleting messages from user DM: {e}")
                            finally:
                                del forwarded_message_ids[msg_id]

                    except Exception as e:
                        await event.answer("Failed to replace photo in channel.")
                        print(f"Error replacing photo in channel: {e}")

                    # Delete the photo data after blur operation
                    delete_photo_data(msg_id)
                else:
                    await event.answer("No photo found for blurring!")
                    return
        except Exception as e:
            await event.answer("Failed to fetch photo for blurring.")
            print(f"Error fetching photo: {e}")

client.start()
client.run_until_disconnected()
