import time
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pymongo import MongoClient, ASCENDING

# Bot Token aur Channel ID
bot_token = "7041654616:AAHCsdChgpned-dlBEjv-OcOxSi_mY5HRjI"  # Yahan apna bot token daalna hai
channel_id = "-1002374330304"  # Yahan apna channel ID daalna hoga

# MongoDB setup (with TTL index)
mongo_client = MongoClient("mongodb+srv://manik:manik11@cluster0.iam3w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = mongo_client['your_db']
collection = db['message_logs']

# Create TTL index on 'time' field, documents will expire after 7 days (604800 seconds)
collection.create_index([('time', ASCENDING)], expireAfterSeconds=604800)  # 7 days = 604800 seconds

# Telegram client
app = Client("my_bot", bot_token=bot_token)

# Variables for old and new text
old_text = "hello"
new_text = "by"

# Function to replace text
async def replace_text_in_channel(message):
    try:
        if old_text in message.text:
            # Replace old text with new text
            new_message = message.text.replace(old_text, new_text)
            await message.edit(new_message)  # Edit the message with new text

            # Log the change in MongoDB (store old message text)
            collection.insert_one({
                "old_text": message.text,  # Save the old message text
                "new_text": new_message,   # Save the new message text
                "time": time.time()        # Timestamp for when the change occurred
            })
            print("Message updated and logged successfully")

    except FloodWait as e:
        print(f"Flood wait: Sleeping for {e.x} seconds")
        time.sleep(e.x)  # Handle FloodWait
        await replace_text_in_channel(message)  # Retry after waiting

@app.on_message(filters.chat(channel_id) & filters.text)
async def on_message(client, message):
    await replace_text_in_channel(message)

app.run()
