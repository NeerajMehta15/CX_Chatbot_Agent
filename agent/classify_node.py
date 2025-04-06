from langchain.chat_models import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
import config


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

    system_prompt = (
        "You are a helpful assistant for classifying customer support queries.\\n"
        "Classify the following user query into one of these categories: faq, ticket, payment, user_info, fallback.\\n"
        "Just reply with one word — the category name."
    )

    few_shots = [
        ("What time is check-in?", "faq"),
        ("My Wi-Fi is not working", "ticket"),
        ("When is my rent due?", "payment"),
        ("What is my room number?", "user_info"),
        ("Hi", "fallback")
    ]

    examples = "\\n".join([f"Query: {q}\\nAnswer: {a}" for q, a in few_shots])
    final_prompt = (f"{system_prompt}\\n\\n{examples}\\n\\nQuery: {user_query}\\nAnswer:")

    llm = ChatGroq(groq_api_key=config.GROQ_API_KEY,model_name="llama3-70b-8192")

    response = llm.invoke([SystemMessage(content="You are a classification assistant."),HumanMessage(content=final_prompt)])

    intent = response.content.strip().lower()

    return {**state,"intent": intent}