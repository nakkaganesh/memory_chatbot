from langchain_core.messages import AIMessage, HumanMessage

from backend import create_memory


def test_memory_starts_empty():
    memory = create_memory()

    assert memory.messages == []


def test_memory_stores_conversation():
    memory = create_memory()

    memory.add_message(HumanMessage(content="My name is Ganesh."))
    memory.add_message(AIMessage(content="Nice to meet you, Ganesh."))

    assert len(memory.messages) == 2
    assert memory.messages[0].content == "My name is Ganesh."
    assert memory.messages[1].content == "Nice to meet you, Ganesh."


def test_new_memory_is_independent():
    memory_one = create_memory()
    memory_two = create_memory()

    memory_one.add_message(
        HumanMessage(content="Remember this.")
    )

    assert len(memory_one.messages) == 1
    assert memory_two.messages == []