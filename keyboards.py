from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
import openai_api

main_menu_kb = [
    [KeyboardButton(text='Очистить историю')],  # Вторая строка меню
    [KeyboardButton(text='Изменить источник доступа к GPT')]
]

# Создаем экземпляр меню
main_menu = ReplyKeyboardMarkup(keyboard=main_menu_kb,
                                resize_keyboard=True,
                                input_field_placeholder='Введите сообщение')


async def get_providers_kb():
    providers_menu_kb = []
    temp_ = []
    for provider in await openai_api.OpenAI_API.get_providers_list():
        temp_.append(KeyboardButton(text=provider))
        if len(temp_) == 2:
            providers_menu_kb.append(temp_)
            temp_ = []

    else:
        if len(temp_) == 1:
            providers_menu_kb.append(temp_)
            temp_ = []
    return ReplyKeyboardMarkup(keyboard=providers_menu_kb,
                               resize_keyboard=True,
                               input_field_placeholder='Выберите провайдера')


if __name__ == "__main__":
    import asyncio

    asyncio.run(get_providers_kb())
