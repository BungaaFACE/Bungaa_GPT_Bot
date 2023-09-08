import g4f
import traceback


CONVERSATION_MES_LIMIT = 512


class OpenAI_API:

    def __init__(self, tg_user_id):
        self.messages = []

    # def moderation_check(text):
    #     return not openai.Moderation.create(input=text)['results'][0]['flagged']

    async def send_message(self, text):
        self.messages.append({"role": "user", "content": text})
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages,
                provider=g4f.Provider.DeepAi)
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


if __name__ == '__main__':
    user1 = OpenAI_API('1')
    user1.send_message('Привет! Меня зовут Ким')
    user1.send_message('Как меня зовут?')
    user2 = OpenAI_API('2')
    user2.send_message('Как меня зовут?')
