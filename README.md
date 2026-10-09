# 🤖 Agentic AI Assistant — LangChain

### An intelligent AI assistant powered by Python, LangChain, LangGraph, and Google Gemini.

A terminal-based AI assistant that intelligently selects tools to answer student-related questions, retrieve student information, and perform mathematical calculations. Built with LangChain and LangGraph, it uses SQLite checkpointing to persist conversation state, enabling contextual follow-up questions even after restarting the application.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/LangChain-Agentic%20AI-1C3C3C?style=for-the-badge" alt="LangChain" />
  <img src="https://img.shields.io/badge/LangGraph-Workflow%20Persistence-1C3C3C?style=for-the-badge" alt="LangGraph" />
  <img src="https://img.shields.io/badge/LLM-Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Google Gemini" />
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
</p>

---

## ✨ Features

* 🧠 **Gemini-Powered AI** — Understands user questions and generates natural-language responses.
* 🛠️ **LLM Tool Calling** — Selects and executes appropriate Python tools based on user requests.
* 🧮 **Mathematical Calculations** — Supports addition, subtraction, multiplication, and division.
* 🎓 **Student Information Retrieval** — Retrieves a student's branch, year of study, and attendance.
* 📊 **Attendance Lookup** — Retrieves attendance percentages for registered students.
* 🔄 **Multi-Tool Workflows** — Can combine tool calls to answer questions requiring multiple steps.
* 💬 **Multi-Turn Conversations** — Uses saved conversation state to understand contextual follow-up questions.
* 💾 **Persistent Conversation History** — Stores LangGraph checkpoints in a local SQLite database.
* 🧵 **Thread-Based Conversations** — Uses a configurable `thread_id` to identify and resume a conversation.
* 🖥️ **Interactive Terminal Interface** — Accepts questions continuously until the user types `exit`.
* 🔐 **Environment-Based API Key** — Reads the Gemini API key from an environment variable.

## 🧠 How It Works

```text
                  User Question
                        │
                        ▼
                 LangChain Agent
                        │
                        ▼
                    Gemini LLM
                        │
                        ▼
              Select Appropriate Tool
                        │
             ┌──────────┼──────────┐
             ▼          ▼          ▼
        Calculator   Student   Attendance
                       Info      Lookup
             │          │          │
             └──────────┼──────────┘
                        ▼
                   Tool Results
                        │
                        ▼
                    Gemini LLM
                        │
                        ▼
                   Final Answer
                        │
                        ▼
                Update Graph State
                        │
                        ▼
               SQLite Checkpointer
                        │
                        ▼
               Persistent Checkpoint
```

The agent receives a question and uses Google Gemini to determine whether a tool is needed. LangChain manages the agent and tool interactions, while LangGraph manages the agent's state.

When a tool is required, the agent executes it and uses the result to generate a natural-language response. The checkpointer saves the graph state in SQLite, allowing the application to restore conversation context for the same thread.

## 🛠️ Available Tools

### 🧮 1. Calculator — `calculator`

Performs mathematical operations on two numbers.

Supported operations:

* Addition
* Subtraction
* Multiplication
* Division, with a check for division by zero

### 🎓 2. Student Information — `get_student_info`

Retrieves a registered student's:

* Branch of study
* Year of study
* Attendance percentage

### 📊 3. Attendance Lookup — `get_student_attendance`

Retrieves the attendance percentage of a registered student independently.

All three tools are implemented as Python functions and registered with the LangChain agent using the `@tool` decorator. The agent can select the appropriate tool based on the user's request.

## 💡 Example Queries

### 🧮 Mathematical Calculations

```text
Ask: What is 125 multiplied by 8?

Ask: What is 25 multiplied by 8, then subtract 60?
```

### 🎓 Student Information

```text
Ask: Tell me about Sourabh.

Ask: What is Priya's attendance?

Ask: What branch is Nidhi studying in?
```

### 🔄 Multi-Step Questions

```text
Ask: What is Sourabh's attendance, and how many percentage
points does he need to reach 95%?
```

### 💬 Follow-Up Conversations

```text
Ask: Tell me about Sourabh.

Assistant: Sourabh is a fourth-year Mechanical Engineering
student with 87% attendance.

Ask: What is his attendance?

Assistant: Sourabh's attendance is 87%.
```

*Example responses are illustrative; the exact wording generated by Gemini may vary.*

## 🗃️ Sample Student Database

The project currently uses a Python dictionary containing sample student records.

| Student | Branch                 | Year | Attendance |
| ------- | ---------------------- | ---: | ---------: |
| Sourabh | Mechanical Engineering |    4 |        87% |
| Priya   | Computer Science       |    3 |        91% |
| Nidhi   | Electrical Engineering |    4 |        84% |

The assistant is instructed not to invent student data and to clearly report when a student is not found.

**Note:** Student records are stored in the Python source code. SQLite is used for conversation checkpoints, not as the student database.

## 💾 Persistent Conversation History

This project uses LangGraph checkpointing to save and restore conversation state through SQLite.

### 1. Create the SQLite Checkpointer

