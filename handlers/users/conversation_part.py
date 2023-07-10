from aiogram import types
import requests
import os
from loader import dp, db, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import openai


openai.api_key = os.environ.get('OPENAI_KEY')


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


# Handle bot messages
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_text(message: types.Message, state: FSMContext):
    if message.text.lower() and message.from_user.is_bot == "mario":
        await message.answer("Data received!")
    user_id = message.from_user.id
    character = message.text
    db.insert_character(user_id, character)
    send_character_event(user_id, character)
    if character == 'mario':
        await message.answer(f"Привет я Марио, что вы хотите от меня?")
    elif character == 'albert':
        await message.answer(f"Привет я Энштейн, что вы хотите от меня?")


@dp.message_handler(content_types='text')
async def message_from_user(message: types.Message):
    user_id = message.from_user.id
    question = message.text
    send_messages_event(user_id, question)
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=question,
        temperature=0.9,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["You:"]
    )
    temporary_message = await message.answer("Я печатаю.")
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