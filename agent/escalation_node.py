from tools.ticket_tool import create_ticket
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
import utils.config as config


def summarize_issue(user_query: str) -> str:
    """Use Groq LLM to summarize user query for ticket description."""
    llm = ChatGroq(groq_api_key=config.GROQ_API_KEY, model_name="llama3-70b-8192")

    prompt = f"Summarize the following issue clearly for creating a support ticket:\n\n{user_query}"
    response = llm.invoke([
        SystemMessage(content="You are a helpful assistant for writing support ticket summaries."),
        HumanMessage(content=prompt)
    ])
    return response.content.strip()


def escalation_node(state: dict) -> dict:
    """
    Escalates unresolved queries by creating a support ticket.
    
    Requires:
    - 'user_id'
    - 'user_query'
    - 'feedback' == 'no'
    
    Returns:
    - 'ticket_id'
    - 'final_response'
    - 'escalation_status'
    """
    user_id = state.get("user_id")
    user_query = state.get("user_query")
    feedback = state.get("feedback", "").lower()

    if feedback != "no":
        return {**state, "escalation_status": "not_triggered"}

    #Summarize issue with LLM
    issue_summary = summarize_issue(user_query)

    #Create ticket using your existing tool
    ticket_id = create_ticket(user_id, issue_summary, file_path="./data/tickets.csv")

    return {
        **state,
        "ticket_id": ticket_id,
        "escalation_status": "ticket_created",
        "final_response": f"A support ticket has been created for you. Your ticket ID is {ticket_id}."
    }