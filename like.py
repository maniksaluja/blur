from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

TOKEN = '7041654616:AAHCsdChgpned-dlBEjv-OcOxSi_mY5HRjI'
CHAT_ID = '-1002374330304'
LIKE_EMOJI = '👍'
DISLIKE_EMOJI = '👎'
API_URL = f"https://api.telegram.org/bot{TOKEN}"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_reaction(chat_id, message_id, emoji):
    url = f"{API_URL}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': emoji,
        'reply_to_message_id': message_id
    }
    logging.info(f"Sending {emoji} to message ID {message_id}")
    response = requests.post(url, data=payload)
    response_data = response.json()
    if response_data.get('ok'):
        logging.info(f"Sent {emoji} to message ID {message_id} successfully.")
    else:
        logging.error(f"Failed to send {emoji} to message ID {message_id}. Error: {response_data.get('description')}")
    return response_data

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    update = request.get_json()
    if "channel_post" in update:
        message = update["channel_post"]
        message_id = message["message_id"]
        logging.info(f"New message found with ID {message_id}")
        send_reaction(CHAT_ID, message_id, LIKE_EMOJI)
        send_reaction(CHAT_ID, message_id, DISLIKE_EMOJI)
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(port=8443)
