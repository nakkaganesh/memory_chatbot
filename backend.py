import os
from operator import itemgetter

from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI


# Load environment variables from .env
load_dotenv()


def create_llm():
    """Create and configure the OpenAI chat model."""

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found. "
            "Create a .env file and add your OpenAI API key."
        )

    return ChatOpenAI(
        api_key=api_key,
        model="gpt-4o-mini",
        temperature=0.2,
        max_tokens=1024,
    )


# Create the language model
llm = create_llm()


# Prompt used by the chatbot
chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful AI assistant. "
            "Answer the user's questions clearly and concisely. "
            "Use the conversation history when it is relevant. "
            "If you do not know something, say so rather than making it up.",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)


# Keep only recent messages when the conversation becomes large
trimmer = trim_messages(
    max_tokens=1000,
    strategy="last",
    token_counter=llm,
    include_system=False,
    start_on="human",
)


# Main LangChain pipeline
base_chain = (
    RunnablePassthrough.assign(
        history=itemgetter("history") | trimmer
    )
    | chat_prompt
    | llm
)


def create_memory():
    """Create an empty short-term conversation history."""

    return InMemoryChatMessageHistory()


def run_conversation(input_text, memory, session_id="default"):
    """
    Run one conversational turn using short-term memory.

    Args:
        input_text: Current user message.
        memory: In-memory chat history for the current session.
        session_id: Unique identifier for the conversation session.

    Returns:
        Tuple containing the assistant response and updated memory.
    """

    chat_with_history = RunnableWithMessageHistory(
        base_chain,
        lambda _: memory,
        input_messages_key="input",
        history_messages_key="history",
    )

    try:
        result = chat_with_history.invoke(
            {"input": input_text},
            config={
                "configurable": {
                    "session_id": session_id
                }
            },
        )

        return result.content, memory

    except Exception as error:
        print(f"Chatbot error: {error}")

        return (
            "Sorry, I couldn't process your request. "
            "Please try again.",
            memory,
        )