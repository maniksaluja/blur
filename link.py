from pyrogram import Client, filters
import requests
import os

api_id = '26980824'  # Replace with your API ID
api_hash = 'fb044056059384d3bea54ab7ce915226'  # Replace with your API Hash
bot_token = "7041654616:AAHCsdChgpned-dlBEjv-OcOxSi_mY5HRjI"
channel_id = -1002374330304  # Your channel ID

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.chat(channel_id) & filters.photo)
async def handle_photo(client, message):
    print("Photo received...")
    
    # Download the photo
    downloaded_file = await message.download(file_name=os.path.join("downloads", f"{message.photo.file_id}.jpg"))
    print(f"Downloaded file path: {downloaded_file}")

    try:
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
            print(f"Response Text: {response.text}")
    except Exception as e:
        print(f"Error: {str(e)}")

app.run()
