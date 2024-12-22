from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler

# Your Bot Token
TOKEN = '7099022623:AAHF5XCTdVgREoJWvK6sRJedYIso35E0XpE'
# Channel ID (e.g., @YourChannel)
CHANNEL_ID = '-1002385675587'

# Define the link you want to open
link = "https://t.me/CuteGirlTG"

def post_with_button(update, context):
    # Create a button with the link
    keyboard = [
        [InlineKeyboardButton("Click to Open Link", url=link)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Post the message to your channel with the button
    context.bot.send_message(chat_id=CHANNEL_ID, text="Click the button below:", reply_markup=reply_markup)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("post", post_with_button))  # '/post' command to trigger the function

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
