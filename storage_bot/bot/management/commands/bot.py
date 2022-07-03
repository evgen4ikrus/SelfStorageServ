from email import message
import os
from turtle import update

from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CommandHandler, Updater, CallbackQueryHandler, MessageHandler, Filters

from bot.models import User, Cell, Order


BUTTON_PERSONAL_DATA = "Посмотреть личные данные"
BUTTON_MAIN_MENU = "Назад"
BUTTON_EDIT_DATA = "Редактировать личные данные"
BUTTON_WIEW_ORDERS = "Посмотреть мои заазы"

BUTTON_EDIT_NAME = "Редактировать имя"
BUTTON_EDIT_SURNAME = "Редактировать фамилию"
BUTTON_EDIT_EMAIL = "Редактировать email"
BUTTON_EDIT_ADRESS = "Редактировать адрес"
BUTTON_EDIT_PHONE = "Редактировать телефон"
BUTTON_PERSONAL_ACCOUNT = 'Личный кабинет'

EDITABLE_DATA = None
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


def get_user(telegram_id):
    user = User.objects.get(telegram_id=telegram_id)
    return user


def get_cells():
    cells = Cell.objects.all()
    return cells


def get_prices():
    pass


def add_user_info():
    pass


def get_order_information(order):
    cell = order.cell
    storage = cell.storage
    message = f'''Дата создания заказа: {order.create_date}
Ваши вещи находится в ячейке № {cell.number} на нашем складе по адресу: {storage.address}, на {cell.floor} этаже
Температура хранения: {cell.temperature} градусов цельсия
Площадь ячейки: {cell.size} м2, высота потолка : {cell.height} м.
Цена аренды: {cell.price}р. в месяц
Дата окончания аренды : {order.lease_time}
Ваш комментарий по заказу: {order.comment}'''
    return message


def get_user_information(telegram_id):
    user = get_user(telegram_id=telegram_id)
    user_information = f'''Имя: {user.name}
Фамилия: {user.surname}
Номер телефона: {user.phone}
Адрес: {user.address}
Email: {user.email}'''
    return user_information


def get_orders(telegram_id):
    user = get_user(telegram_id=telegram_id)
    orders = Order.objects.filter(user=user)
    return orders


def get_number_orders(telegram_id):
    user = get_user(telegram_id=telegram_id)
    orders_count = Order.objects.filter(user=user).count()
    return orders_count


def edit_user_data(text, user):
    global EDITABLE_DATA
    if EDITABLE_DATA == 'Имя':
        user.name = text
    elif EDITABLE_DATA == 'Фамилия':
        user.surname = text
    elif EDITABLE_DATA == 'Email':
        user.email = text
    elif EDITABLE_DATA == 'Адрес':
        user.address = text
    elif EDITABLE_DATA == 'Номер телефона':
        user.phone = text
    user.save()
    
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


def data_edit_message_handler(update: Update, context: CallbackContext):
    text = update.message.text
    user_id = update.message.from_user.id
    user = get_user(telegram_id=user_id)
    edit_user_data(text, user)
    reply_markup = get_data_edit_keyboard()
    context.bot.send_message(chat_id=update.effective_chat.id, text="Личные данные обновлены")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Что хотите изменить ещё?", reply_markup=reply_markup)


def keyboard_cabinet_callback_handler(update: Update, context: CallbackContext):
    global EDITABLE_DATA
    query = update.callback_query
    data = query.data
    user_id = update.callback_query.message.chat.id
    if data == BUTTON_PERSONAL_DATA:
        reply_markup = get_account_keyboard(user_id)
        message = get_user_information(telegram_id=user_id)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup)
        
    elif data == BUTTON_EDIT_DATA:
        reply_markup = get_data_edit_keyboard()
        message = "Что хотите изменить?"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup)
    
    elif data == BUTTON_WIEW_ORDERS:
        reply_markup = get_account_keyboard(user_id)
        orders = get_orders(telegram_id=user_id)
        for order in orders:
            message = get_order_information(order)
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        message = "Ваш личный кабинет"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup)
        
    elif data == BUTTON_MAIN_MENU:
        ##### Доработать после создания главного меню #######
        pass
    
    elif data == BUTTON_EDIT_NAME:
        EDITABLE_DATA = 'Имя'
        message = "Введите Ваше имя:"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        
    elif data == BUTTON_EDIT_SURNAME:
        EDITABLE_DATA = 'Фамилия'
        message = "Введите Вашу Фамилию:"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    
    elif data == BUTTON_EDIT_EMAIL:
        EDITABLE_DATA = 'Email'
        message = "Введите Ваш email:"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    
    elif data == BUTTON_EDIT_ADRESS:
        EDITABLE_DATA = 'Адрес'
        message = "Введите Ваш адрес:"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    elif data == BUTTON_EDIT_PHONE:
        EDITABLE_DATA = 'Номер телефона'
        message = "Введите Ваш номер телефона:"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    
    elif data == BUTTON_PERSONAL_ACCOUNT:
        message = "Ваш личный кабинет"
        reply_markup = get_account_keyboard(user_id)
        
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            reply_markup=reply_markup,
        )

"""
------------------------------------------------------------------------------
Клавиатуры
------------------------------------------------------------------------------
"""


def get_account_keyboard(user_id):
    orders_count = get_number_orders(telegram_id=user_id)
    keyboard=[
        [
            InlineKeyboardButton("Посмотреть личные данные", callback_data=BUTTON_PERSONAL_DATA),
            InlineKeyboardButton("Редактировать личные данные", callback_data=BUTTON_EDIT_DATA),
        ],
        [InlineKeyboardButton(f"Посмотреть мои заказы ({orders_count})", callback_data=BUTTON_WIEW_ORDERS),],
        [InlineKeyboardButton("Назад", callback_data=BUTTON_MAIN_MENU),],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_data_edit_keyboard():
    keyboard=[
        [
            InlineKeyboardButton("Имя", callback_data=BUTTON_EDIT_NAME),
            InlineKeyboardButton("Фамилию", callback_data=BUTTON_EDIT_SURNAME),
            InlineKeyboardButton("Адрес", callback_data=BUTTON_EDIT_ADRESS),
        ],
        [
            InlineKeyboardButton("Email", callback_data=BUTTON_EDIT_EMAIL),
            InlineKeyboardButton("Номер телефона", callback_data=BUTTON_EDIT_PHONE),
        ],
        [InlineKeyboardButton("Назад", callback_data=BUTTON_PERSONAL_ACCOUNT),],
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
        button_cabinet_handler = CallbackQueryHandler(callback=keyboard_cabinet_callback_handler, pass_chat_data=True)
        
        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(approve_handler)
        dispatcher.add_handler(account_handler)
        dispatcher.add_handler(button_cabinet_handler)
        dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=data_edit_message_handler))
        
        updater.start_polling()
        updater.idle()
