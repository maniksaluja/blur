from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot Configuration
api_id = "26980824"
api_hash = "fb044056059384d3bea54ab7ce915226"
bot_token = "7041654616:AAHCsdChgpned-dlBEjv-OcOxSi_mY5HRjI"
app = Client("edit_bot", api_id, api_hash, bot_token=bot_token)

# Track Edit Mode (Temporary)
edit_mode = {"status": False}  # False = ❌, True = ✅
user_data = {"old_text": "", "new_text": "", "channel_id": ""}

@app.on_message(filters.command("edit") & filters.private)
async def toggle_edit_mode(client, message):
    # Buttons for editing
    buttons = [
        [
            InlineKeyboardButton("Edit ✅❌", callback_data="edit_toggle"),
        ]
    ]
    await message.reply_text(
        "Click 'Edit ✅❌' to enable or disable the edit mode.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query()
async def callback_handler(client, callback_query):
    global edit_mode, user_data

    if callback_query.data == "edit_toggle":
        # If in edit mode, show options to edit old and new text
        if edit_mode["status"]:
            buttons = [
                [
                    InlineKeyboardButton("OLD TEXT", callback_data="old_text"),
                    InlineKeyboardButton("NEW TEXT", callback_data="new_text"),
                ],
                [InlineKeyboardButton("Start Processing", callback_data="start_processing")]
            ]
            await callback_query.message.edit_text(
                "Edit Mode: ON. Choose OLD or NEW Text, or Start Processing.",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        else:
            # Toggle to enable/disable edit mode
            edit_mode["status"] = True
            buttons = [
                [
                    InlineKeyboardButton("Edit ✅❌", callback_data="edit_toggle"),
                ]
            ]
            await callback_query.message.edit_text(
                "Edit Mode: ON",
                reply_markup=InlineKeyboardMarkup(buttons)
            )

    elif callback_query.data == "old_text":
        # Ask user for old text to replace
        await callback_query.message.reply_text("Please send the OLD text you want to replace.")
        
    elif callback_query.data == "new_text":
        # Ask user for new text
        await callback_query.message.reply_text("Please send the NEW text to replace with.")
        
    elif callback_query.data == "start_processing":
        # Ask for channel ID and forward messages to start processing
        await callback_query.message.reply_text("Please provide the Channel ID to start processing.")
        
    elif callback_query.data == "cancel_processing":
        # Cancel the processing
        await callback_query.message.reply_text("Processing has been cancelled.")

# Handling user's text input
@app.on_message(filters.text & filters.private)
async def handle_input(client, message):
    global user_data

    # Store the old text, new text, and channel ID from user
    if "OLD TEXT" in message.text:
        user_data["old_text"] = message.text
        await message.reply_text("OLD Text has been saved. Now please send the NEW Text.")

    elif "NEW TEXT" in message.text:
        user_data["new_text"] = message.text
        await message.reply_text(f"NEW Text has been saved. Now please send the Channel ID or press 'Start Processing'.")

    elif message.text.isdigit():  # Assuming Channel ID is numeric
        user_data["channel_id"] = message.text
        await message.reply_text(f"Channel ID {user_data['channel_id']} has been saved. Press 'Start Processing' to continue.")

    elif message.text == "Start Processing":
        # Here, implement the actual process of text replacement in the channel based on user inputs
        if user_data["old_text"] and user_data["new_text"] and user_data["channel_id"]:
            # Start text replacement in the channel (placeholder code)
            await message.reply_text(
                f"Processing started on Channel ID {user_data['channel_id']}.\nOld Text: {user_data['old_text']}\nNew Text: {user_data['new_text']}"
            )
        else:
            await message.reply_text("Please make sure all steps are completed (old text, new text, and channel ID).")

print("Bot is running...")
app.run()
