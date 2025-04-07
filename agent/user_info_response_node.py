from tools.user_info_tool import get_user_info


def user_info_response_node(state: dict) -> dict:
    """
    Responds to a user query classified as 'user_info' by fetching user profile details.
    
    Requires:
    - 'user_id'
    
    Returns:
    - Updated state with 'final_response'
    """
    user_id = state.get("user_id")
    answer = get_user_info(user_id, file_path="./data/user_info.csv")

    return {
        **state,
        "final_response": answer
    }