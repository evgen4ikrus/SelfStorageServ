import os

from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater


def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    message = "Hello, {}!".format(user['username'])
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


class Command(BaseCommand):

    def handle(self, *args, **options):
        load_dotenv()

        updater = Updater(token=os.getenv("BOT_TOKEN"), use_context=True)
        dispatcher = updater.dispatcher

        start_handler = CommandHandler('start', start)
        dispatcher.add_handler(start_handler)
        updater.start_polling()
        updater.idle()
