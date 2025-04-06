import pandas as pd
from datetime import datetime

def load_ticket_data(file_path):
    """Load ticket data from CSV."""
    ticket_data = pd.read_csv(file_path)
    return ticket_data

def get_open_ticket_status(user_id: str, file_path):
    """
    Get the latest open ticket info for a user.

    Args:
        user_id (str): The user's ID.
        file_path (str): Path to the tickets CSV file.

    Returns:
        str: Status of open ticket or a message if none found.
    """
    df = load_ticket_data(file_path)
    open_tickets = df[(df["user_id"] == user_id) & (df["status"] == "open")]

    if open_tickets.empty:
        return "You don't have any open support tickets at the moment."

    latest_ticket = open_tickets.sort_values(by="created_at", ascending=False).iloc[0]
    return (
        f"Your open ticket (ID: {latest_ticket['ticket_id']}) "
        f"is regarding: '{latest_ticket['issue']}'. It is currently marked as: {latest_ticket['status']}."
    )


def create_ticket(user_id: str, issue: str, file_path):
    """
    Create a new support ticket for a user.

    Args:
        user_id (str): The user's ID.
        issue (str): A summary of the unresolved issue.
        file_path (str): Path to the tickets CSV file.

    Returns:
        str: Confirmation message with ticket ID.
    """
    df = load_ticket_data(file_path)

    new_ticket = {
        "ticket_id": f"T{int(datetime.now().timestamp())}",
        "user_id": user_id,
        "issue": issue,
        "status": "open",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    df = pd.concat([df, pd.DataFrame([new_ticket])], ignore_index=True)
    df.to_csv(file_path, index=False)

    return f"A support ticket has been created for you. Your ticket ID is {new_ticket['ticket_id']}."