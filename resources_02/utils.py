import concurrent.futures
import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from google import genai
from google.genai.types import HttpOptions, ModelContent, Part, UserContent
from dataclasses import dataclass
import re
load_dotenv()


@dataclass
class ChatParams:
    system_role_message: str = None
    temperature: float = 0.7
    expected_output_format: any = None


def hf_chat(content: str, params: ChatParams):
    """Call the Hugging Face Inference API to get a chat completion.
    Args:
        params (ChatParams): Parameters for the chat.
    Returns:
        dict: The response from the model.
    """
    client = InferenceClient(
        provider="cohere",
        api_key=os.environ["HF_TOKEN"],
    )
    messages = []
    if params.system_role_message:
        messages.append({
            "role": "system",
            "content": params.system_role_message
        })
    messages.append({
        "role": "user",
        "content": content
    })
    completion = client.chat.completions.create(
        model="CohereLabs/c4ai-command-r-plus",
        temperature=params.temperature,
        messages=messages,
        # response_format=params.expected_output_format,
    )

    return completion.choices[0].message.content


def openai_chat(content: str, params: ChatParams):
    """Call the OpenAI API to get a chat completion.
    Args:
        content (str): The user input to send to the model.
        params (ChatParams): Parameters for the chat.
    Returns:
        str: The response from the model.
    """

    client = OpenAI()
    messages = []
    if params.system_role_message:
        messages.append({
            "role": "system",
            "content": params.system_role_message
        })

    messages.append({
        "role": "user",
        "content": content
    })

    # Prepare the completion arguments
    completion_args = {
        "model": "gpt-4.1-nano",
        "messages": messages,
        "temperature": params.temperature,
    }

    # Add response_format if expected_output_format is provided
    if params.expected_output_format:
        completion_args["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "name": "output-format",
                "description": "",
                "schema": params.expected_output_format,
                "strict": True
            }
        }

    completion = client.chat.completions.create(**completion_args)

    response_content = completion.choices[0].message.content

    # Si hay un formato de salida esperado, limpiar la respuesta JSON
    if params.expected_output_format:
        response_content = clean_json_response(response_content)

    return response_content


def aws_bedrock_chat(content: str, params: ChatParams):
    """Call the AWS Bedrock API to get a chat completion.
    Args:
        content (str): The user input to send to the model.
        params (ChatParams): Parameters for the chat.
    Returns:
        str: The response from the model.
    """


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
            "openai": executor.submit(openai_chat, prompt),
        }
        results = {}
        for key, future in futures.items():
            try:
                results[key] = future.result()
            except Exception as e:
                results[key] = f"Error: {e}"
        return results


def parse_json_response(res):
    # parse the JSON response
    try:
        return json.loads(res)
    except json.JSONDecodeError as e:
        print("Failed to parse JSON response:")
        print(res)
        print(f"Error: {e}")


def clean_json_response(response_text):
    """
    Cleans the response from an LLM to extract only valid JSON.
    Handles cases where the model returns JSON wrapped in markdown code blocks.
    """
    # Remove markdown code blocks (```json ... ``` or ``` ... ```)
    json_pattern = r'```(?:json)?\s*(.*?)\s*```'
    match = re.search(json_pattern, response_text, re.DOTALL)

    if match:
        return match.group(1).strip()

    # If there are no code blocks, try to extract JSON directly
    # Look for the first { to the last }
    start = response_text.find('{')
    end = response_text.rfind('}')

    if start != -1 and end != -1 and start <= end:
        return response_text[start:end+1]

    # If it is a JSON array, look for [ ]
    start = response_text.find('[')
    end = response_text.rfind(']')

    if start != -1 and end != -1 and start <= end:
        return response_text[start:end+1]

    # If no JSON is found, return the original response
    return response_text.strip()
