import os
import datetime

from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext, CommandHandler, Updater, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler

from bot.models import User, Cell, Order, Storage


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

BUTTON_MY_PROFILE = "Мой личный кабинет"
BUTTON_NEW_ORDER = "Новый заказ"
BUTTON_OUR_TARRIFS = "Наши тарифы"
BUTTON_OUR_ADDRESSES = "Наши адреса"

BUTTON_SMALL = "До 3 м3"
BUTTON_MEDIUM = "3-10 м3"
BUTTON_LARGE = "От 10 м3"

BUTTON_YES = "Да"
BUTTON_NO = "Нет"

BUTTON_CONFIRM = "Подтвердить заказ"

"""
------------------------------------------------------------------------------
Команды для работы с БД
------------------------------------------------------------------------------
"""
def find_user(telegram_id: int):
    return User.objects.filter(telegram_id=telegram_id)


def find_cells(size):
    if size == "small":
        return Cell.objects.all().filter(size__lt=3)
    elif size == "medium":
        return Cell.objects.all().filter(size__gte=3).filter(size__lt=10)
    else:
        return Cell.objects.all().filter(size__gte=10)


def get_user_information(telegram_id):
    user = find_user(telegram_id=telegram_id)
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
    orders_count = user.orders.count()
    return orders_count

"""
------------------------------------------------------------------------------
Хэндлеры команд для бота
------------------------------------------------------------------------------
"""
def start(update: Update, context: CallbackContext):
    message = "Добро пожаловать в сервис по хранению вещей!"
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    user = find_user(user_id)
    reply_markup = get_main_menu_keyboard(user)
    context.bot.send_message(
            chat_id=chat_id,
            text=message,
            reply_markup=reply_markup,
        )
    return WELCOME


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


def start_menu_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    chat_id = query.message.chat_id
    user = find_user(user_id)
    if data == BUTTON_MY_PROFILE:
        reply_markup = get_account_keyboard(user_id)
        message = "Ваш личный кабинет"
        context.bot.send_message(
            chat_id=chat_id,
            text=message,
            reply_markup=reply_markup,
        )
        return PROFILE
    elif data == BUTTON_NEW_ORDER:
        if user:
            message = "Выберите размер ячейки для хранения"
            reply_markup = get_cell_sizes()
            context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup,)
            return NEW_ORDER
        else:
            message = "Сначала нужно Вас зарегистрировать, пожалуйста, поделитесь контактами"
            reply_markup = get_contact()
            context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup,)
            return USER_REGISTATION
    elif data == BUTTON_OUR_TARRIFS:
        message = "Тариф КОРОТКИЙ (до 2 месяцеев) - 1000 руб / месяц \
            Тариф СУПЕР (до 6 месяцев) - 800 руб / месяц \
            Тариф ХИТ (до 1 года) - 700 руб / месяц \
            * тариф рассчитан на стандарную ячейку, окончательная цена будет зависеть от размера груза"
        reply_markup = get_main_menu_keyboard(user)
        context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)
        return WELCOME
    elif data == BUTTON_OUR_ADDRESSES:
        storages = Storage.objects.all()
        message = []
        number = 1
        for storage in storages.iterator():
            message.append(f"{number}. Склад №{storage.id} по адресу: {storage.address}")
            number += 1
        reply_markup = get_main_menu_keyboard(user)
        context.bot.send_message(chat_id=chat_id, text="\n".join(message), reply_markup=reply_markup,)
        return WELCOME



def order_callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat_id
    user_id = user_id = update.callback_query.message.chat.id
    user = find_user(user_id)
    measurer = True
    if data == BUTTON_SMALL:
        cells = find_cells(size="small")
    elif data == BUTTON_MEDIUM:
        cells = find_cells(size="medium")
    elif data == BUTTON_LARGE:
        cells = find_cells(size="large")
    if data == BUTTON_SMALL or data == BUTTON_MEDIUM or data == BUTTON_LARGE:
        message = "Нужна ли Вам доставка?"
        reply_markup = get_yes_no_keyboard()
        context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)
    if data == BUTTON_YES and not user.address:
        measurer = True
        message = "Пожалуйста, укажите Ваш адрес"
        context.bot.send_message(chat_id=chat_id, text=message)
        return GET_ADDRESS
    elif data == BUTTON_NO or (data == BUTTON_YES and user.address):
        measurer = False
        message = "Добавьте комментарий к заказу, если это необходимо"
        context.bot.send_message(chat_id=chat_id, text=message,)
        return COMMENT
    if data == BUTTON_CONFIRM:
        new_order = Order(
            user = user.id,
            create_date=datetime.datetime.now(),
            measurer=measurer,
            comment = context.user_data.get("Comment", ""))
        new_order.save()
        message = "Ваш заказ создан, в ближайшее времся с Вами свяжется менеджер"
        reply_markup = get_main_menu_keyboard(user)
        context.bot.send_message(
            chat_id=chat_id,
            text=message,
            reply_markup=reply_markup,
        )
        return WELCOME


