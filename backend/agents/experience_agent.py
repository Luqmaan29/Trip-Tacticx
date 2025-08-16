from utils.groq_wrapper import ask_groq

def run_experience_agent(prompt, budget, days, preferences):
    """
    Generates a detailed day-by-day travel experience itinerary.

    Parameters:
    - prompt (str): The user prompt describing the trip context.
    - budget (float): Per-person budget for experiences (already calculated in run_multi_agent).
    - days (int): Number of days in the itinerary.
    - preferences (str): Traveler preferences for experiences.

    Returns:
    - str: The AI-generated itinerary.
    """
    messages = [
        {
            "role": "system",
            "content": (
                f"You are a travel experience planner. Create a day-by-day itinerary for {days} days "
                f"that matches these preferences: {preferences}. "
                f"Ensure total experience costs fit within {budget:.2f} per person. "
                "Balance famous attractions with unique local experiences. "
                "Mention entry fees, travel time between activities, and a short tip for each day."
            )
        },
        {"role": "user", "content": prompt},
    ]

    return ask_groq("gemma2-9b-it", messages)
