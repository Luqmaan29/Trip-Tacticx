# booking_agent.py
from utils.groq_wrapper import ask_groq

def run_booking_agent(prompt, per_person_transport_budget, group_size):
    """
    per_person_transport_budget: budget per person allocated for transport (number)
    group_size: number of travelers
    Returns: AI response text describing transport options within that per-person budget.
    """
    messages = [
        {
            "role": "system",
            "content": (
                f"You are a travel booking agent. Suggest transport options (bus, train, flight) between two cities "
                f"within the given per-person transport budget: {per_person_transport_budget:.2f}. "
                f"Group size: {group_size}. Provide realistic timings, price ranges (per-person and group estimates), and duration. "
                "If the per-person budget is too low for flights, suggest trains or buses and propose a cost-saving alternative (overnight travel, flexible dates, etc.)."
            )
        },
        {"role": "user", "content": prompt},
    ]
    return ask_groq("gemma2-9b-it", messages)
