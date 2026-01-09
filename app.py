import streamlit as st
from agent.langgraph_flow import run_agent
import utils.config as config
from tools.faq_tool import initialize_vector_store

# Page configuration
st.set_page_config(
    page_title="CX Agent for Stanza Living",
    page_icon="🏠",
    layout="wide"
)

# Sidebar for API key configuration
st.sidebar.title("⚙️ Configuration")
st.sidebar.markdown("""
### API Key Setup
This chatbot uses **Groq API** for AI-powered responses.

To use this application:
1. Get your free API key from [Groq Console](https://console.groq.com)
2. Enter your API key below
3. Start chatting!
""")

# API Key input with session state
if 'groq_api_key' not in st.session_state:
    st.session_state.groq_api_key = ""

groq_api_key = st.sidebar.text_input(
    "Groq API Key",
    type="password",
    value=st.session_state.groq_api_key,
    help="Enter your Groq API key. Get one for free at https://console.groq.com"
)

if groq_api_key:
    st.session_state.groq_api_key = groq_api_key
    config.GROQ_API_KEY = groq_api_key
    st.sidebar.success("✅ API Key configured!")
else:
    st.sidebar.warning("⚠️ Please enter your Groq API key to use the chatbot")

# Initialize the vector store only once
if 'vector_store_initialized' not in st.session_state:
    try:
        config.VECTOR_STORE = initialize_vector_store()
        st.session_state.vector_store_initialized = True
    except Exception as e:
        st.error(f"Error initializing vector store: {str(e)}")

# Streamlit app title
st.title("🏠 CX Agent for STANZA LIVING")
st.markdown("---")

def main():
    # Check if API key is provided
    if not st.session_state.groq_api_key:
        st.warning("👈 Please enter your Groq API key in the sidebar to start using the chatbot")
        st.info("""
        ### How to get a Groq API Key:
        1. Visit [Groq Console](https://console.groq.com)
        2. Sign up or log in
        3. Navigate to API Keys section
        4. Create a new API key
        5. Copy and paste it in the sidebar
        """)
        return

    # User ID input
    user_id = st.text_input("Enter your user ID:", placeholder="e.g., U101")

    if user_id:
        st.info("💡 You can ask about FAQs, tickets, payments, or user information.")

    # Query input
    user_query = st.text_input("Please mention what you are looking for:", placeholder="e.g., What time is check-in?")

    if user_query:
        try:
            with st.spinner("🤔 Processing your query..."):
                # Call the agent to process the query
                response = run_agent(user_query=user_query, user_id=user_id)

            # Show agent's response
            st.success(f"**Agent:** {response.get('final_response')}")

            # Feedback section
            st.markdown("---")
            feedback = st.radio("Was this issue resolved?", ["yes", "no"], key="feedback")

            # If issue is resolved, break the flow
            if feedback == "yes":
                st.balloons()
                st.success("Thank you for your feedback. Have a great day!")
                return  # Exit the function to end the flow

            # If the issue is not resolved, ask if a ticket was created
            if response.get("escalation_status") == "ticket_created":
                st.warning(f"📝 Ticket created: **{response.get('ticket_id')}**")
                st.info("Our support team will reach out to you soon.")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.error("Please check if your API key is valid and try again.")

if __name__ == "__main__":
    main()
