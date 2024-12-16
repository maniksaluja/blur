from pyrogram import filters
from telegraph import Telegraph
from pyrogram import Client

# Initialize Telegram client
api_id = '26980824'  # Replace with your API ID
api_hash = 'fb044056059384d3bea54ab7ce915226'  # Replace with your API Hash
bot_token = "7041654616:AAHCsdChgpned-dlBEjv-OcOxSi_mY5HRjI"
channel_id = -1002374330304  # Your channel ID

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Initialize Telegraph API
telegraph = Telegraph()
telegraph.create_account(short_name="MyBot")

@app.on_message(filters.chat(channel_id) & filters.photo)
async def handle_photo(client, message):
    try:
        # Start processing the photo
        print("Photo received...")

        # Upload the photo to telegraph
        photo_file = await message.download()
        print(f"File path: {photo_file}")
        
        # Upload to Telegraph
        response = telegraph.upload(file=photo_file)
        print(f"Telegraph response: {response}")

        # Get the URL of the uploaded image
        image_url = response[0]['src']
        print(f"Image URL: {image_url}")

        # Edit the post with the URL in the caption
        await message.edit_caption(caption=f"Check out this image: {image_url}")

    except Exception as e:
        print(f"Error: {str(e)}")

app.run()
