from agent.langgraph_flow import run_agent

def main():
    print("Welcome to the CX Agent CLI 🚀")
    user_id = input("Enter your user ID: ").strip()
    print("You can type 'exit' anytime to quit.")

    while True:
        user_query = input("\\nYou: ").strip()
        if user_query.lower() in ["exit", "quit"]:
            print("Goodbye! 👋")
            break

        feedback = input("Was this issue resolved? (yes/no): ").strip().lower()
        response = run_agent(user_query=user_query, user_id=user_id, feedback=feedback)

        print(f"\\nAgent: {response.get('final_response')}")
        if response.get("escalation_status") == "ticket_created":
            print(f"Ticket ID: {response.get('ticket_id')}")

if __name__ == "__main__":
    main()