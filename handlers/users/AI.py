import os
import openai

openai.api_key = os.environ.get('OPENAI_KEY')
openai.Model.list()

response = openai.Completion.create(
    model='text-davinci-003',
    prompt='hello',
)
print(response['choices'][0]['text'])