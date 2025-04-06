import pandas as pd

def load_user_info(file_path):
    """Load user info data from CSV."""
    return pd.read_csv(file_path)


def get_user_info(user_id: str, file_path):
    """
    Get user profile info (room, city, check-in date, etc.).

    Args:
        user_id (str): The user's ID.
        file_path (str): Path to the user info CSV file.

    Returns:
        str: A summary of the user's info or an error message.
    """
    df = load_user_info(file_path)
    user_row = df[df["user_id"] == user_id]

    if user_row.empty:
        return "Sorry, I couldn't find your profile information."

    user = user_row.iloc[0]
    return (
        f"Here's your profile info:\n"
        f"Name: {user['name']}\n"
        f"Room No: {user['room_no']}\n"
        f"City: {user['city']}\n"
        f"Check-in Date: {user['checkin_date']}"
    )
