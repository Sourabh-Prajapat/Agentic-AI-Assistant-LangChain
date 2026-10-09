import os
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver


# Sample student database
students = {
    "Sourabh": {
        "branch": "Mechanical Engineering",
        "year": 4,
        "attendance": 87
    },
    "Priya": {
        "branch": "Computer Science",
        "year": 3,
        "attendance": 91
    },
    "Nidhi": {
        "branch": "Electrical Engineering",
        "year": 4,
        "attendance": 84
    }
}


@tool
def calculator(a: float, b: float, operation: str) -> float | str:
    """Perform a mathematical operation on two numbers.

    Args:
        a: The first number.
        b: The second number.
        operation: add, subtract, multiply, or divide.
    """
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            return "Cannot divide by zero."
        return a / b

    return "Unsupported operation."


@tool
def get_student_info(name: str) -> dict:
    """Get a student's branch, year of study, and attendance.

    Args:
        name: The student's name.
    """
    if name in students:
        return students[name]

    return {"error": "Student not found"}


@tool
def get_student_attendance(name: str) -> int | dict:
    """Get the attendance percentage of a student.

    Args:
        name: The student's name.
    """
    if name in students:
        return students[name]["attendance"]

    return {"error": "Student not found"}


if not os.getenv("GEMINI_API_KEY"):
    raise ValueError(
        "Please set the GEMINI_API_KEY environment variable."
    )


model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)


system_prompt = (
    "You are a helpful student assistant. "
    "Use the available tools to retrieve student information "
    "and perform calculations when needed. "
    "Do not invent student data. "
    "If a student is not found, explain that clearly."
)


# Use a persistent SQLite database for conversation history.
with SqliteSaver.from_conn_string("checkpoints.db") as checkpointer:

    agent = create_agent(
        model=model,
        tools=[
            calculator,
            get_student_info,
            get_student_attendance
        ],
        system_prompt=system_prompt,
        checkpointer=checkpointer
    )

    # Messages with this ID belong to the same conversation.
    config = {
        "configurable": {
            "thread_id": "session_1"
        }
    }

    while True:
        print("\n")
        print("=" * 30)
        print("Type 'exit' to quit.")
        print("=" * 30)

        question = input("\nAsk: ").strip()

        if question.lower() == "exit":
            print("Assistant: Goodbye!")
            break

        if not question:
            continue

        try:
            result = agent.invoke(
                {
                    "messages": [
                        HumanMessage(content=question)
                    ]
                },
                config=config
            )

            content = result["messages"][-1].content

            print("\nAssistant:")

            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict):
                        if block.get("type") == "text":
                            print(block["text"])
                    elif hasattr(block, "text"):
                        print(block.text)
            else:
                print(content)

        except Exception as error:
            print(f"\nAn error occurred: {error}")