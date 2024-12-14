import time
import requests
import logging

# Logging setup kar rahe hain
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TOKEN = '7041654616:AAHCsdChgpned-dlBEjv-OcOxSi_mY5HRjI'
CHAT_ID = '-1002374330304'
LIKE_EMOJI = '👍'
DISLIKE_EMOJI = '👎'
API_URL = f"https://api.telegram.org/bot{TOKEN}"

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

def monitor_channel():
    last_update_id = None
    while True:
        logging.info("Checking for new updates")
        updates = get_updates(last_update_id)
        if updates.get("ok"):
            for update in updates["result"]:
                if "channel_post" in update:
                    message = update["channel_post"]
                    message_id = message["message_id"]
                    logging.info(f"New message found with ID {message_id}")

                    # Ensuring the message actually exists before sending reaction
                    try:
                        response = requests.get(f"{API_URL}/getChatMessage", params={"chat_id": CHAT_ID, "message_id": message_id})
                        if response.status_code == 200:
                            logging.info(f"Message ID {message_id} exists. Sending reactions.")
                            send_reaction(CHAT_ID, message_id, LIKE_EMOJI)
                            send_reaction(CHAT_ID, message_id, DISLIKE_EMOJI)
                        else:
                            logging.error(f"Message ID {message_id} does not exist or could not be fetched. Response: {response.text}")
                    except Exception as e:
                        logging.error(f"Exception occurred while verifying message ID {message_id}: {e}")

                last_update_id = update["update_id"] + 1
        time.sleep(1)  # Rate limit exceed na ho, isliye sleep kar rahe hain

monitor_channel()
