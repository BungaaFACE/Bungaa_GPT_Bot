from aiogram.types import Message, CallbackQuery
from aiogram import F, Dispatcher, Bot
from aiogram.filters import Filter
from openai_api import OpenAI_API
import keyboards as kb
import nest_asyncio
import asyncio
import os


nest_asyncio.apply()

bot = Bot(token=os.getenv('BUNGAAGPT_API_KEY'))
dp = Dispatcher()

# { telegram_user_id: OpenAI_API(telegram_user_id) }
user_conversations = {}


class Providers_Filter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.text in await OpenAI_API.get_providers_list()


@dp.message(F.text == '/start' or F.text.lower().strip() == 'menu' or F.text.lower().strip() == 'меню')
async def show_menu(message: Message):
    await message.answer(text='Добро пожаловать в BungaaGPT.\n'
                         'Начать новую беседу можно в меню.\n'
                         'Для начала общения отправьте сообщение с запросом.',
                         reply_markup=kb.main_menu)


@dp.message(F.text == 'Очистить историю')
async def start_new_conversation(message: Message):
    try:
        del user_conversations[message.from_user.id]
        await message.answer(text='История очищена.')
    except:
        await message.answer(text='У вас нет истории сообщений.')


@dp.message(F.text == 'Изменить источник доступа к GPT')
async def show_providers_list(message: Message):
    await message.answer('Выберите провайдера', reply_markup=await kb.get_providers_kb())


@dp.message(F.text == 'Провайдер')
async def show_current_provider(message: Message):
    if user_conversations.get(message.from_user.id):
        await message.answer(user_conversations[message.from_user.id].provider.__name__, reply_markup=kb.main_menu)


@dp.message(Providers_Filter())
async def change_provider(message: Message):
    if message.from_user.id in user_conversations.keys():
        await user_conversations[message.from_user.id].change_provider(message.text)
    else:
        user_conversations[message.from_user.id] = OpenAI_API(
            message.from_user.id, message.text)
    await message.answer('Провайдер изменен.', reply_markup=kb.main_menu)


@dp.message()
async def message_to_gpt(message: Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    if not user_conversations.get(message.from_user.id):
        user_conversations[message.from_user.id] = OpenAI_API(
            message.from_user.id)
    answer_text = await user_conversations[message.from_user.id].send_message(message.text)
    await message.answer(answer_text, reply_markup=kb.main_menu)


async def main():
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
