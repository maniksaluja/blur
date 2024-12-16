import requests

# Your bot token
bot_token = "7041654616:AAHCsdChgpned-dlBEjv-OcOxSi_mY5HRjI"
url = f"https://api.telegram.org/bot{bot_token}/getMe"

response = requests.get(url)

# Check if API is working
if response.status_code == 200:
    print("API is working.")
    print("Response:", response.json())
else:
    print(f"API not working. Status Code: {response.status_code}")
    print("Response:", response.json())
