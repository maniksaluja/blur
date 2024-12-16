import requests

def upload_image_to_telegraph(image_path):
    url = "https://telegra.ph/upload"
    
    # Open image and send POST request
    with open(image_path, 'rb') as file:
        response = requests.post(url, files={'file': ('file.jpg', file, 'image/jpeg')})

    # Check response status
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and len(result) > 0 and 'src' in result[0]:
            # Image URL
            image_url = f"https://telegra.ph{result[0]['src']}"
            print(f"Image uploaded successfully! URL: {image_url}")
            return image_url
        else:
            print("Failed to upload image to Telegraph.")
    else:
        print(f"Failed to upload image. Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

# Example usage
image_path = "/home/ubuntu/blur/downloads/AgACAgUAAyEFAASNhWfAAAIBM2dgIcWDncUSubLFx4i7H8ms4FA8AALBvzEbp7ABV-QBKxn64Ie9AAgBAAMCAAN5AAceBA.jpg"
upload_image_to_telegraph(image_path)
