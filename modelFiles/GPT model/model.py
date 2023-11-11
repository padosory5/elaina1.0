from openai import OpenAI


client = OpenAI(api_key="...")



response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
  ]
)

print(response)


'''
client = "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"

'''

