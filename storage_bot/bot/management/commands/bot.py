import os

from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater

from bot.models import User, Cell

# Кладем telegram id при активации бота
def add_tgid(telegram_id: int):
    user = User(tgid=telegram_id)
    user.save()

# Проверяем есть ли пользователь в БД
def find_user(telegram_id: int):
    find_user = User.objects.all().filter(tgid=telegram_id)
    if not find_user:
        return False
    return True


def make_order(telegram_id: int):
    pass

def get_cells():
    cells = Cell.objects.all()
    return cells



def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if find_user(user_id):
        message = f"Hello, your id is {user_id}!"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    else:
        add_tgid(user_id)
        message = f"Описание проекта, соглашение о ПД"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


class Command(BaseCommand):

    def handle(self, *args, **options):
        load_dotenv()

        updater = Updater(token=os.getenv("BOT_TOKEN"), use_context=True)
        dispatcher = updater.dispatcher

        start_handler = CommandHandler('start', start)
        cells_handler = CommandHandler('cells', cells)
        dispatcher.add_handler(start_handler, get_cells)
        updater.start_polling()
        updater.idle()