```python
with SqliteSaver.from_conn_string("checkpoints.db") as checkpointer:
```

* **`SqliteSaver`** provides SQLite-based checkpoint storage.
* **`from_conn_string()`** creates the saver using the specified database connection string.
* **`checkpointer`** holds the saver used by the agent.
* **`with`** manages the saver’s lifetime and resource cleanup.

### 2. Connect the Checkpointer to the Agent

```python
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
```

Passing `checkpointer=checkpointer` enables LangGraph to save and restore the agent's state.

### 3. Configure the Conversation Thread

```python
config = {
    "configurable": {
        "thread_id": "session_1"
    }
}
```

* **`configurable`** contains runtime configuration values.
* **`thread_id`** identifies the conversation whose state should be retrieved and updated.
* Reusing the same thread ID resumes that conversation when its saved checkpoints are available.

### 4. Invoke the Agent

```python
result = agent.invoke(
    {
        "messages": [
            HumanMessage(content=question)
        ]
    },
    config=config
)
```

The application sends only the new user message. LangGraph uses the checkpointer to load the existing state for the configured thread and saves updated state as the agent progresses.

### Benefits

* Conversation state is saved in `checkpoints.db`.
* Follow-up questions can use previous conversation messages.
* Conversation state can persist across application restarts.
* Different thread IDs can maintain separate conversations.

**Important:** The application currently uses the fixed thread ID `session_1`. Anyone running the application with the same database and thread ID will resume that thread. Use a distinct ID for each independent conversation. Checkpoints preserve conversation state; they do not guarantee unlimited context or permanent factual memory.

## 🧰 Technologies Used

| Technology                         | Purpose                                                |
| ---------------------------------- | ------------------------------------------------------ |
| Python                             | Application logic and tool implementation              |
| Google Gemini (`gemini-3.6-flash`) | Natural-language understanding and response generation |
| LangChain                          | Agent creation and tool integration                    |
| `langchain-google-genai`           | Integration between LangChain and Google Gemini        |
| LangGraph                          | Agent state management and checkpointing               |
| SQLite                             | Local persistent storage for conversation checkpoints  |
| `langgraph-checkpoint-sqlite`      | SQLite checkpoint saver integration                    |

**Key concepts:** Agentic AI, LLM Tool Calling, Function Calling, Multi-Tool Workflows, Stateful Agents, Checkpointing, Persistent Conversation History, Thread-Based State Management.

## 📂 Project Structure

```text
Agentic-AI-Assistant-LangChain/
│
├── main.py           # Agent, tools, and interactive conversation loop
├── requirements.txt  # Python dependencies
├── checkpoints.db    # SQLite database created at runtime
├── .gitignore        # Files excluded from Git
└── README.md         # Project documentation
```

`checkpoints.db` is generated when the application initializes the SQLite saver. It may not exist in a fresh clone until the application runs.

## 🚀 Getting Started

### Prerequisites

* Python installed on your system
* A Google Gemini API key
* Git

### 1. Clone the Repository

```bash
git clone https://github.com/Sourabh-Prajapat/Agentic-AI-Assistant-LangChain.git

cd Agentic-AI-Assistant-LangChain
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

Ensure that `requirements.txt` contains:

```text
langchain
langchain-google-genai
langgraph-checkpoint-sqlite
```

### 4. Configure Your Gemini API Key

Set your API key in Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

Replace `YOUR_API_KEY` with your actual Google Gemini API key.

Keep your API key private. Never hard-code it in your source files or upload it to GitHub.

### 5. Run the Assistant

```bash
python main.py
```

The assistant will prompt you to enter a question:

```text
Ask: What is Sourabh's attendance?
```

Continue asking questions and using follow-up messages. To exit the application, type:

```text
Ask: exit
```

### 6. Test Persistent Conversation History

1. Ask a question, such as `Tell me about Sourabh.`
2. Ask a follow-up, such as `What is his attendance?`
3. Type `exit` to close the application.
4. Restart the program using `python main.py`.
5. Ask `What were we discussing earlier?`

The assistant should be able to use the saved state from `session_1`, provided the SQLite database and checkpoints remain available.

## 📚 Learning Outcomes

This project demonstrates:

* Integrating Google Gemini with LangChain.
* Creating custom tools using Python and the `@tool` decorator.
* Describing tools with docstrings and type hints.
* Registering multiple tools with an AI agent.
* Enabling LLM-driven tool selection and execution.
* Using tool results to generate natural-language responses.
* Representing user messages with `HumanMessage`.
* Understanding LangGraph state and checkpointing.
* Connecting a SQLite checkpointer to a LangChain agent.
* Using `configurable` and `thread_id` to manage conversation state.
* Maintaining persistent, multi-turn conversation history.
* Building an interactive command-line AI application.
* Managing API credentials through environment variables.

---

## 👨‍💻 Author

**Sourabh**

B.Tech Graduate, IIT Jammu

GitHub: [Sourabh-Prajapat](https://github.com/Sourabh-Prajapat)

---

<p align="center">
  <i>Exploring Agentic AI, one tool at a time. 🚀</i>
</p>
