import pandas as pd

def load_payment_data(file_path):
    """Load payment data from CSV."""
    payment_data = pd.read_csv(file_path)
    return payment_data


def get_payment_status(user_id: str, file_path):
    """
    Get the latest payment info for a user.

    Args:
        user_id (str): The user's ID.
        file_path (str): Path to the payments CSV file.

    Returns:
        str: A human-readable summary of the payment.
    """
    df = load_payment_data(file_path)
    
    # Filter and sort by due_date descending (latest first)
    user_payments = df[df["user_id"] == user_id].sort_values(by="due_date", ascending=False)

    if user_payments.empty:
        return "I couldn't find any payment information for your account."

    latest_payment = user_payments.iloc[0]
    
    summary = (
        f"Your last recorded payment is ₹{latest_payment['amount']} "
        f"which was due on {latest_payment['due_date']}. "
        f"{'GST was applied.' if latest_payment['gst_applied'].lower() == 'yes' else 'GST was not applied.'} "
        f"Current payment status: {latest_payment['status']}."
    )
    
    return summary
