# Short-Term Memory Chatbot

A conversational AI chatbot built with **Python, LangChain, OpenAI, and Streamlit** that maintains short-term conversational context during an active user session.

The project demonstrates how an LLM application can remember previous messages, manage conversation history, control context size, and maintain independent chat sessions.

---

## Features

- Multi-turn conversational AI
- Session-based short-term memory
- LangChain message-history management
- Token-aware conversation-history trimming
- Independent Streamlit sessions
- Conversation reset functionality
- Interactive Streamlit chat interface
- Environment-variable API key management
- Automated memory tests with Pytest
- Error handling and terminal logging

---

## Architecture

```text
                    User
                     │
                     ▼
              Streamlit Chat UI
                     │
                     ▼
                Session State
               ┌─────┴─────┐
               │           │
          Session ID   Chat History
               │
               ▼
      In-Memory Message History
               │
               ▼
        Token-Based Trimming
               │
               ▼
             Chat Prompt
               │
               ▼
           GPT-4o-mini
               │
               ▼
           AI Response
               │
               ▼
          Memory Updated
```

---

## How Short-Term Memory Works

Each Streamlit session creates its own in-memory conversation history and unique session ID.

When a user sends a message:

1. The user message is received through the Streamlit interface.
2. The current conversation history is retrieved.
3. Older messages are trimmed when necessary to control context size.
4. Relevant conversation history is inserted into the prompt.
5. The prompt is sent to the OpenAI language model.
6. The assistant generates a response.
7. The user message and assistant response are stored in the current session history.
8. The updated conversation history is used for subsequent messages.

This allows the chatbot to answer follow-up questions using information from earlier turns.

The memory is intentionally **session-based and non-persistent**.

---

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

The chatbot uses previous messages in the current conversation to answer follow-up questions.

---

## Conversation Reset

The **Clear Conversation** button in the Streamlit sidebar resets the active conversation.

When clicked, it:

- Creates a new empty memory
- Clears the displayed chat history
- Generates a new session ID

This prevents information from the previous conversation from carrying into the new conversation.

---

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
- Git
- GitHub

---

## Project Structure

```text
memory_chatbot/
│
├── tests/
│   └── test_memory.py
│
├── backend.py
├── frontend.py
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md
```

### `backend.py`

Contains the core chatbot logic, including:

- OpenAI model configuration
- LangChain prompt
- Short-term conversation memory
- Token-based message trimming
- Conversation execution
- Error handling

### `frontend.py`

Contains the Streamlit user interface, including:

- Chat interface
- Session state
- Session ID management
- Displayed conversation history
- Conversation reset functionality

### `tests/test_memory.py`

Contains automated tests for the short-term memory implementation.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/nakkaganesh/memory_chatbot.git
cd memory_chatbot
```

---

## Install Dependencies

### Using uv

Install the project dependencies:

```bash
uv sync
```

### Using pip

Alternatively:

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_openai_api_key
```

The `.env` file contains sensitive information and should **never be committed to GitHub**.

Make sure `.env` is included in `.gitignore`.

---

## Run the Application

Start the Streamlit application:

```bash
uv run streamlit run frontend.py
```

Streamlit will display a local URL, typically:

```text
http://localhost:8501
```

Open the URL in your browser to use the chatbot.

---

## Testing

Run the automated test suite with:

```bash
uv run pytest -v
```

The test suite verifies:

- New memory starts empty
- Conversation messages are stored correctly
- Separate memory instances remain independent

Current test result:

```text
3 passed
```

A LangChain deprecation warning may currently appear during testing. It does not cause the tests to fail.

---

## Memory Scope

This project specifically demonstrates **short-term conversational memory**.

The chatbot remembers information only within the active conversation session.

It does not implement:

- Long-term persistent memory
- Vector databases
- Retrieval-Augmented Generation (RAG)
- Cross-session user memory
- Database-backed conversation storage

These capabilities are intentionally outside the scope of this project.

---

## Security

The OpenAI API key is loaded from an environment variable using `python-dotenv`.

The API key should be stored in:

```text
.env
```

and must not be hardcoded inside Python files or committed to GitHub.

---

## Known Limitations

- Conversation memory is stored in memory and is not persistent.
- Restarting the application removes conversation state.
- The project intentionally demonstrates short-term memory only.
- Conversation history is limited to control context size and token usage.
- The current LangChain message-history APIs emit deprecation warnings and may be migrated to LangGraph persistence in a future version.

---

## Key Learning Outcomes

This project demonstrates:

- Building an LLM application with LangChain
- Integrating OpenAI models with Python
- Implementing short-term conversational memory
- Handling multi-turn conversations
- Prompt engineering
- Context-window management
- Token-aware message trimming
- Streamlit session-state management
- Session isolation
- Secure API-key configuration
- Exception handling
- Automated testing with Pytest
- Dependency management with uv
- Git and GitHub project management

---

## Future Improvements

Possible future enhancements include:

- Migration to LangGraph-based memory and persistence
- Persistent conversation history
- SQLite or PostgreSQL integration
- Retrieval-Augmented Generation (RAG)
- Vector database integration
- Document-based question answering
- User authentication
- Conversation management
- Docker containerization
- Cloud deployment

---

## Author

**Ganesh Nakka**

AI / Machine Learning & Agentic AI Engineer

GitHub: `nakkaganesh`

---

## License

This project is intended for educational and portfolio purposes.