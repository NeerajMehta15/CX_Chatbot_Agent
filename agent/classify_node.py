from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
import utils.config as config

def classify_node(state: dict) -> dict:
    """
    Classify user intent using Groq's LLM via LangChain.

    Input state must contain:
    - 'user_query': the raw query
    - 'user_id': the user's ID

    Returns updated state with:
    - 'intent': one of ['faq', 'ticket', 'payment', 'user_info', 'fallback']
    """
    user_query = state.get("user_query", "")

    system_prompt = SystemMessage(content="""
You are a classification assistant for a residential support chatbot.

Classify user queries into one of the following:

- faq: If the user is asking about general info, help, or known issues like payment failures, service availability, policies, etc.
- ticket: Only if the user is **raising a personal complaint or service request** (e.g., "My Wi-Fi is not working", "There is a leak in my bathroom").
- payment: If the user asks about rent, GST, amount paid, due date, refunds, etc.
- user_info: If the user asks about their personal info like room number, check-in, ID details, address, etc.
- fallback: If you are not sure or the user is just greeting or unclear.

Examples:
Query: What time is check-in? → faq  
Query: My AC is not working → ticket  
Query: When is my rent due? → payment  
Query: What is my room number? → user_info  
Query: Hello → fallback

Only respond with one word: faq, ticket, payment, user_info, or fallback.
""")

    human_prompt = HumanMessage(content=f"Query: {user_query}\nAnswer:")

    # Use Groq’s LLM
    llm = ChatGroq(
        groq_api_key=config.GROQ_API_KEY,
        model_name="llama3-70b-8192"
    )

    response = llm.invoke([system_prompt, human_prompt])
    intent = response.content.strip().lower()

    return {**state, "intent": intent}
