from aiogram import types
import requests
import os
from loader import dp, db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import openai


openai.api_key = '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'


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


def send_answers_event(answers):
    payload = {
        'api_key': os.environ.get('API_KEY'),
        'events': [
            {
                'event_type': 'Answers',
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


@dp.message_handler(commands=['mario', 'enshtein'])
async def conversation(message: types.Message):
    if message.text == 'mario':
        await message.answer(f"Привет я Марио, что вы хотите от меня?")
    else:
        await message.answer(f"Привет я Энштейн, что вы хотите от меня?")


@dp.message_handler(content_types='text')
async def message_from_user(message: types.Message):
    user_id = message.from_user.id
    question = message.text
    db.insert_user_question(user_id, question)
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
    print(response['choices'][0]['text'])
    if response['choices'][0]['text']:
        answers = response['choices'][0]['text']
        send_answers_event(answers)
        db.insert_answer(answers)
        await message.answer(response['choices'][0]['text'])
    else:
        await message.answer('No answer')