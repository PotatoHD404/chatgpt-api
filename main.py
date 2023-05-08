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


def main():
    prompt = """The following is a conversation with an AI assistant.
     The assistant is helpful, creative, clever, and very friendly."""
    model = "gpt-3.5-turbo"
    messages = [
        {"role": "user", "content": prompt}
    ]
    # https://platform.openai.com/docs/api-reference/chat/create
    # https://platform.openai.com/account/api-keys
    # https://platform.openai.com/account/usage
    # get_response(messages, model)
    get_response_stream(messages, model)


def get_response_stream(messages, model):
    """Get response in interactive way from OpenAI API."""
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        # temperature=0.9,
        max_tokens=150,
        n=1,
        stream=True,
    )
    result = None
    added_indexes = {}
    finished = 0
    for chunk in response:
        # print(chunk)
        if result is None:
            result = {**chunk, 'choices': []}
        for choice in chunk['choices']:
            index = choice['index']
            if index not in added_indexes:
                new_choice = {'message': {}, **choice}
                del new_choice['delta']
                result['choices'].append(new_choice)
                result['choices'].sort(key=lambda x: x['index'])
                added_indexes = {x['index']: i for i, x in enumerate(result['choices'])}

            delta = choice['delta']
            index = added_indexes[index]
            for k, v in delta.items():
                if k not in result['choices'][index]['message']:
                    result['choices'][index]['message'][k] = v
                else:
                    result['choices'][index]['message'][k] += v
            if 'content' in delta:
                print(delta['content'], end='')
            if 'finish_reason' in choice and choice['finish_reason'] is not None:
                finished += 1
                result['choices'][index]['message']['finish_reason'] = choice['finish_reason']
                print()

        if finished == len(result['choices']):
            break

    # read all responses from file and append new response
    process_result(messages, result)


def process_result(messages, result):
    responses = read_json('responses.json')
    timestamp = result['created']
    time = datetime.fromtimestamp(timestamp)
    dt_string = time.strftime("%d/%m/%Y %H:%M:%S")
    # response = response['choices'][0]['response']
    result['input_messages'] = messages
    result['created_timestamp'] = timestamp
    result['created'] = dt_string
    # prepend response to list
    responses.insert(0, result)
    # save responses to file
    save_json('responses.json', responses)


def get_response(messages, model):
    """Get response from OpenAI API."""
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        # temperature=0.9,
        max_tokens=150,
        n=1,
        # stream=True,
    )
    print(response['choices'][0]['message']['content'])
    # read all responses from file and append new response
    process_result(messages, response)


if __name__ == "__main__":
    main()
