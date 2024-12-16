import requests

def upload_text_to_telegraph(title, content):
    url = "https://api.telegra.ph/createPage"
    
    # Preparing the data payload for the text
    data = {
        'title': title,
        'content': f'[{{"tag":"p","children":["{content}"]}}]',
        'author_name': 'Your Bot Name',  # Optional
        'author_url': 'https://yourwebsite.com',  # Optional
    }
    
    try:
        # Sending POST request
        response = requests.post(url, data=data)
        
        print(f"Response Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if 'result' in result:
                page_url = result['result']['url']
                print(f"Text uploaded successfully! URL: {page_url}")
                return page_url
            else:
                print("Failed to upload text. Invalid response format.")
        else:
            print(f"Failed to upload text. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

# Example usage
title = "Sample Title"
content = "This is a test text for uploading on Telegraph."
upload_text_to_telegraph(title, content)
