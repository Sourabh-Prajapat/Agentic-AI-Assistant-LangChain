# 🤖 Agentic AI Assistant — LangChain

A Python-based AI assistant powered by Google Gemini and LangChain that intelligently selects tools to answer student-related questions and perform mathematical calculations.

## ✨ Features

* 🧠 **Gemini-Powered AI** — Understands user questions and generates natural-language responses.
* 🛠️ **LLM Tool Calling** — Selects appropriate Python tools based on the user's request.
* 🧮 **Mathematical Calculations** — Supports addition, subtraction, multiplication, and division.
* 🎓 **Student Information Retrieval** — Retrieves student branch, year of study, and attendance.
* 📊 **Attendance Lookup** — Retrieves attendance percentages for registered sample students.
* 🔄 **Multi-Tool Workflows** — Can combine tool calls to answer questions requiring multiple steps.
* 💬 **Interactive Terminal Interface** — Accepts questions directly from the command line.

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
        ┌───────┼────────┐
        ▼       ▼        ▼
   Calculator  Student   Attendance
               Info       Lookup
        │       │          │
        └───────┼──────────┘
                ▼
          Tool Results
                │
                ▼
           Gemini LLM
                │
                ▼
          Final Answer
```

The agent receives a question, determines whether a tool is needed, executes the selected tool through LangChain, and uses the result to generate a response.

## 🛠️ Available Tools

| Tool                     | Description                                                  |
| ------------------------ | ------------------------------------------------------------ |
| `calculator`             | Performs addition, subtraction, multiplication, and division |
| `get_student_info`       | Retrieves a student's branch, year, and attendance           |
| `get_student_attendance` | Retrieves a student's attendance percentage                  |

## 💡 Example Queries

Try asking the assistant:

* `What is 125 multiplied by 8?`
* `What is 25 multiplied by 8, then subtract 60?`
* `Tell me about Sourabh.`
* `What is Priya's attendance?`
* `What branch is Nidhi studying in?`
* `What is Sourabh's attendance, and how many percentage points does he need to reach 95%?`
* `Tell me about Rahul.`

The sample database contains Sourabh, Priya, and Nidhi. Questions about students who aren't registered should receive a not-found response.

## 🧰 Technologies Used

* **Language:** Python
* **LLM:** Google Gemini
* **Framework:** LangChain
* **Integration:** `langchain-google-genai`
* **Concepts:** Agentic AI, LLM Tool Calling, Function Calling, Multi-Tool Workflows

## 📂 Project Structure

```text
Agentic AI Assistant LangChain/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Sourabh-Prajapat/Agentic-AI-Assistant-LangChain.git
cd "Agentic AI Assistant LangChain"
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure your Gemini API key

Set the API key in PowerShell:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

Replace `YOUR_API_KEY` with your actual Google Gemini API key.

Keep your API key private. Never hard-code it in your source files or upload it to GitHub.

### 5. Run the assistant

```bash
python main.py
```

Enter a question when prompted:

```text
Ask your assistant: What is Sourabh's attendance?
```

The assistant will process the question and display its response in the terminal.

## 📚 Learning Objectives

This project demonstrates:

* Integrating Google Gemini with LangChain.
* Defining Python functions as AI tools.
* Using docstrings and type hints to describe tools.
* Registering multiple tools with an agent.
* Letting an LLM select tools based on user questions.
* Executing tool calls and using their results in final responses.
* Building an interactive command-line AI application.

## 👨‍💻 Author

**Sourabh**
B.Tech Graduate, IIT Jammu

GitHub: [Sourabh-Prajapat](https://github.com/Sourabh-Prajapat)