from gradio_client import Client

client = Client("huggingface-projects/gemma-3n-E4B-it")

def ask_ai(message):
    result = client.predict(
        message={"text": message},
        system_prompt="You are a helpful assistant.",
        max_new_tokens=300,
        api_name="/chat"
    )
    return result
