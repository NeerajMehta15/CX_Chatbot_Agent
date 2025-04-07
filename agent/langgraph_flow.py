from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional

from agent.classify_node import classify_node
from agent.escalation_node import escalation_node
from agent.faq_response_node import faq_response_node
from agent.ticket_response_node import ticket_response_node
from agent.payment_response_node import payment_response_node
from agent.user_info_response_node import user_info_response_node


# Define the state schema using TypedDict
class AgentState(TypedDict):
    user_query: str
    user_id: str
    intent: str
    feedback: str
    ticket_id: Optional[str]
    escalation_status: Optional[str]
    final_response: Optional[str]


# Define intent-based routing function
def intent_router(state: AgentState) -> str:
    return state.get("intent", "fallback")


# Define feedback-based routing function
def feedback_router(state: AgentState) -> str:
    return state.get("feedback", "yes")


# Create LangGraph flow
graph = StateGraph(AgentState)

# Add nodes
graph.add_node("classify", classify_node)
graph.add_node("faq_response", faq_response_node)
graph.add_node("ticket_response", ticket_response_node)
graph.add_node("payment_response", payment_response_node)
graph.add_node("user_info_response", user_info_response_node)
graph.add_node("escalate", escalation_node)

# Entry point
graph.set_entry_point("classify")

# Conditional routing based on intent
graph.add_conditional_edges("classify", intent_router, {
    "faq": "faq_response",
    "ticket": "ticket_response",
    "payment": "payment_response",
    "user_info": "user_info_response",
    "fallback": "escalate"
})

# Conditional routing from each response node based on feedback
graph.add_conditional_edges("faq_response", feedback_router, {"no": "escalate","yes": END})
graph.add_conditional_edges("ticket_response", feedback_router, {"no": "escalate","yes": END})
graph.add_conditional_edges("payment_response", feedback_router, {"no": "escalate","yes": END})
graph.add_conditional_edges("user_info_response", feedback_router, {"no": "escalate","yes": END})

# Escalation ends the flow
graph.add_edge("escalate", END)

# Compile the graph
cx_agent_graph = graph.compile()

#Run agent code
def run_agent(user_query, user_id, feedback="yes"):
    initial_state = {
        "user_query": user_query,
        "user_id": user_id,
        "feedback": feedback
    }
    final_state = cx_agent_graph.invoke(initial_state)
    return final_state

