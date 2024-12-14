import time
import requests

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
    return response.json()

def monitor_channel():
    last_message_id = None
    while True:
        # Get new messages from the channel
        new_messages = []  # Fetch new messages from Telegram API
        for message in new_messages:
            if message['message_id'] > last_message_id:
                send_reaction(CHAT_ID, message['message_id'], LIKE_EMOJI)
                send_reaction(CHAT_ID, message['message_id'], DISLIKE_EMOJI)
                time.sleep(1)  # Ensure we do not exceed rate limits
                last_message_id = message['message_id']

monitor_channel()
