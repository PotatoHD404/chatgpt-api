# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import json
import os
from datetime import datetime

import openai
from dotenv import load_dotenv

from count_tokens import num_tokens_from_string

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def read_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == "__main__":
    prompt = """The following is a conversation with an AI assistant.
     The assistant is helpful, creative, clever, and very friendly."""
    model = "gpt-3.5-turbo"
    messages = [
        {"role": "user", "content": prompt}
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        # temperature=0.9,
        max_tokens=150,
        n=1,
    )
    print(response['choices'][0]['message']['content'])
    # read all responses from file and append new response
    responses = read_json('responses.json')
    timestamp = response['created']
    time = datetime.fromtimestamp(timestamp)
    dt_string = time.strftime("%d/%m/%Y %H:%M:%S")
    # response = response['choices'][0]['response']
    response['input_messages'] = messages
    response['created_timestamp'] = timestamp
    response['created'] = dt_string
    responses.append(response)
    # save responses to file
    save_json('responses.json', responses)
