import json
import os
import csv
from langchain_core.tools import tool

@tool
def get_claim(employee_name:str)->str:
    """Fetches the pending expense claim details for a given employee name from claims.json."""    
    try:
        with open("claims.json","r") as f:
            claims_data = json.load(f)
        print(f"\n👉 [DEBUG] Python read claims.json and found these keys: {list(claims_data.keys())}")
        print(f"👉 [DEBUG] Looking for: '{employee_name}'")
        for name, details in claims_data.items():
            if name.lower() == employee_name.lower():
                return json.dumps({name: details})
        return f"No pending claims found for {employee_name}"
    except Exception as e:
        return f"Errror reading claims database:{str(e)}"

@tool
def check_policy()->str:
    """Reads and returns the company expense policy guidelines from policy.txt."""
    try:
        with open("policy.txt","r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading policy document:{str(e)}"

@tool
def write_ledger(employee_name:str,item:str,amount:int,status:str)->str:
    """Logs the finalized expense claim into the company ledger (ledger.csv). Call this ONLY after checking the policy and getting necessary approvals."""    
    try:
        file_exists = os.path.isfile("ledger.csv")
        with open("ledger.csv","a",newline="") as f:
            writer = csv.writer(f)
            if not file_exists or os.stat("ledger.csv").st_size ==0:
                writer.writerow(["Name", "Item", "Amount", "Status"])
            writer.writerow([employee_name,item,amount,status])
        return f"Successfully logged {status} claim for {employee_name} into ledger"
    except Exception as e:
        return f"Error writing to ledger:{str(e)}"

@tool
def ask_human(prompt: str) -> str:
    """Prompts a human manager in the terminal for approval when policy limits are exceeded. Pass a clear reason to the prompt."""
    print(f"\n⚠️  [AGENT REQUESTING MANAGER APPROVAL] ⚠️")
    print(f"Reason: {prompt}")
    response = input("\nYour Response (e.g., 'Approved', 'Rejected', or specific instructions): ")
    return response

agent_tools = [get_claim, check_policy, write_ledger, ask_human]