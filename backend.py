import os
from operator import itemgetter

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import trim_messages
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory


load_dotenv()


def create_llm():
    """Create the OpenAI chat model."""

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found. "
            "Create a .env file and add your API key."
        )

    return ChatOpenAI(
        api_key=api_key,
        model="gpt-4o-mini",
        temperature=0.2,
        max_tokens=1024,
    )


llm = create_llm()



examples = [
    {
        "input": "Who are you?",
        "output": (
            "I'm your personal assistant. I help you with questions about "
            "AI, Data Science, and Data Engineering courses, placements, "
            "and careers."
        ),
    },
    {
        "input": "I'm from a non-IT background. Can I learn AI?",
        "output": (
            "Absolutely. Many BEPEC learners come from non-IT backgrounds. "
            "We start from fundamentals and take you to job-ready, step by "
            "step. No prior coding is needed to begin."
        ),
    },
    {
        "input": "How long does the course take?",
        "output": (
            "It depends on the track and your pace, but most learners become "
            "job-ready in a few focused months. Pick a track and commit to "
            "consistent daily practice."
        ),
    },
]


example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)


few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)




chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful and friendly AI assistant built by "
            "BEPEC Solutions. You remember the ongoing conversation "
            "and answer clearly and concisely. If you do not know "
            "something, say so honestly instead of making things up. "
            "Match the tone and style of the examples.",
        ),
        few_shot_prompt,
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)




trimmer = trim_messages(
    max_tokens=1000,
    strategy="last",
    token_counter=llm,
    include_system=False,
    start_on="human",
)



base_chain = (
    RunnablePassthrough.assign(
        history=itemgetter("history") | trimmer
    )
    | chat_prompt
    | llm
)


def create_memory():
    """Create a fresh short-term in-memory conversation history."""

    return InMemoryChatMessageHistory()


def run_conversation(input_text, memory, session_id="default"):
    """
    Run one conversational turn.

    Args:
        input_text: Current user message.
        memory: In-memory chat history for the current session.
        session_id: Identifier for the conversation session.

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

    except Exception:
        return (
            "Sorry, I couldn't process your request. "
            "Please try again.",
            memory,
        )