from datetime import datetime
import os

from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CommandHandler, Updater, CallbackQueryHandler

from bot.models import User, Cell, Order


BUTTON_PERSONAL_DATA = "Посмотреть личные данные"
BUTTON_BACK = "Назад"
BUTTON_EDIT_DATA = "Редактировать личные данные"
BUTTON_WIEW_ORDERS = "Посмотреть мои заазы"

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


def get_user_information(telegram_id):
    user = User.objects.get(telegram_id=telegram_id)
    user_information = f'''Имя: {user.name}
Фамилия: {user.surname}
Номер телефона: {user.phone}
Адрес: {user.address}
Email: {user.email}'''
    return user_information


def get_orders(telegram_id):
    user = User.objects.get(telegram_id=telegram_id)
    orders = Order.objects.filter(user=user)
    return orders


def get_number_orders(telegram_id):
    user = User.objects.get(telegram_id=telegram_id)
    orders_count = Order.objects.filter(user=user).count()
    return orders_count

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
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    if find_user(user_id):
        message = "Ваш личный кабинет"
        reply_markup = get_account_keyboard(user_id)
        
        context.bot.send_message(
            chat_id=chat_id,
            text=message,
            reply_markup=reply_markup,
        )
    else:
        message = f"Мы вас не знаем, возможно вы не согласились на обработку ПД"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def keyboard_callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    user_id = update.callback_query.message.chat.id
    print(user_id)
    if data == BUTTON_PERSONAL_DATA:
        reply_markup = get_account_keyboard(user_id)
        message = get_user_information(telegram_id=user_id)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup)
        
    elif data == BUTTON_EDIT_DATA:
        pass
    
    elif data == BUTTON_WIEW_ORDERS:
        reply_markup = get_account_keyboard(user_id)
        orders = get_orders(telegram_id=user_id)
        for order in orders:
            
# Нужно изменить после редактирования модели - Ячейка

            message = f'''Дата создания: {order.create_date}
Ваш комментарий: {order.comment}'''
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        message = "Ваш личный кабинет"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup)
        
    elif data == BUTTON_BACK:
        pass


"""
------------------------------------------------------------------------------
Функции для личного кабинета
------------------------------------------------------------------------------
"""


def get_account_keyboard(user_id):
    orders_count = get_number_orders(telegram_id=user_id)
    keyboard=[
        [InlineKeyboardButton("Посмотреть личные данные", callback_data=BUTTON_PERSONAL_DATA),],
        [InlineKeyboardButton("Редактировать личные данные", callback_data=BUTTON_EDIT_DATA),],
        [InlineKeyboardButton(f"Посмотреть мои заказы ({orders_count})", callback_data=BUTTON_WIEW_ORDERS),],
        [InlineKeyboardButton("Назад", callback_data=BUTTON_BACK),],
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
        button_handler = CallbackQueryHandler(callback=keyboard_callback_handler, pass_chat_data=True)
      
        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(approve_handler)
        dispatcher.add_handler(account_handler)
        dispatcher.add_handler(button_handler)
        updater.start_polling()
        updater.idle()
