import requests

def check_telegraph_api():
    # Image file path ko sahi tarah se specify karein
    image_path = '/home/ubuntu/blur/downloads/AgACAgUAAyEFAASNhWfAAAIBQGdgKnurXUHjwlFMiumb17PpnMGIAAPAMRunsAFXUiNZfqIiAW0ACAEAAwIAA3gABx4E.jpg'  # Example image

    # File ko open karna
    with open(image_path, 'rb') as file:
        # Telegraph API par POST request bhejna
        response = requests.post('https://telegra.ph/upload', files={'file': ('image.jpg', file, 'image/jpeg')})

    # Response ka status check karna
    if response.status_code == 200:
        print("API Working: Image uploaded successfully!")
        result = response.json()  # API response ko json format mein convert karna
        if isinstance(result, list) and len(result) > 0 and 'src' in result[0]:
            image_url = f"https://telegra.ph{result[0]['src']}"
            print(f"Image URL: {image_url}")
        else:
            print("Error: Unexpected response from API")
    else:
        print(f"API not working. Status Code: {response.status_code}")
        print(f"Response: {response.text}")

# Call the function to check API status
check_telegraph_api()
