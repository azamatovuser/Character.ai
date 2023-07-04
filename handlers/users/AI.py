import openai

openai.api_key = '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'
openai.Model.list()

response = openai.Completion.create(
    model='davinci',
    prompt='hello',
)
print(response['choices'][0]['text'])