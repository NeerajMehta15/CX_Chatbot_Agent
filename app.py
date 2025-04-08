import streamlit as st
from agent.langgraph_flow import run_agent
import utils.config as config
from tools.faq_tool import initialize_vector_store

# Initialize the vector store
config.VECTOR_STORE = initialize_vector_store()

# Streamlit app title
st.title("CX Agent for STANZA LIVING")

def main():
    # User ID input
    user_id = st.text_input("Enter your user ID:")

    if user_id:
        st.write("You can type 'exit' anytime to quit.")

    # Query input
    user_query = st.text_input("Please mention what you are looking for:")

    if user_query:
        # Call the agent to process the query
        response = run_agent(user_query=user_query, user_id=user_id)

        # Show agent's response
        st.write(f"**Agent:** {response.get('final_response')}")

        # Feedback section
        feedback = st.radio("Was this issue resolved?", ["yes", "no"])

        # If issue is resolved, break the flow
        if feedback == "yes":
            st.write("Thank you for your feedback. Have a great day!")
            return  # Exit the function to end the flow

        # If the issue is not resolved, ask if a ticket was created
        if response.get("escalation_status") == "ticket_created":
            st.write(f"Ticket ID: {response.get('ticket_id')}")

if __name__ == "__main__":
    main()
