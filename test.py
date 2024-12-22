from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters

# Your Bot Token
TOKEN = '7099022623:AAHF5XCTdVgREoJWvK6sRJedYIso35E0XpE'
# Channel ID (e.g., @YourChannel)
CHANNEL_ID = '-1002385675587'

# Define the link you want to open
link = "https://t.me/CuteGirlTG"

def add_button_to_post(update, context):
    # Check if the message is from the channel
    if update.message.chat.id == int(CHANNEL_ID):
        # Create a button with the link
        keyboard = [
            [InlineKeyboardButton("Click to Open Link", url=link)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Edit the message with the button
        context.bot.edit_message_text(
            chat_id=CHANNEL_ID,
            message_id=update.message.message_id,
            text=update.message.text,
            reply_markup=reply_markup
        )

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Listen for new messages in the channel
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, add_button_to_post))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
