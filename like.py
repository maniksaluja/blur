from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes

TOKEN = '7041654616:AAHCsdChgpned-dlBEjv-OcOxSi_mY5HRjI'
CHAT_ID = '-1002374330304'
LIKE_EMOJI = '👍'
DISLIKE_EMOJI = '👎'

async def send_reaction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.channel_post
    if message:
        await context.bot.send_message(chat_id=message.chat_id, text=LIKE_EMOJI, reply_to_message_id=message.message_id)
        await context.bot.send_message(chat_id=message.chat_id, text=DISLIKE_EMOJI, reply_to_message_id=message.message_id)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Bot is running!')

async def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(MessageHandler(filters.ChannelPost(), send_reaction))
    application.add_handler(CommandHandler("start", start))

    await application.start_polling()
    await application.idle()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
