from utils.groq_wrapper import ask_groq

def run_stay_agent(prompt, budget, group_size, trip_type, preferences, days):
    """
    Generates accommodation recommendations for the trip.

    Parameters:
    - prompt (str): The user prompt describing the trip context.
    - budget (float): Per-person budget for accommodation (already calculated in run_multi_agent).
    - group_size (int): Number of people in the group.
    - trip_type (str): Type of trip (e.g., leisure, adventure, business).
    - preferences (str): Special accommodation preferences.
    - days (int): Number of nights to stay.

    Returns:
    - str: The AI-generated accommodation suggestions.
    """
    messages = [
        {
            "role": "system",
            "content": (
                f"You are a hotel and stay expert. Recommend accommodations within {budget:.2f} per person "
                f"for {days} nights. "
                f"Group size: {group_size}. Trip type: {trip_type}. Special preferences: {preferences}. "
                "If budget is tight, suggest hostels, guesthouses, or shared apartments. "
                "Provide price per night, total stay cost, location pros/cons, and a short justification."
            )
        },
        {"role": "user", "content": prompt},
    ]
    return ask_groq("gemma2-9b-it", messages)
