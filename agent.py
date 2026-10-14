import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from tools import agent_tools
load_dotenv()

if not os.environ.get("GOOGLE_API_KEY"):
    print("❌ Error: GOOGLE_API_KEY not found. Please create a .env file and add your key.")
    exit(1)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0)
agent_executor = create_react_agent(llm,agent_tools)

def run_agent():
    print("🤖 Autonomous Company Operator initialized.")
    print("Type your request below (or type 'exit' to quit).\n")

    while True:
        user_input = input("Manager: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        print("\n--- Agent Execution Log ---")

        events = agent_executor.stream(
            {"messages": [("user", user_input)]},
            stream_mode="values"
        )
        for event in events:
            message = event["messages"][-1]
            if hasattr(message,'tool_calls') and message.tool_calls:
                for tc in message.tool_calls:
                    print(f"⚙️  Action: Agent decided to call '{tc['name']}' with arguments: {tc['args']}")
            elif message.content and message.type == "ai":
                print(f"✅ Final Result: {message.content}\n")

if __name__ == "__main__":
    run_agent()

