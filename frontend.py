import uuid

import streamlit as st

import backend


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Short-Term Memory Chatbot",
    page_icon="💬",
    layout="centered",
)

st.title("💬 Short-Term Memory Chatbot")

st.caption(
    "Conversational AI powered by OpenAI + LangChain "
    "with session-based short-term memory."
)


# ---------------------------------------------------------
# Initialize session state
# ---------------------------------------------------------

if "memory" not in st.session_state:
    st.session_state.memory = backend.create_memory()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:
    st.header("Controls")

    if st.button(
        "Clear Conversation",
        use_container_width=True,
    ):
        st.session_state.memory = backend.create_memory()
        st.session_state.chat_history = []
        st.session_state.session_id = str(uuid.uuid4())

        st.rerun()

    st.divider()

    st.markdown(
        """
        **About**

        This chatbot demonstrates short-term conversational
        memory using LangChain and Streamlit.

        Conversation context is maintained only during the
        active session.
        """
    )


# ---------------------------------------------------------
# Display conversation history
# ---------------------------------------------------------

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])


# ---------------------------------------------------------
# User input
# ---------------------------------------------------------

input_text = st.chat_input("Ask me anything...")


if input_text:

    # Display user message
    with st.chat_message("user"):
        st.markdown(input_text)

    st.session_state.chat_history.append(
        {
            "role": "user",
            "text": input_text,
        }
    )


    # Generate assistant response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response, updated_memory = backend.run_conversation(
                input_text=input_text,
                memory=st.session_state.memory,
                session_id=st.session_state.session_id,
            )

        st.markdown(response)


    # Update memory
    st.session_state.memory = updated_memory

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "text": response,
        }
    )