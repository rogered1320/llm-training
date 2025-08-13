from langchain_community.chat_message_histories import DynamoDBChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    ChatPromptTemplate
)

from langchain_openai import ChatOpenAI


def run_memory_chatbot(message, session_id):
    print(f"Running memory chatbot with message: {message} and session_id: {session_id}")
    llm = get_llm()

    system_prompt = "You are a helpful assistant called Zeta."

    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_prompt),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{query}"),
    ])

    pipeline = prompt_template | llm

    chat_history = get_chat_history(session_id)

    pipeline_with_history = create_pipeline_with_history(pipeline, chat_history)

    result = pipeline_with_history.invoke(
        {"query": message},
        config={"configurable": {"session_id": session_id}}
    )
    print(f"Memory chatbot response: {result}")
    return result.content


def get_llm():
    return ChatOpenAI(
        model="gpt-4.1-nano",
        temperature=0.7,
        verbose=True
    )


def get_chat_history(session_id):
    dynamo_table_name = "ChatBotSessionTable"
    chat_history = DynamoDBChatMessageHistory(table_name=dynamo_table_name, session_id=session_id)
    return chat_history


def create_pipeline_with_history(pipeline, chat_history):
    return RunnableWithMessageHistory(
        pipeline,
        lambda x: chat_history,
        input_messages_key="query",   # must match the prompt input variable
        history_messages_key="history"  # must match the prompt history variable
    )


if __name__ == "__main__":
    # Example usage
    from dotenv import load_dotenv
    load_dotenv()
    session_id = "example_session"
    message = "What is the capital of France?"
    response = run_memory_chatbot(message, session_id)
    print(f"Response from memory chatbot: {response}")
