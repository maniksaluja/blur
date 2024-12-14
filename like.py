from pyrogram import Client, filters
import asyncio

# Bot token aur channel ID
bot_token = "7041654616:AAHqmt9LKjTL9lRAXj8HT_ZkjaWW9I-hz3Q"
channel_id = -1002374330304  # Aapka channel ID

app = Client("my_bot", bot_token=bot_token)

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
