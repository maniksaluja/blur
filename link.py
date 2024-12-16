from pyrogram import Client, filters
import requests
import os
from PIL import Image

api_id = '26980824'  # Replace with your API ID
api_hash = 'fb044056059384d3bea54ab7ce915226'  # Replace with your API Hash
bot_token = "7041654616:AAHCsdChgpned-dlBEjv-OcOxSi_mY5HRjI"
channel_id = -1002374330304  # Your channel ID
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.on_message(filters.chat(channel_id) & filters.photo)
async def handle_photo(client, message):
    print("Photo received...")
    
    # Download the photo
    downloaded_file = await message.download(file_name=os.path.join("downloads", f"{message.photo.file_id}.jpg"))
    print(f"Downloaded file path: {downloaded_file}")

    if not allowed_file(downloaded_file):
        print("File format not supported. Only jpg, jpeg, and png formats are allowed.")
        return

    try:
        # Check file size
        file_size = os.path.getsize(downloaded_file)
        if file_size > MAX_FILE_SIZE:
            # Compress the image
            image = Image.open(downloaded_file)
            compressed_file = os.path.join("downloads", f"{message.photo.file_id}_compressed.jpg")
            image.save(compressed_file, "JPEG", quality=85)
            downloaded_file = compressed_file
            print(f"Compressed file path: {downloaded_file}")

        # Upload image to Telegraph using HTTP POST request
        with open(downloaded_file, 'rb') as file:
            response = requests.post('https://telegra.ph/upload', files={'file': file})
        
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")

        if response.status_code == 200:
            result = response.json()
            print(f"Response JSON: {result}")

            if isinstance(result, list) and len(result) > 0 and 'src' in result[0]:
                # Extract image URL
                image_url = f"https://telegra.ph{result[0]['src']}"
                print(f"Image uploaded successfully! URL: {image_url}")
                
                # Send a new message with the uploaded image URL
                caption = f"Check out this photo: {image_url}"
                await client.send_message(chat_id=message.chat.id, text=caption)
            else:
                print("Failed to upload image to Telegraph or response format is not valid")
        else:
            print(f"Failed to upload image to Telegraph. Status Code: {response.status_code}")
            print(f"Response Headers: {response.headers}")
            print(f"Response Text: {response.text}")
    except Exception as e:
        print(f"Error: {str(e)}")

app.run()
