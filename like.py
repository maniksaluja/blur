from pyrogram import Client, filters
import asyncio

# Telegram API details
api_id = '26980824'  # Replace with your API ID
api_hash = 'fb044056059384d3bea54ab7ce915226'  # Replace with your API Hash
bot_token = "7041654616:AAHqmt9LKjTL9lRAXj8HT_ZkjaWW9I-hz3Q"
channel_id = -1002374330304  # Your channel ID

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# New Post Par Reactions Add Karna
@app.on_message(filters.text & filters.chat(channel_id))
async def add_reactions(client, message):
    try:
        # Reaction ko add karna (Like aur Dislike)
        await message.react("👍")  # Like reaction
        await message.react("👎")  # Dislike reaction
    except Exception as e:
        print(f"Error: {e}")
        # FloodWait ko handle karne ke liye
        await asyncio.sleep(10)  # Sleep for 10 seconds before retrying
        await add_reactions(client, message)

@app.on_message(filters.text & filters.chat(channel_id))
async def handle_new_post(client, message):
    # Reactions ko automatically add karenge jab new post ho
    await add_reactions(client, message)

app.run()
