# Short-Term Memory Chatbot

A conversational AI chatbot built with **Python, LangChain, OpenAI, and Streamlit** that maintains short-term conversational context during an active user session.

The project demonstrates how an LLM application can remember previous messages, manage conversation history, control context size, and maintain independent chat sessions.

## Features

- Multi-turn conversational AI
- Session-based short-term memory
- LangChain message-history management
- Token-aware conversation-history trimming
- Few-shot prompt engineering
- Independent Streamlit sessions
- Conversation reset functionality
- Interactive Streamlit chat interface
- Environment-variable API key management
- Automated memory tests with Pytest

## Architecture

```text
                    User
                     │
                     ▼
              Streamlit Chat UI
                     │
                     ▼
              Session State
              ┌──────┴──────┐
              │             │
        Session ID     Chat History
              │
              ▼
    In-Memory Message History
              │
              ▼
       Token-Based Trimming
              │
              ▼
        Few-Shot Prompt
              │
              ▼
          GPT-4o-mini
              │
              ▼
          AI Response
              │
              └──────────► Memory Updated
```

## How Short-Term Memory Works

Each Streamlit session creates its own in-memory conversation history.

When a user sends a message:

1. The message is added to the current conversation.
2. Recent message history is retrieved.
3. History is trimmed to control context size.
4. Relevant conversation history is inserted into the prompt.
5. The prompt is sent to the language model.
6. The assistant response is stored in the same session history.

This allows the chatbot to answer follow-up questions using information from earlier turns.

The memory is intentionally **session-based and non-persistent**. Clearing the conversation or ending the session removes the stored conversational context.

## Example

```text
User: My name is Ganesh.

Assistant: Nice to meet you, Ganesh.

User: What is my name?

Assistant: Your name is Ganesh.

User: I am learning machine learning.

Assistant: That's great!

User: What am I learning?

Assistant: You are learning machine learning.
```

## Conversation Reset

The **Clear Conversation** control:

- Creates a new empty memory
- Clears displayed chat history
- Generates a new session ID

This prevents context from the previous conversation from carrying into the new conversation.

## Tech Stack

- Python
- LangChain
- LangChain Core
- LangChain OpenAI
- OpenAI GPT-4o-mini
- Streamlit
- python-dotenv
- Pytest
- uv
- Git / GitHub

## Project Structure

```text
memory_chatbot/
├── tests/
│   └── test_memory.py
├── backend.py
├── frontend.py
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/nakkaganesh/memory_chatbot.git
cd memory_chatbot
```

### Using uv

Install dependencies:

```bash
uv sync
```

### Using pip

Alternatively:

```bash
pip install -r requirements.txt
```

## Environment Configuration

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_openai_api_key
```

The `.env` file is excluded from Git and should never be committed.

## Run the Application

```bash
uv run streamlit run frontend.py
```

Then open the local Streamlit URL shown in the terminal.

## Run Tests

```bash
uv run pytest -v
```

The test suite verifies:

- New memory starts empty
- Conversation messages are stored correctly
- Separate memory instances remain independent

## Memory Scope

This project specifically demonstrates **short-term conversational memory**.

It does not implement:

- Long-term persistent memory
- Vector databases
- Retrieval-Augmented Generation (RAG)
- Cross-session user memory

Those capabilities are intentionally outside the scope of this project.

## Key Learning Outcomes

This project demonstrates:

- Building LLM applications with LangChain
- Short-term conversational memory
- Multi-turn conversation handling
- Prompt engineering
- Few-shot prompting
- Context-window management
- Token-aware message trimming
- Streamlit session-state management
- Session isolation
- Secure API-key configuration
- Automated testing of memory behavior
- Git/GitHub project management