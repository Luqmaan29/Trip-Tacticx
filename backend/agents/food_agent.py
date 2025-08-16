from utils.groq_wrapper import ask_groq

def run_food_agent(prompt, budget, days):
    """
    Generates a food and dining guide for the trip.

    Parameters:
    - prompt (str): The user prompt describing the trip context.
    - budget (float): Per-person budget for food (already calculated in run_multi_agent).
    - days (int): Number of days in the itinerary.

    Returns:
    - str: The AI-generated food and dining guide.
    """
    messages = [
        {
            "role": "system",
            "content": (
                f"You are a food guide for travelers. Suggest famous local dishes and the best places to eat. "
                f"Include street food, popular restaurants, and unique culinary experiences. "
                f"Budget for food is about {budget:.2f} per person for the entire trip "
                f"(~{budget / days:.2f} per day). "
                "Mention approximate prices and why the food is special."
            )
        },
        {"role": "user", "content": prompt},
    ]
    return ask_groq("gemma2-9b-it", messages)
