import os

from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CommandHandler, Updater, CallbackQueryHandler

from bot.models import User, Cell



"""
------------------------------------------------------------------------------
Команды для работы с БД
------------------------------------------------------------------------------
"""
# Кладем telegram id при соглашении на обработку ПД
def add_tgid(telegram_id: int):
    user = User(telegram_id=telegram_id)
    user.save()

# Проверяем есть ли id пользователя в БД
def find_user(telegram_id: int):
    find_user = User.objects.filter(telegram_id=telegram_id)
    if not find_user:
        return False
    return True


def make_order(telegram_id: int):
    pass


def get_cells():
    cells = Cell.objects.all()
    return cells


def get_prices():
    pass


def add_user_info():
    pass


"""
------------------------------------------------------------------------------
Хэндлеры команд для бота
------------------------------------------------------------------------------
"""
def start(update: Update, context: CallbackContext):
    message = f"Описание проекта, соглашение о ПД, ссылка"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def approve(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    add_tgid(user_id)
    message = f"Вы согласились на обработку своих данных, наверное мы сохраним их :)"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def account(update: Update, context: CallbackContext):
    user_id = 1
    chat_id = update.message.chat_id
    if find_user(user_id):
        message = "Ваш личный кабинет"
        reply_markup = get_account_keyboard()
        
        context.bot.send_message(
            chat_id=chat_id,
            text=message,
            reply_markup=reply_markup,
        )
    else:
        message = f"Мы вас не знаем, возможно вы не согласились на обработку ПД"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)



"""
------------------------------------------------------------------------------
Функции для личного кабинета
------------------------------------------------------------------------------
"""

def get_user_information(telegram_id):
    user = User.objects.get(telegram_id=telegram_id)
    user_information = f'''Имя: {user.name}
Фамилия: {user.surname}
Номер телефона: {user.phone}
Адрес: {user.address}
Email: {user.email}'''
    return user_information


def get_account_keyboard():
    keyboard=[
        [InlineKeyboardButton("Посмотреть личные данные", callback_data='ererer'),],
        [InlineKeyboardButton("Редактировать личные данные", callback_data='sdgsg'),],
        [InlineKeyboardButton(f"Посмотреть мои заказы", callback_data='eredfdfhrer'),],
        [InlineKeyboardButton("Назад", callback_data='erdfhdherer'),],
    ]
    return InlineKeyboardMarkup(keyboard)


class Command(BaseCommand):

    def handle(self, *args, **options):
        load_dotenv()

        updater = Updater(token=os.getenv("BOT_TOKEN"), use_context=True)
        dispatcher = updater.dispatcher

        start_handler = CommandHandler('start', start)
        approve_handler = CommandHandler('approve', approve)
        account_handler = CommandHandler('account', account)
      
        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(approve_handler)
        dispatcher.add_handler(account_handler)
        updater.start_polling()
        updater.idle()
