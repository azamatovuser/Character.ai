from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, db
import requests
import os


def send_registration_event(user_id, username, first_name, last_name):
    payload = {
        'api_key': os.environ.get('API_KEY'),
        'events': [
            {
                'event_type': 'Sign Up',
                'user_id': str(user_id),
                'user_properties': {
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name
                }
            }
        ]
    }
    response = requests.post('https://api.amplitude.com/2/httpapi', json=payload)
    if response.status_code == 200:
        print('Event sent successfully to Amplitude')
    else:
        print('Failed to send event to Amplitude')
    print(response.content)


@dp.message_handler(commands=['start', 'menu'])
async def start(message: types.Message):
    first_name = message.from_user.first_name
    button = InlineKeyboardMarkup()
    mini_button = InlineKeyboardButton('Открыть web app страницу', callback_data='button')
    button.add(mini_button)
    if message.text == '/menu':
        await message.reply(f"Привет {first_name}!", reply_markup=button)
    else:
        user_id = message.from_user.id
        username = message.from_user.username
        last_name = message.from_user.last_name
        db.insert_user(user_id, username, first_name, last_name)
        send_registration_event(user_id, username, first_name, last_name)
        await message.reply(f"Привет {first_name}!", reply_markup=button)
