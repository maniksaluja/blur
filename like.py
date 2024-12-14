import time
import requests
import logging

# Logging setup kar rahe hain
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TOKEN = '7041654616:AAHCsdChgpned-dlBEjv-OcOxSi_mY5HRjI'
CHAT_ID = '-1002374330304'
LIKE_EMOJI = '👍'
API_URL = f"https://api.telegram.org/bot{TOKEN}"
START_MESSAGE = "Bot has started!"

def send_message(chat_id, text):
    url = f"{API_URL}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    logging.info(f"Sending start message to chat ID {chat_id}")
    try:
        response = requests.post(url, data=payload)
        response_data = response.json()
        if response_data.get('ok'):
            message_id = response_data['result']['message_id']
            logging.info(f"Sent message to chat ID {chat_id} successfully with message ID {message_id}")
            return message_id
        else:
            logging.error(f"Failed to send message to chat ID {chat_id}. Error: {response_data.get('description')}")
            return None
    except Exception as e:
        logging.error(f"Exception occurred while sending message to chat ID {chat_id}: {e}")
        return None

def send_reaction(chat_id, message_id, emoji):
    url = f"{API_URL}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': emoji,
        'reply_to_message_id': message_id
    }
    logging.info(f"Sending {emoji} to message ID {message_id}")
    try:
        response = requests.post(url, data=payload)
        response_data = response.json()
        if response_data.get('ok'):
            logging.info(f"Sent {emoji} to message ID {message_id} successfully.")
        else:
            logging.error(f"Failed to send {emoji} to message ID {message_id}. Error: {response_data.get('description')}")
        return response_data
    except Exception as e:
        logging.error(f"Exception occurred while sending {emoji} to message ID {message_id}: {e}")

def get_updates(offset=None):
    url = f"{API_URL}/getUpdates"
    params = {'offset': offset, 'timeout': 100}
    logging.info("Fetching updates")
    try:
        response = requests.get(url, params=params)
        response_data = response.json()
        if response_data.get('ok'):
            logging.info("Fetched updates successfully.")
        else:
            logging.error(f"Failed to fetch updates. Error: {response_data.get('description')}")
        return response_data
    except Exception as e:
        logging.error(f"Exception occurred while fetching updates: {e}")
        return {}

def monitor_channel(start_message_id):
    last_update_id = None
    while True:
        logging.info("Checking for new updates")
        updates = get_updates(last_update_id)
        if updates.get("ok"):
            for update in updates["result"]:
                if "channel_post" in update:
                    message = update["channel_post"]
                    message_id = message["message_id"]
                    if message_id > start_message_id:
                        logging.info(f"New message found with ID {message_id}")
                        send_reaction(CHAT_ID, message_id, LIKE_EMOJI)
                    last_update_id = update["update_id"] + 1
        time.sleep(1)  # Ensure we do not exceed rate limits

def main():
    start_message_id = send_message(CHAT_ID, START_MESSAGE)
    if start_message_id:
        monitor_channel(start_message_id)
    else:
        logging.error("Failed to send start message. Exiting.")

if __name__ == "__main__":
    main()
