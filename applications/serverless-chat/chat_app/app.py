import json
from chat_app.qa_chat import run_qa_chatbot
from chat_app.memory_chat import run_memory_chatbot
import boto3
from botocore.exceptions import ClientError
import os
from chat_app.constants import configure_remote_env_vars
ssm = boto3.client('ssm')
os.environ["LANGSMITH_PROJECT"] = "serverless-chat"


def lambda_handler(event, context):
    """AWS Lambda function handler for the serverless chat application."""
    
    print("Lambda function started")
    body = event.get("body")
    if isinstance(body, str):
        body = json.loads(body)
    else:
        body = body or {}

    question = body.get("question", None)
    chat_type = body.get("chat_type", "qa")
    session_id = body.get("session_id", "")

    if not question:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Bad Request: 'question' parameter is required",
            }),
        }

    configure_env_vars()
    print("Running chatbot with the provided question", chat_type, session_id)
    if(chat_type == "qa"):
        response = run_qa_chatbot(question)
    elif(chat_type == "memory"):
        response = run_memory_chatbot(question, session_id)
    else:
        response = "Unsupported chat type. Please use 'qa' for question-answering."
    print(f"Chatbot response: {response}")
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": response
        }),
    }


def configure_env_vars():
    """Configure environment variables based on the deployment context."""
    if not os.getenv("NO_LOCAL_ENV") == "true":
        configure_local_env_vars()
    else:
        configure_remote_env_vars()


def configure_local_env_vars():
    """
    Configure local environment variables from a .env file.
    This is useful for local development and testing.
    """
    from dotenv import load_dotenv
    load_dotenv("../../../.env")
    print("Local environment variables configured from .env file")


def get_secure_param(name: str) -> str:
    """
    Reads a SecureString from SSM using the AWS-managed key (aws/ssm).
    """
    print(f"Reading SSM parameter: {name}")
    try:
        resp = ssm.get_parameter(Name=name, WithDecryption=False)
        return resp["Parameter"]["Value"]
    except ClientError as e:
        print(e)
        # Do not leak parameter names/values in logs in real apps
        raise RuntimeError(f"Failed to read SSM parameter: {e.response.get('Error', {}).get('Message', 'unknown')}")
