import requests

# Make a simple GET request to the API to check if it's reachable
response = requests.get('https://telegra.ph/')
if response.status_code == 200:
    print("Telegraph API is working.")
else:
    print(f"Telegraph API returned status code: {response.status_code}")
