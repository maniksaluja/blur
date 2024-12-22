from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters

# Your Bot Token
TOKEN = '7099022623:AAHF5XCTdVgREoJWvK6sRJedYIso35E0XpE'
# Channel ID (e.g., @YourChannel)
CHANNEL_ID = '-1002385675587'

# Define the link you want to open
link = "https://t.me/CuteGirlTG"

async def add_button_to_post(update, context):
    # Check if the message is from the channel
    if update.message.chat.id == int(CHANNEL_ID):
        # Create a button with the link
        keyboard = [
            [InlineKeyboardButton("Click to Open Link", url=link)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Edit the message with the button
        await context.bot.edit_message_text(
            chat_id=CHANNEL_ID,
            message_id=update.message.message_id,
            text=update.message.text,
            reply_markup=reply_markup
        )

async def main():
    application = Application.builder().token(TOKEN).build()

    # Listen for new messages in the channel
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_button_to_post))

    # Run polling without asyncio.run()
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    # Run the application directly without asyncio.run()
    asyncio.get_event_loop().run_until_complete(main())
