
# Integration test for run_qa_chatbot using real environment variables loaded from .env
from langchain_google_genai import ChatGoogleGenerativeAI
from openai import BaseModel
from chat_app.qa_chat import run_qa_chatbot
import pytest
from pathlib import Path
from dotenv import load_dotenv

# We should create a custom .env for test but in this case we will use the existing one
dotenv_path = Path(__file__).resolve().parents[4] / '.env'
print(f"Loading environment variables from {dotenv_path}")
if dotenv_path.exists():
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError(f".env file not found at {dotenv_path}")


def test_full_run_qa_chatbot():
    """
    This test will run the real qa_chat.run_qa_chatbot using actual environment variables.
    It requires valid API keys and a working Pinecone/LLM setup.
    """
    question = "What is artificial intelligence?"
    answer = run_qa_chatbot(question)
    assert isinstance(answer, str)
    assert len(answer) > 0


def test_full_llm_as_judge_response():
    """
    This test will run the real qa_chat.run_qa_chatbot using actual environment variables.
    It requires valid API keys and a working Pinecone/LLM setup.
    """
    question = "What is artificial intelligence?"
    answer = run_qa_chatbot(question)
    expected_answer = "No Information to answer that question."

    test_result = llm_as_judge(question, expected_answer, answer)

    assert test_result.is_correct, f"Expected correct answer but got: {test_result.reasoning}"


def llm_as_judge(question, expected_answer, answer):
    """
    Uses the LLM to evaluate if the provided answer is correct based on the expected answer.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # other params...
    ).with_structured_output(EvaluationResponse)

    prompt = f"""
    You are an impartial judge evaluating an answer to a question.
    Your task is to compare the provided answer to the expected answer and determine if it is correct.

    Question: "{question}"
    Expected Answer: "{expected_answer}"
    Provided Answer: "{answer}"

    Evaluation Criteria:
    - Is the provided answer factually correct and relevant to the question?
    - Does it sufficiently match the expected answer in meaning and content?
    - Is the answer in the same language as the question?

    Respond ONLY with a JSON object in the following format:
    {{
      "is_correct": true or false,  // true if the answer is correct, false otherwise
      "reasoning": "A brief explanation of your evaluation (required only if is_correct is false), max 50 charsters"
    }}

    Do not include any text outside the JSON object.
    """

    return llm.invoke(prompt)


class EvaluationResponse(BaseModel):
    is_correct: bool
    reasoning: str = None
