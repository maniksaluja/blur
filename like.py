from telethon import TelegramClient, events
from telethon.tl.types import InputPeerChannel

api_id = '26980824'  # Replace with your API ID
api_hash = 'fb044056059384d3bea54ab7ce915226'  # Replace with your API Hash
bot_token = "7041654616:AAHCsdChgpned-dlBEjv-OcOxSi_mY5HRjI"
channel_id = -1002374330304  # Your channel ID

client = TelegramClient('my_bot', api_id, api_hash).start(bot_token=bot_token)

# Monitor for new messages in the channel
@client.on(events.NewMessage(chats=channel_id))
async def handler(event):
    message = event.message
    print(f"New message ID: {message.id} received")
    
    try:
        # Add reactions (like/dislike) to every new post
        await message.add_reaction("👍")  # Like reaction
        await message.add_reaction("👎")  # Dislike reaction
        print(f"Reactions added to message ID: {message.id}")
    
    except Exception as e:
        print(f"Error: {e}")
        await asyncio.sleep(10)  # Sleep for 10 seconds before retrying
        print("Retrying after 10 seconds...")

client.start()
print("Bot is running...")
client.run_until_disconnected()
