from tools.ticket_tool import get_open_ticket_status


def ticket_response_node(state: dict) -> dict:
    """
    Responds to a user query classified as 'ticket' by fetching open ticket status.
    
    Requires:
    - 'user_id'
    
    Returns:
    - Updated state with 'final_response'
    """
    user_id = state.get("user_id")
    answer = get_open_ticket_status(user_id, file_path="./data/tickets.csv")

    return {
        **state,
        "final_response": answer
    }