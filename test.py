from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Application, MessageHandler, filters

# Replace this with your channel ID and target username
CHANNEL_ID = "-1002385675587"
TARGET_USERNAME = "iamgojoof6eyes"

def start(update: Update, context):
    update.message.reply_text('Hello! Main tumhara Telegram bot hoon. Tum kya karna chahte ho?')

def post(update: Update, context):
    button = InlineKeyboardButton("Message me", callback_data="message_me")
    reply_markup = InlineKeyboardMarkup([[button]])
    context.bot.send_message(chat_id=CHANNEL_ID, text='Click the button to message the user.', reply_markup=reply_markup)

def button(update: Update, context):
    query = update.callback_query
    user_id = query.from_user.id
    query.edit_message_text(text=f"Redirecting to user {TARGET_USERNAME}")

    # Send DM to the target user with the reply tag
    context.bot.send_message(chat_id=f"@{TARGET_USERNAME}", text=f"Yeh message aapko DM mein mila hai.\n\nReply: {query.message.reply_to_message.text}")

def main():
    application = Application.builder().token("7099022623:AAHF5XCTdVgREoJWvK6sRJedYIso35E0XpE").build()

    dp = application.add_handler
    dp(CommandHandler("start", start))
    dp(CommandHandler("post", post))
    dp(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == '__main__':
    main()
