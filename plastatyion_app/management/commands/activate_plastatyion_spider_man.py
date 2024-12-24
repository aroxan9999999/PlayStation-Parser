from django.core.management.base import BaseCommand
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, MenuButtonWebApp

class Command(BaseCommand):
    help = "Запуск Telegram-бота с кнопкой для перехода в веб-приложение"

    def handle(self, *args, **options):
        asyncio.run(self.start_bot())

    async def start_bot(self):
        TOKEN = "7768207417:AAGWTh5Of-lJEoviTjHv8ulJrnVWzvDfLDk"
        WEB_APP_URL = "http://127.0.0.1:8000/"  # Замените на ваш URL веб-приложения
        bot = Bot(token=TOKEN)
        dp = Dispatcher()

        @dp.message(CommandStart())
        async def start_command_handler(message):
            # Кнопка перехода в веб-приложение
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="Открыть веб-приложение", web_app=WebAppInfo(url=WEB_APP_URL))
            ]])

            # Сообщение с кнопкой
            await message.answer(
                "Добро пожаловать! Нажмите на кнопку ниже, чтобы открыть веб-приложение.",
                reply_markup=keyboard
            )

            # Установка встроенной кнопки в меню
            menu_button = MenuButtonWebApp(
                text="О",
                web_app=WebAppInfo(url=WEB_APP_URL)
            )
            await bot.set_chat_menu_button(menu_button=menu_button)

        # Запуск бота
        await dp.start_polling(bot)
