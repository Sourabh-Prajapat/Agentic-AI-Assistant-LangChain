import os
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent


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


agent = create_agent(
    model=model,
    tools=[
        calculator,
        get_student_info,
        get_student_attendance
    ],
    system_prompt=(
        "You are a helpful student assistant. "
        "Use the available tools to retrieve student information "
        "and perform calculations when needed. "
        "Do not invent student data. "
        "If a student is not found, explain that clearly."
    )
)


question = input("Ask your assistant: ")

result = agent.invoke({
    "messages": [
        {"role": "user", "content": question}
    ]
})


# Extract and print the final answer
final_message = result["messages"][-1]
content = final_message.content

if isinstance(content, list):
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            print(block["text"])
        elif hasattr(block, "text"):
            print(block.text)
else:
    print(content)