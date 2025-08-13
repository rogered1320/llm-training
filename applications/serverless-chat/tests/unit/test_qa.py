

# Unit tests for qa_chat.py
import pytest
from unittest.mock import patch, MagicMock

# Mock external dependencies to avoid import errors and real API calls
import sys
sys.modules['pinecone'] = MagicMock()
sys.modules['langchain_openai'] = MagicMock()
sys.modules['langchain_pinecone'] = MagicMock()
sys.modules['langchain_core.runnables'] = MagicMock()
sys.modules['langchain_core.messages'] = MagicMock()
sys.modules['langchain_core.prompts'] = MagicMock()
sys.modules['langchain_core.tracers.langchain'] = MagicMock()

from chat_app import qa_chat


# Test that run_qa_chatbot raises ValueError when question is empty
def test_run_qa_chatbot_empty_question():
    with pytest.raises(ValueError):
        qa_chat.run_qa_chatbot("")


# Test that run_qa_chatbot returns the expected answer when all dependencies are mocked
@patch("chat_app.qa_chat.get_llm")
@patch("chat_app.qa_chat.get_rewriter_chain")
@patch("chat_app.qa_chat.get_retriever")
@patch("chat_app.qa_chat.get_retriever_chain")
@patch("chat_app.qa_chat.get_full_chain")
def test_run_qa_chatbot_success(mock_full_chain, mock_get_retriever_chain, mock_get_retriever, mock_get_rewriter_chain, mock_get_llm):
    # Setup mocks for the full chain and all dependencies
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = {"result": MagicMock(content="Test answer")}
    mock_full_chain.return_value = mock_chain
    mock_get_llm.return_value = MagicMock()
    mock_get_rewriter_chain.return_value = MagicMock()
    mock_get_retriever.return_value = MagicMock()
    mock_get_retriever_chain.return_value = MagicMock()

    result = qa_chat.run_qa_chatbot("What is AI?")
    assert result == "Test answer"


# Test that format_docs returns None for None or empty input
def test_format_docs_none():
    assert qa_chat.format_docs(None) is None
    assert qa_chat.format_docs([]) is None


# Test that format_docs returns a string containing content and url for valid docs
def test_format_docs_valid():
    doc = MagicMock()
    doc.page_content = "content"
    doc.metadata = {"source_url": "url"}
    result = qa_chat.format_docs([doc])
    assert "content" in result and "url" in result


# Test is_context_valid returns False for empty list and True for non-empty list
def test_is_context_valid():
    assert not qa_chat.is_context_valid([])
    assert qa_chat.is_context_valid([1,2])


# Test that stop_step_fn returns an AIMessage with the expected content
def test_stop_step_fn():
    msg = qa_chat.stop_step_fn({})
    assert hasattr(msg, "content")
    assert "enough information" in msg.content
