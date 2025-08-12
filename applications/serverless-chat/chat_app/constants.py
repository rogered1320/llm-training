from botocore.exceptions import ClientError
import boto3
import os
ENV_VARS = {
    "LANGSMITH_ENDPOINT": "https://api.smith.langchain.com",
    "LANGSMITH_PROJECT": "serverless-chat"
}
SEC_ENV_VARS_KEYS = [
    'LANGSMITH_TRACING',
    'BEDROCK_API_KEY',
    'LANGSMITH_API_KEY',
    'OPENAI_API_KEY',
    'PINECONE_API_KEY',
    'POSTGRESQL_CONNECTION_STRING',
]


ssm = boto3.client('ssm')


def get_secure_param(names: list[str]) -> list[str]:
    """
    Reads a SecureString from SSM using the AWS-managed key (aws/ssm).
    """
    try:
        resp = ssm.get_parameters(Names=names, WithDecryption=False)
        return [(param["Name"], param["Value"]) for param in resp["Parameters"]]
    except ClientError as e:
        print(e)
        raise RuntimeError(f"Failed to read SSM parameter")


def configure_remote_env_vars():
    """Configure environment variables from SSM parameters"""
    print("Configuring environment variables from SSM parameters")
    for key, value in ENV_VARS.items():
        os.environ[key] = value
    params = get_secure_param(SEC_ENV_VARS_KEYS)
    for key, value in params:
        os.environ[key] = value
    print("Environment variables configured successfully")
