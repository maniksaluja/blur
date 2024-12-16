import requests

# Telegram API URL for testing
api_url = "https://api.telegram.org/7041654616:AAHCsdChgpned-dlBEjv-OcOxSi_mY5HRjI/getMe"

# Make a request to the bot API to check if the bot is working
response = requests.get(api_url)

# Check if the response is successful
if response.status_code == 200:
    print("API is working. Response:", response.json())
else:
    print("API not working. Status Code:", response.status_code, "Response:", response.text)
