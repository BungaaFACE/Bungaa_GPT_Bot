import g4f
import traceback


CONVERSATION_MES_LIMIT = 512
PROVIDERS_BLACKLIST = {'BaseProvider', 'AsyncProvider',
                       'AsyncGeneratorProvider', 'RetryProvider', 'ChatBase'}


class OpenAI_API:

    def __init__(self, tg_user_id, provider=None):
        self.messages = []
        if not provider:
            self.provider = provider
        else:
            self.provider = getattr(g4f.Provider, provider)

    async def change_provider(self, provider):
        if provider == 'Лучший доступный провайдер':
            self.provider = None
        else:
            self.provider = getattr(g4f.Provider, provider)

    async def send_message(self, text):
        self.messages.append({"role": "user", "content": text})
        try:
            response = await g4f.ChatCompletion.create_async(
                model=g4f.models.default,
                provider=self.provider,
                messages=self.messages)
            self.messages.append({"role": "assistant", "content": response})
        except:
            print(traceback.format_exc())
            self.messages.pop()
            return 'Возникла ошибка:\n\n' + traceback.format_exc()
        # Проверка на максимальное кол-во сообщений
        pre_response = await self.len_converstaion_handler()
        return pre_response + response

    async def len_converstaion_handler(self):
        # (Количество оставшихся сообщений) // 2 (Ответы бота на каждое сообщение)
        messages_left = (CONVERSATION_MES_LIMIT - len(self.messages)) // 2
        if messages_left == 0:
            self.messages.clear()
            return f'~~~~~~~~~~~~~~~~~~~~~\n'\
                'ВНИМАНИЕ! Беседа сброшена.\n'\
                'Следующее сообщение будет в новом диалоге.\n'\
                '~~~~~~~~~~~~~~~~~~~~~\n'
        elif messages_left == 20 or \
                messages_left == 15 or \
                messages_left <= 10:
            return '~~~~~~~~~~~~~~~~~~~~~\n'\
                f'ВНИМАНИЕ! У вас осталось {messages_left} запроса в текущей беседе.\n'\
                'После этого беседа с ботом будет сброшена и начнется новый диалог.\n'\
                '~~~~~~~~~~~~~~~~~~~~~\n'

        return ''

    @staticmethod
    async def get_providers_list():
        providers_list = [provider for provider in g4f.Provider.__all__
                          if provider not in PROVIDERS_BLACKLIST
                          and getattr(g4f.Provider, provider).working and not getattr(g4f.Provider, provider).needs_auth]
        providers_list.insert(0, 'Лучший доступный провайдер')
        return providers_list


if __name__ == '__main__':
    import asyncio

    async def main():
        # user1 = OpenAI_API('1')
        # response = await user1.send_message('Привет! Меня зовут Ким')
        # print(response)
        # response = await user1.send_message('Как меня зовут?')
        # print(response)
        # user2 = OpenAI_API('2')
        # response = await user2.send_message('Как меня зовут?')
        # print(response)
        result = await OpenAI_API.get_providers_list()
        print(result)

    asyncio.run(main())
