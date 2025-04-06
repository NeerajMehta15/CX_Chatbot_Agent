#The LangGraph flow is the orchestration layer of your agent — it defines how each part (node) connects and runs in a logical sequence based on user input and state.

from langgraph.graph import StateGraph, END
from agent.classify_node import classify_node
from agent.escalation_node import escalation_node
from agent.faq_response_node import faq_response_node
from agent.ticket_response_node import ticket_response_node
from agent.payment_response_node import payment_response_node
from agent.user_info_response_node import user_info_response_node

# 1. Define the state schema
state_schema = {
    "user_query": str,
    "user_id": str,
    "intent": str,
    "feedback": str,
    "ticket_id": str,
    "escalation_status": str,
    "final_response": str
}

# 2. Create the LangGraph flow
graph = StateGraph(state_schema=state_schema)

# 3. Add nodes
graph.add_node("classify", classify_node)
graph.add_node("faq_response", faq_response_node)
graph.add_node("ticket_response", ticket_response_node)
graph.add_node("payment_response", payment_response_node)
graph.add_node("user_info_response", user_info_response_node)
graph.add_node("escalate", escalation_node)

# 4. Add routing logic using conditional edges
graph.set_entry_point("classify")

graph.add_conditional_edges(
    "classify",
    {
        "faq": "faq_response",
        "ticket": "ticket_response",
        "payment": "payment_response",
        "user_info": "user_info_response",
        "fallback": "escalate"
    }
)

# After response, escalate if feedback == "no"
graph.add_conditional_edges("faq_response", {"no": "escalate", "yes": END})
graph.add_conditional_edges("ticket_response", {"no": "escalate", "yes": END})
graph.add_conditional_edges("payment_response", {"no": "escalate", "yes": END})
graph.add_conditional_edges( "user_info_response", {"no": "escalate", "yes": END})
graph.add_edge("escalate", END)

# 5. Compile the graph
cx_agent_graph = graph.compile()
