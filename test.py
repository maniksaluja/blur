import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Bot setup
app = Client("my_bot", api_id=26980824, api_hash="fb044056059384d3bea54ab7ce915226", bot_token="7099022623:AAHF5XCTdVgREoJWvK6sRJedYIso35E0XpE")

# Replace with your target username (user to DM)
target_username = "god_father11"

@app.on_message(filters.chat("-1002385675587"))
async def add_button(client, message):
    """
    Detect channel messages and add a button with a redirect functionality.
    """
    try:
        # Debugging: Check if message is detected
        print("Message detected:", message.text or "Non-text message")

        # Add button
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Redirect to DM", callback_data=f"redirect_{message.message_id}")]]
        )
        await message.reply_text(
            "Click the button below to visit the DM.",
            reply_markup=button,
            quote=True,
        )
    except Exception as e:
        logging.error(f"Error in add_button: {e}")

@app.on_callback_query(filters.regex(r"redirect_\d+"))
async def handle_redirect(client, callback_query):
    """
    Handle the button click event and send a DM with the tagged post link.
    """
    try:
        # Extract message ID and channel ID
        message_id = int(callback_query.data.split("_")[1])  # Extract message_id from callback_data
        channel_id = callback_query.message.chat.id
        tag_link = f"https://t.me/c/{str(channel_id)[4:]}/{message_id}"  # Create tag link for the post

        # Debugging: Log the tag link
        print(f"Generated tag link: {tag_link}")

        # Send message in target user's DM with the tagged post link
        await client.send_message(
            target_username,
            f"User clicked the button for this post: [View Post]({tag_link})",
            parse_mode="markdown"
        )
        await callback_query.answer("Redirected to DM!")  # Notify user
    except Exception as e:
        logging.error(f"Error in handle_redirect: {e}")

@app.on_message(filters.command("check_id"))
async def check_channel_id(client, message):
    """
    Helper command to check channel ID.
    """
    try:
        await message.reply_text(f"Channel ID: {message.chat.id}")
    except Exception as e:
        logging.error(f"Error in check_channel_id: {e}")

app.run()
