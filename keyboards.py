from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main_menu_kb = [
    [KeyboardButton(text='Очистить историю')]  # Вторая строка меню
]

# Создаем экземпляр меню
main_menu = ReplyKeyboardMarkup(keyboard=main_menu_kb,
                                resize_keyboard=True,
                                input_field_placeholder='Введите сообщение')
