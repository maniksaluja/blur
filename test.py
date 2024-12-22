import nest_asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext
import logging

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Your Bot Token
TOKEN = '7099022623:AAHF5XCTdVgREoJWvK6sRJedYIso35E0XpE'
# Channel ID (e.g., @YourChannel)
CHANNEL_ID = '-1002385675587'

# Define the link you want to open
link = "https://t.me/CuteGirlTG"

async def add_button_to_post(update: Update, context: CallbackContext):
    try:
        # Check if the message exists and if it's from the correct channel
        if update.channel_post and update.channel_post.chat.id == int(CHANNEL_ID):
            logger.info(f"Message received: {update.channel_post.text}")
            
            # Create a button with the link
            keyboard = [
                [InlineKeyboardButton("Click to Open Link", url=link)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Log before editing the message
            logger.info("Attempting to add button to the post...")

            # Edit the message with the button
            await context.bot.edit_message_text(
                chat_id=update.channel_post.chat.id,
                message_id=update.channel_post.message_id,
                text=update.channel_post.text,
                reply_markup=reply_markup
            )

            # Log after the button is added
            logger.info("Button added successfully!")
        else:
            logger.warning(f"Message not from the correct channel or does not exist! Message chat_id: {update.channel_post.chat.id if update.channel_post else 'None'}")
    except Exception as e:
        logger.error(f"Error occurred while adding button: {e}")

async def main():
    application = Application.builder().token(TOKEN).build()

    # Log bot startup
    logger.info("Bot started successfully!")

    # Listen for new messages in the channel
    application.add_handler(MessageHandler(filters.ALL, add_button_to_post))

    # Run polling without asyncio.run()
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    # Run the application with nest_asyncio
    asyncio.get_event_loop().run_until_complete(main())
