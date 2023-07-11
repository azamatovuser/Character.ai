from aiogram import types
import requests
import os
from loader import dp, db, bot, storage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import openai


openai.api_key = os.environ.get('OPENAI_KEY')
character_check = ['none']


def send_character_event(user_id, character):
    payload = {
        'api_key': os.environ.get('API_KEY'),
        'events': [
            {
                'event_type': 'Character',
                'user_id': str(user_id),
                'user_properties': {
                    'character': character
                }
            }
        ]
    }
    response = requests.post('https://api.amplitude.com/2/httpapi', json=payload)
    if response.status_code == 200:
        print('Event character sent successfully to Amplitude')
    else:
        print('Failed character to send event to Amplitude')
    print(response.content)


def send_messages_event(user_id, question):
    payload = {
        'api_key': os.environ.get('API_KEY'),
        'events': [
            {
                'event_type': 'Messages',
                'user_id': str(user_id),
                'user_properties': {
                    'question': question
                }
            }
        ]
    }
    response = requests.post('https://api.amplitude.com/2/httpapi', json=payload)
    if response.status_code == 200:
        print('Event messages sent successfully to Amplitude')
    else:
        print('Failed messages to send event to Amplitude')
    print(response.content)


def send_api_event(user_id, answers):
    payload = {
        'api_key': os.environ.get('API_KEY'),
        'events': [
            {
                'event_type': 'Answers',
                'user_id': str(user_id),
                'user_properties': {
                    'answers': answers
                }
            }
        ]
    }
    response = requests.post('https://api.amplitude.com/2/httpapi', json=payload)
    if response.status_code == 200:
        print('Event answers sent successfully to Amplitude')
    else:
        print('Failed answers to send event to Amplitude')
    print(response.content)


def send_answers_event(user_id, answers):
    payload = {
        'api_key': os.environ.get('API_KEY'),
        'events': [
            {
                'event_type': 'Answers',
                'user_id': str(user_id),
                'user_properties': {
                    'answers': answers
                }
            }
        ]
    }
    response = requests.post('https://api.amplitude.com/2/httpapi', json=payload)
    if response.status_code == 200:
        print('Event answers sent successfully to Amplitude')
    else:
        print('Failed answers to send event to Amplitude')
    print(response.content)


# @dp.message_handler()
# async def handle_text(message: types.Message):
#     user_id = message.from_user.id
#     if await storage.get_state(chat=user_id):
#         await bot.send_message(chat_id=message.chat.id, text='Ой, извините!')
#     user_id = message.from_user.id
#     character = message.text
#     db.insert_character(user_id, character)
#     send_character_event(user_id, character)
#     if character == 'mario':
#         await message.answer(f"Привет я Марио, что вы хотите от меня?")
#     elif character == 'albert':
#         await message.answer(f"Привет я Энштейн, что вы хотите от меня?")


@dp.message_handler(text=['mario game character', 'albert einstein'])
async def mario(message: types.Message):
    user_id = message.from_user.id
    character = message.text
    character_check[0] = message.text
    send_character_event(user_id, character)
    db.insert_character(user_id, character)
    if character == 'mario game character':
        await message.answer('Я игровой персонаж марио, ведь я же буду интересен вам, да ведь?')
    else:
        await message.answer('Алберт Энштейн, один из великих умов. Не всем же везет иметь такую беседу, верно?')


@dp.message_handler(content_types='text')
async def message_from_user(message: types.Message):
    if character_check[0] == 'none':
        await message.answer('Сначала выберите персонажа')
    else:
        temporary_message = await message.answer("Я печатаю..")
        user_id = message.from_user.id
        question = message.text
        send_messages_event(user_id, question)
        response = openai.Completion.create(
            model='text-davinci-003',
            prompt=f"Bro you are {character_check[0]} and don't send dangerous information "
                   f"and you need to answer to this question - {question}. Also and don't begin conversation with ?",
            max_tokens=1000,
        )
        # if response.status_code == '200':
        #     pass
        if response['choices'][0]['text']:
            answer = response['choices'][0]['text']
            answer.replace("_", "\\_")
            answer.replace("*", "\\*")
            answer.replace("[", "\\[")
            answer.replace("`", "\\`")
            answer.replace("=", "\\=")
            send_answers_event(user_id, answer)
            db.insert_user_question_answer(user_id, question, answer)
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=temporary_message.message_id, text=answer)
        else:
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=temporary_message.message_id, text='Я совсем не понял вас :(')