def keyboard_cabinet_callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    user_id = update.callback_query.message.chat.id
    if data == BUTTON_PERSONAL_DATA:
        reply_markup = get_account_keyboard(user_id)
        message = get_user_information(telegram_id=user_id)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup)
        
    elif data == BUTTON_EDIT_DATA:
        reply_markup = get_data_edit_keyboard()
        message = "Что хотите изменить/добавить?"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup)
    
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
        
    elif data == BUTTON_MAIN_MENU:
        pass
    
    elif data == BUTTON_EDIT_NAME:
        pass
        
    elif data == BUTTON_EDIT_SURNAME:
        pass
    
    elif data == BUTTON_EDIT_EMAIL:
        pass
    
    elif data == BUTTON_EDIT_ADRESS:
        pass

    elif data == BUTTON_EDIT_PHONE:
        pass
    
    elif data == BUTTON_PERSONAL_ACCOUNT:
        message = "Ваш личный кабинет"
        reply_markup = get_account_keyboard(user_id)
        
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            reply_markup=reply_markup,
        )

def contact_callback(update: Update, context: CallbackContext):
    contact = update.effective_message.contact
    user = User(
        telegram_id=contact['user_id'],
        name = contact['first_name'],
        surname = contact['last_name'],
        phone = contact['phone_number']
    )
    user.save()
    
    chat_id = update.message.chat_id
    message = "Выберите размер ячейки для хранения"
    reply_markup = get_cell_sizes()
    context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup,)
    return NEW_ORDER


def address_call_back(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user = find_user(telegram_id=user_id),
    chat_id = update.message.chat_id
    user.address = update.message
    user.save()
    message = "Добавьте комментарий к заказу, если это необходимо"
    context.bot.send_message(chat_id=chat_id, text=message,)
    return COMMENT


def comment_callback(update: Update, context: CallbackContext):
    context.user_data["Comment"] = update.message
    message = "Заказ готов"
    chat_id = update.message.chat_id
    reply_markup = confirm_order()
    context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup,)
    return WELCOME


def cancel(update: Update, context: CallbackContext):
    return ConversationHandler.END


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


def get_main_menu_keyboard(user):
    keyboard=[
        [InlineKeyboardButton("Новый заказ", callback_data=BUTTON_NEW_ORDER),],
        [InlineKeyboardButton("Наши тарифы", callback_data=BUTTON_OUR_TARRIFS),],
        [InlineKeyboardButton("Наши адреса", callback_data=BUTTON_OUR_ADDRESSES),],
    ]
    if user:
        profile_button = [InlineKeyboardButton("Личный кабинет", callback_data=BUTTON_MY_PROFILE),]
        keyboard = [profile_button] + keyboard
    return InlineKeyboardMarkup(keyboard)


def get_data_edit_keyboard():
    keyboard=[
        [
            InlineKeyboardButton("Имя", callback_data=BUTTON_EDIT_NAME),
            InlineKeyboardButton("Фамилию", callback_data=BUTTON_EDIT_SURNAME),
            InlineKeyboardButton("Адрес", callback_data=BUTTON_EDIT_EMAIL),
        ],
        [
            InlineKeyboardButton("Email", callback_data=BUTTON_EDIT_ADRESS),
            InlineKeyboardButton("Номер телефона", callback_data=BUTTON_EDIT_PHONE),
        ],
        [InlineKeyboardButton("Назад", callback_data=BUTTON_PERSONAL_ACCOUNT),],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_contact():
    keyboard=[
        [
            KeyboardButton("Поделиться контактом", request_contact=True),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True,)


def get_cell_sizes():
    keyboard=[
        [
            InlineKeyboardButton("До 3 м3", callback_data=BUTTON_SMALL),
            InlineKeyboardButton("3-10 м3", callback_data=BUTTON_MEDIUM),
            InlineKeyboardButton("От 10 м3", callback_data=BUTTON_LARGE),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_yes_no_keyboard():
    keyboard=[
        [
            InlineKeyboardButton("Да", callback_data=BUTTON_YES),
            InlineKeyboardButton("Нет, привезу сам", callback_data=BUTTON_NO),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def confirm_order():
    keyboard=[
        [
            InlineKeyboardButton("Подтвердить заказ", callback_data=BUTTON_CONFIRM),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)



WELCOME = 0
PROFILE = 1
USER_REGISTATION = 2
NEW_ORDER = 3
GET_ADDRESS = 4
COMMENT = 5

class Command(BaseCommand):

    def handle(self, *args, **options):
        load_dotenv()

        updater = Updater(token=os.getenv("BOT_TOKEN"), use_context=True)
        dispatcher = updater.dispatcher

        handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                WELCOME: [CallbackQueryHandler(callback=start_menu_handler, pass_chat_data=True,)],
                PROFILE: [CallbackQueryHandler(callback=keyboard_cabinet_callback_handler, pass_chat_data=True,)],
                USER_REGISTATION: [MessageHandler(Filters.contact, contact_callback)],
                NEW_ORDER: [CallbackQueryHandler(callback=order_callback_handler, pass_chat_data=True,)],
                GET_ADDRESS: [MessageHandler(Filters.text, address_call_back)],
                COMMENT: [MessageHandler(Filters.text, comment_callback)],
            },
            fallbacks=[CommandHandler('cancel', cancel)],
            )
        dispatcher.add_handler(handler)

        updater.start_polling()
        updater.idle()
