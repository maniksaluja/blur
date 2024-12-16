import requests

# Define the URL for the Telegraph API
TELEGRAPH_API_URL = 'https://telegra.ph/upload'

# Path to the image you want to upload (change this path according to your image location)
image_path = 'path_to_your_image.jpg'

# Open the image file to send it to the API
try:
    with open(image_path, 'rb') as image_file:
        # Sending the image to the Telegraph API
        response = requests.post(TELEGRAPH_API_URL, files={'file': ('image.jpg', image_file, 'image/jpeg')})

        # Checking the response status code
        if response.status_code == 200:
            print("API is working correctly.")
            try:
                # Parsing the JSON response if available
                response_json = response.json()
                if isinstance(response_json, list) and len(response_json) > 0 and 'src' in response_json[0]:
                    image_url = f"https://telegra.ph{response_json[0]['src']}"
                    print(f"Image uploaded successfully! URL: {image_url}")
                else:
                    print("Failed to parse the image URL from the response.")
            except ValueError:
                print("Invalid JSON response.")
        else:
            print(f"API failed with status code: {response.status_code}")
            print(f"Error response: {response.text}")

except FileNotFoundError:
    print("The specified image file does not exist.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
