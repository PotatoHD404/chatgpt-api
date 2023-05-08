# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import os

import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":
    prompt = """The following is a conversation with an AI assistant.
     The assistant is helpful, creative, clever, and very friendly."""
    # response = openai.Completion.create(
    #     engine="davinci",
    #     prompt=prompt,
    #     temperature=0.9,
    #     max_tokens=150,
    #     top_p=1,
    #     frequency_penalty=0,
    #     # presence_penalty=0.6,
    #     # stop=["\n", " Human:", " AI:"]
    # )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            # {"role": "system", "content": "You are a helpful assistant."},
            # {"role": "user", "content": "Who won the world series in 2020?"},
            # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ],
        # temperature=0.9,
        max_tokens=150,
        n=1,
    )

    # print response text

    print(response['choices'][0])


