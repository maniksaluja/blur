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
    print("New message received")  # Log when a new message is received
    try:
        print("Adding reactions...")  # Log before adding reactions
        
        # Ensure the message is from the right channel and not already reacted
        if not message.from_user.is_bot:
            # Send reaction (Like or Dislike)
            await message.react("👍")  # Like reaction
            await message.react("👎")  # Dislike reaction
            print("Reactions added successfully!")  # Log success
        else:
            print("Ignoring bot message...")  # Ignore bot messages

    except Exception as e:
        print(f"Error: {e}")  # Log error if it occurs
        # FloodWait ko handle karne ke liye
        await asyncio.sleep(10)  # Sleep for 10 seconds before retrying
        print("Retrying after 10 seconds...")  # Log retry
        await add_reactions(client, message)

@app.on_message(filters.text & filters.chat(channel_id))
async def handle_new_post(client, message):
    print("Handling new post...")  # Log when handling new post
    # Reactions ko automatically add karenge jab new post ho
    await add_reactions(client, message)

print("Bot is starting...")  # Log when bot starts
app.run()
