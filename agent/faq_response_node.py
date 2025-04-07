from tools.faq_tool import get_faq_answer
import utils.config as config


def faq_response_node(state: dict) -> dict:
    """
    Responds to a user query classified as 'faq' using the FAQ vector store.
    
    Requires:
    - 'user_query'
    
    Returns:
    - Updated state with 'final_response'
    """
    user_query = state.get("user_query")

    # Call the FAQ retrieval tool
    answer = get_faq_answer(user_query, vector_store=config.VECTOR_STORE, config=config)

    return {
        **state,
        "final_response": answer
    }