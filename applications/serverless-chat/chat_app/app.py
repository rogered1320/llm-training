import json
from qa_chat import run_qa_chatbot
import boto3
from botocore.exceptions import ClientError
import os
from constants import configure_remote_env_vars
ssm = boto3.client('ssm')
os.environ["LANGSMITH_PROJECT"] = "serverless-chat"


def lambda_handler(event, context):
    """AWS Lambda function handler for the serverless chat application."""
    configure_env_vars()
    body = event.get("body")
    if isinstance(body, str):
        body = json.loads(body)
    parameters = event.get("queryStringParameters", {})
    chat_type = body.get("chat_type", "qa")
    question = body.get("question", "")
    chat_id = body.get("chat_id", "")
    print("Lambda function started", question)
    if not question:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Bad Request: 'question' parameter is required",
            }),
        }
    print("Running chatbot with the provided question")
    response = run_qa_chatbot(question)
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
