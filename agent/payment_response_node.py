from tools.payment_tool import get_payment_status


def payment_response_node(state: dict) -> dict:
    """
    Responds to a user query classified as 'payment' by fetching payment details.
    
    Requires:
    - 'user_id'
    
    Returns:
    - Updated state with 'final_response'
    """
    user_id = state.get("user_id")
    answer = get_payment_status(user_id, file_path="./data/payments.csv")

    return {
        **state,
        "final_response": answer
    }