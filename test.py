import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMediaDocument

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Bot initialization
app = Client("my_bot", bot_token="7099022623:AAHF5XCTdVgREoJWvK6sRJedYIso35E0XpE")

# Channel ID or username
channel_id = "-1002385675587"

# Callback function when the button is pressed
@app.on_callback_query()
def on_button_click(client, callback_query):
    try:
        if callback_query.data == "open_dm":
            logger.info(f"User {callback_query.from_user.id} clicked 'Open DM' button.")
            callback_query.message.reply_text("Opening your DM...")
            client.send_message(callback_query.from_user.id, "https://t.me/CuteGirlTG")
            callback_query.answer()
            logger.info(f"DM link sent to {callback_query.from_user.id}.")
    except Exception as e:
        logger.error(f"Error in on_button_click: {e}")

# Function to monitor new posts in the channel
@app.on_message(filters.channel & filters.chat(channel_id))
def on_new_post(client, message):
    try:
        logger.debug(f"Received new message in channel {channel_id}. Message ID: {message.message_id}")

        if message.photo:  # If the message contains a photo
            logger.debug(f"Photo found in message ID: {message.message_id}")
            button = InlineKeyboardButton("Open DM", url="https://t.me/CuteGirlTG")
            keyboard = InlineKeyboardMarkup([[button]])

            # Add the button to the photo message
            client.edit_message_media(
                chat_id=message.chat.id,
                message_id=message.message_id,
                media=InputMediaPhoto(message.photo.file_id),
                reply_markup=keyboard
            )
            logger.info(f"Button added to photo message ID: {message.message_id}")
        
        elif message.document:  # If the message contains a document
            logger.debug(f"Document found in message ID: {message.message_id}")
            button = InlineKeyboardButton("Open DM", url="https://t.me/CuteGirlTG")
            keyboard = InlineKeyboardMarkup([[button]])

            # Add the button to the document message
            client.edit_message_media(
                chat_id=message.chat.id,
                message_id=message.message_id,
                media=InputMediaDocument(message.document.file_id),
                reply_markup=keyboard
            )
            logger.info(f"Button added to document message ID: {message.message_id}")
        else:
            logger.debug(f"Message ID {message.message_id} does not contain a photo or document.")
    except Exception as e:
        logger.error(f"Error in on_new_post: {e}")

# Run the bot
app.run()
