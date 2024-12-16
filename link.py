from pyrogram import Client, filters
from telegraph import Telegraph
import os

api_id = '26980824'  # Replace with your API ID
api_hash = 'fb044056059384d3bea54ab7ce915226'  # Replace with your API Hash
bot_token = "7041654616:AAHCsdChgpned-dlBEjv-OcOxSi_mY5HRjI"
channel_id = -1002374330304  # Your channel ID

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Initialize Telegraph
telegraph = Telegraph()
telegraph.create_account(short_name='my_bot')

@app.on_message(filters.chat(channel_id) & filters.photo)
async def handle_photo(client, message):
    print("Photo received...")
    
    # Download the photo
    downloaded_file = await message.download(file_name=os.path.join("downloads", f"{message.photo.file_id}.jpg"))
    print(f"Downloaded file path: {downloaded_file}")
    
    try:
        # Upload image to Telegraph
        response = telegraph.upload_file([downloaded_file])
        
        if isinstance(response, list) and len(response) > 0:
            # Extract image URL
            image_url = f"https://telegra.ph{response[0]['src']}"
            print(f"Image uploaded successfully! URL: {image_url}")
            
            # Edit the post with the uploaded image URL
            caption = f"Check out this photo: {image_url}"
            await client.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id, caption=caption)
        else:
            print("Failed to upload image to Telegraph or response format is not valid")
    except Exception as e:
        print(f"Error: {str(e)}")

app.run()
