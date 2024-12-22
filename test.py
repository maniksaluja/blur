from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot setup
app = Client("my_bot", api_id="26980824", api_hash="fb044056059384d3bea54ab7ce915226'", bot_token="7099022623:AAHF5XCTdVgREoJWvK6sRJedYIso35E0XpE")

# Replace with your target username (user to DM)
target_username = "god_father11"

@app.on_message(filters.chat("-1002385675587"))
async def add_button(client, message):
    """
    Detect channel messages and add a button with a redirect functionality.
    """
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Redirect to DM", callback_data=f"redirect_{message.message_id}")]]
    )
    await message.reply_text(
        "Click the button below to visit the DM.",
        reply_markup=button,
        quote=True,
    )

@app.on_callback_query(filters.regex(r"redirect_\d+"))
async def handle_redirect(client, callback_query):
    """
    Handle the button click event and send a DM with the tagged post link.
    """
    message_id = int(callback_query.data.split("_")[1])  # Extract message_id from callback_data
    channel_id = callback_query.message.chat.id
    tag_link = f"https://t.me/c/{str(channel_id)[4:]}/{message_id}"  # Create tag link for the post

    # Send message in target user's DM with the tagged post link
    await client.send_message(
        target_username,
        f"User clicked the button for this post: [View Post]({tag_link})",
        parse_mode="markdown"
    )
    await callback_query.answer("Redirected to DM!")  # Notify user

app.run()
