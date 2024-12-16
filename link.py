import requests
import os

def upload_image_to_telegraph(image_path):
    url = "https://telegra.ph/upload"
    
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            print(f"File does not exist: {image_path}")
            return None
        
        # Get file size and type
        file_size = os.path.getsize(image_path)
        print(f"File Size: {file_size / (1024 * 1024):.2f} MB")  # Convert bytes to MB
        if file_size > 5 * 1024 * 1024:  # Limit to 5MB for upload
            print("File size is too large. Maximum allowed size is 5MB.")
            return None
        
        # Check file type (assuming it should be an image)
        file_extension = image_path.split('.')[-1].lower()
        print(f"File Extension: {file_extension}")
        allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
        if file_extension not in allowed_extensions:
            print(f"Invalid file type. Allowed types are: {allowed_extensions}")
            return None
        
        # Open image and send POST request with custom headers for better handling
        with open(image_path, 'rb') as file:
            files = {'file': ('file.jpg', file, f'image/{file_extension}')}
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            }
            response = requests.post(url, files=files, headers=headers)
        
        print(f"Response Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        
        # Check if the response is valid
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0 and 'src' in result[0]:
                image_url = f"https://telegra.ph{result[0]['src']}"
                print(f"Image uploaded successfully! URL: {image_url}")
                return image_url
            else:
                print("Failed to upload image. Invalid response format.")
        else:
            print(f"Failed to upload image. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
        return None
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

# Example usage
image_path = "/home/ubuntu/blur/downloads/AgACAgUAAyEFAASNhWfAAAIBM2dgIcWDncUSubLFx4i7H8ms4FA8AALBvzEbp7ABV-QBKxn64Ie9AAgBAAMCAAN5AAceBA.jpg"
upload_image_to_telegraph(image_path)
