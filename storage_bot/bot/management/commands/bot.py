import os

from bot.models import User

from dotenv import load_dotenv()

from django.core.management.base import BaseCommand
from django.conf import settings

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
# Импортируем модели



class Command(BaseCommand):
    help = 'Telegramm Bot'

    def handle(self, *args, **options):
        # Пишем код бота тут
        load_dotenv()
        
        async def hello(
                update: Update, 
                context: ContextTypes.DEFAULT_TYPE
        ) -> None:
            await update.message.reply_text(
                f'Hello {update.effective_user.first_name}'
            )

        app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

        app.add_handler(CommandHandler("hello", hello))

        app.run_polling()
