# Autonomous AI Office Operator

A proof-of-concept autonomous agent built for the Founding Engineer Placement Challenge. 

This prototype addresses the problem of fragmented company tasks. Instead of just answering questions, this agent autonomously bridges disparate systems—reading databases, checking company policy documents, and updating ledgers—while knowing exactly when to stop and ask for human manager approval.

## 🎯 The Use Case: Expense Auditing
The system handles an end-to-end expense claim workflow:
1. Receives an unstructured command (`"Process Rahul's expense claim"`).
2. Autonomously fetches the claim from the database (`claims.json`).
3. Reads the company rules (`policy.txt`).
4. Evaluates the claim against the policy threshold (₹10,000).
5. **Human-in-the-Loop:** If the claim exceeds the limit, the agent halts its state and prompts the user in the terminal for authorization.
6. Persists the final approved/rejected state to the company ledger (`ledger.csv`).

## 🧠 Architecture
This project utilizes a **ReAct (Reason + Act)** architecture to fulfill the core loop: `Goal → Understand → Plan → Execute → Observe → Adapt → Verify → Complete`.

*   **LLM Core:** Google Gemini 2.5 Flash via Function Calling.
*   **Orchestration:** LangGraph (Managing the state loop between reasoning and tool execution).
*   **Execution Layer:** Python-based `@tool` functions handling local file I/O to simulate internal company systems.

## ⚙️ How to Run Locally

Ensure you have Python 3 installed. Clone the repository and install the required dependencies:
```bash
pip install langgraph langchain-google-genai python-dotenv

## The Dummy Environment
The agent interacts with local files to simulate enterprise systems. The repository includes:
- `policy.txt`: Contains the static text: "All flights under ₹10,000 are auto-approved. Anything above requires human manager approval."
- `claims.json`: Simulates an HR database containing a pending ₹15,000 flight claim for "Rahul".
- `ledger.csv`: A simple CSV with headers `Name,Item,Amount,Status` where the agent logs completed work.

## The Python Tools (tools.py)
The agent relies on four specific tools, annotated with descriptive docstrings so the LLM knows when to trigger them:
- `get_claim`: Reads the JSON database (case-insensitive).
- `check_policy`: Reads the HR text file.
- `write_ledger`: Appends verified data to the CSV.
- `ask_human`: Pauses the execution state via `input()` to request terminal feedback before proceeding.

## Environment Setup
Create a `.env` file in the root directory and add your Google Gemini API key:
```env
GOOGLE_API_KEY=your_api_key_here



