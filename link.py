from pyrogram import Client, filters
from telegraph import Telegraph

# Telegram API details
api_id = '26980824'  # Replace with your API ID
api_hash = 'fb044056059384d3bea54ab7ce915226'  # Replace with your API Hash
bot_token = "7041654616:AAHCsdChgpned-dlBEjv-OcOxSi_mY5HRjI"
channel_id = -1002374330304  # Your channel ID

# Initialize Pyrogram Client
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Initialize Telegraph Client
telegraph = Telegraph()
telegraph.create_account(short_name='my_bot')

@app.on_message(filters.chat(channel_id) & filters.photo)
def photo_handler(client, message):
    try:
        # Get the file ID of the photo
        file_id = message.photo.file_id
        
        # Download the photo
        file = client.get_file(file_id)
        file_path = file.file_path
        
        # Upload to Telegraph
        response = telegraph.upload_file(file_path)
        
        # Get the URL of the uploaded photo
        photo_url = response[0]['src']
        
        # Create a page with the uploaded photo URL
        page = telegraph.create_page(
            title="Uploaded Photo",
            html_content=f"<img src='{photo_url}' />"
        )
        
        # Get the URL of the created page
        photo_link = f"https://telegra.ph/{page['path']}"
        
        # Edit the post in the channel with the link
        client.edit_message_caption(
            chat_id=message.chat.id,
            message_id=message.message_id,
            caption=f"Here is the uploaded photo: {photo_link}"
        )
        
        print("Photo link created successfully and caption updated.")
    
    except Exception as e:
        print(f"Error: {e}")

# Start the bot
app.run()
