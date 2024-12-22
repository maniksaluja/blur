import nest_asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters
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

async def add_button_to_post(update, context):
    try:
        # Check if the message exists and if it's from the correct channel
        if update.message:
            logger.info(f"Message received: {update.message.text}")
            if update.message.chat and update.message.chat.id == int(CHANNEL_ID):
                # Log when the bot processes a message
                logger.info(f"Processing message in channel {CHANNEL_ID} with text: {update.message.text}")

                # Create a button with the link
                keyboard = [
                    [InlineKeyboardButton("Click to Open Link", url=link)]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                # Log before editing the message
                logger.info("Attempting to add button to the post...")

                # Edit the message with the button
                await context.bot.edit_message_text(
                    chat_id=CHANNEL_ID,
                    message_id=update.message.message_id,
                    text=update.message.text,
                    reply_markup=reply_markup
                )

                # Log after the button is added
                logger.info("Button added successfully!")
            else:
                logger.warning(f"Message not from the correct channel! Message chat_id: {update.message.chat.id}")
        else:
            logger.warning("Received NoneType message, skipping...")
    except Exception as e:
        logger.error(f"Error occurred while adding button: {e}")

async def main():
    application = Application.builder().token(TOKEN).build()

    # Log bot startup
    logger.info("Bot started successfully!")

    # Listen for new messages in the channel
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_button_to_post))

    # Run polling without asyncio.run()
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    # Run the application with nest_asyncio
    asyncio.get_event_loop().run_until_complete(main())
