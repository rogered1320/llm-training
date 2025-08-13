import json
import pytest

from chat_app import app


def test_lambda_handler_no_body():

    ret = app.lambda_handler({"body": None}, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 400
    assert "message" in ret["body"]
    assert data["message"] == "Bad Request: 'question' parameter is required"


def test_lambda_handler_no_question():
    ret = app.lambda_handler({"body": json.dumps({"chat_type": "qa"})}, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 400
    assert "message" in ret["body"]
    assert data["message"] == "Bad Request: 'question' parameter is required"
    
def test_lambda_handler_valid_question(mocker):
    # Mock the run_qa_chatbot function to return a fixed response
    mock_run_qa_chatbot = mocker.patch("chat_app.app.run_qa_chatbot", return_value="Mocked response")
    
    # Mock the configure_local_env_vars function to avoid loading .env file
    mocker.patch("chat_app.app.configure_local_env_vars", return_value=None)
    
    event = {
        "body": json.dumps({
            "question": "What is the capital of France?",
            "chat_type": "qa",
            "chat_id": "12345"
        })
    }
    
    ret = app.lambda_handler(event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "message" in ret["body"]
    assert data["message"] == "Mocked response"
    mock_run_qa_chatbot.assert_called_once_with("What is the capital of France?")
    mock_run_qa_chatbot.assert_called_once()
