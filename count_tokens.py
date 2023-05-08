import tiktoken


def num_tokens_from_string(string: str, model_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model_name)
    # encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(string))
    return num_tokens


def main():
    prompt = """The following is a conversation with an AI assistant.
     The assistant is helpful, creative, clever, and very friendly."""
    print(num_tokens_from_string(prompt, "gpt-3.5-turbo"))


if __name__ == "__main__":
    main()
