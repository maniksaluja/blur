from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, filters

TOKEN = '7041654616:AAHCsdChgpned-dlBEjv-OcOxSi_mY5HRjI'
CHAT_ID = '-1002374330304'
LIKE_EMOJI = '👍'
DISLIKE_EMOJI = '👎'

def send_reaction(update: Update, context: CallbackContext) -> None:
    message = update.channel_post
    if message:
        context.bot.send_message(chat_id=message.chat_id, text=LIKE_EMOJI, reply_to_message_id=message.message_id)
        context.bot.send_message(chat_id=message.chat_id, text=DISLIKE_EMOJI, reply_to_message_id=message.message_id)

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Handler to react to new channel posts
    dispatcher.add_handler(MessageHandler(filters.ChannelPost(), send_reaction))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
