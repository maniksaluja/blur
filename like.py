import time
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

TOKEN = '7041654616:AAHqmt9LKjTL9lRAXj8HT_ZkjaWW9I-hz3Q'
CHAT_ID = '-1002374330304'
LIKE_EMOJI = '👍'
DISLIKE_EMOJI = '👎'

def send_reaction(chat_id, message_id, emoji):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': emoji,
        'reply_to_message_id': message_id
    }
    response = requests.post(url, data=payload)
    logging.info(f"Response: {response.json()}")
    return response.json()

def monitor_channel():
    last_message_id = None
    while True:
        # Get new messages from the channel (this part should be implemented with Telegram API calls)
        new_messages = []  # Placeholder for fetched messages
        for message in new_messages:
            if message['message_id'] > last_message_id:
                result = send_reaction(CHAT_ID, message['message_id'], LIKE_EMOJI)
                if result['ok']:
                    send_reaction(CHAT_ID, message['message_id'], DISLIKE_EMOJI)
                else:
                    logging.error(f"Error sending like: {result['description']}")
                time.sleep(1)  # Ensure we do not exceed rate limits
                last_message_id = message['message_id']

monitor_channel()
