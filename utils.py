import os
import requests
from openai import OpenAI
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from google import genai
load_dotenv()

def hf_chat(content: str):
    """Call the Hugging Face Inference API to get a chat completion.
    Args:
        content (str): The user input to send to the model.
    Returns:
        dict: The response from the model.
    """
    client = InferenceClient(
        provider="cohere",
        api_key=os.environ["HF_TOKEN"],
    )

    completion = client.chat.completions.create(
        model="CohereLabs/c4ai-command-r-plus",
        messages=[
            {
                "role": "user",
                "content": content
            }
        ],
    )

    return completion.choices[0].message.content

def lm_studio_chat(content: str):
    """Call the LM Studio API (LOCAL) to get a chat completion.
    Args:
        content (str): The user input to send to the model.
    Returns:
        dict: The response from the model.
    """

    url = "http://localhost:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "gemma-3-4b-it",
        "messages": [
            # {"role": "system", "content": "Always answer in rhymes. Today is Thursday"},
            {"role": "user", "content": content}
        ],
        #"temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

def openai_chat(content: str):
    """Call the OpenAI API to get a chat completion.
    Args:
        content (str): The user input to send to the model.
    Returns:
        dict: The response from the model.
    """

    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {
                "role": "user",
                "content": content,
            },
        ],
    )

    return completion.choices[0].message.content

def gemini_chat(content: str):
    """Call the Gemini API to get a chat completion.
    Args:
        content (str): The user input to send to the model.
    Returns:
        dict: The response from the model.
    """
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=content
    )
    return response.text


def build_prompt(prompt: str, resume: str = None) -> str:
    """Build a prompt for the model.
    Args:
        prompt (str): The user input to send to the model.
        resume (str, optional): The resume to include in the prompt. Defaults to None.
    Returns:
        str: The complete prompt to send to the model.
    """
    if resume:
        return prompt.replace("{cv}", resume)
    return prompt

import concurrent.futures

def execute_prompt(prompt: str):
    """Execute the prompt against multiple models concurrently.
    Args:
        prompt (str): The user input to send to the models.
    Returns:
        dict: A dictionary with the results from each model.
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            "hf": executor.submit(hf_chat, prompt),
            "lm_studio": executor.submit(lm_studio_chat, prompt),
            "openai": executor.submit(openai_chat, prompt),
            "gemini": executor.submit(gemini_chat, prompt)
        }
        results = {}
        for key, future in futures.items():
            try:
                results[key] = future.result()
            except Exception as e:
                results[key] = f"Error: {e}"
        return results
