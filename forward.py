from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import time

# Bot Configuration
api_id = "YOUR_API_ID"
api_hash = "YOUR_API_HASH"
bot_token = "YOUR_BOT_TOKEN"

# Channel IDs (Make sure bot is added to both channels)
channel_1 = -1001234567890  # Channel 1 ID
channel_2 = -1009876543210  # Channel 2 ID

# Initialize Bot
app = Client("channel_forwarder_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.chat(channel_1) & ~filters.edited)
async def forward_to_channel(_, message):
    try:
        await message.forward(chat_id=channel_2)
    except FloodWait as e:
        print(f"FloodWait triggered! Sleeping for {e.value} seconds.")
        time.sleep(e.value)
    except Exception as ex:
        print(f"Error: {ex}")

print("Bot is running...")
app.run()
