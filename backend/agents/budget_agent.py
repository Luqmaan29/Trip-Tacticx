# budget_agent.py
from utils.groq_wrapper import ask_groq

# Dynamic allocation presets
BUDGET_PROFILES = {
    "Leisure":      {"transport": 0.20, "stay": 0.35, "experiences": 0.25, "food": 0.15, "misc": 0.05},
    "Adventure":    {"transport": 0.25, "stay": 0.25, "experiences": 0.35, "food": 0.10, "misc": 0.05},
    "Honeymoon":    {"transport": 0.15, "stay": 0.45, "experiences": 0.20, "food": 0.15, "misc": 0.05},
    "Solo":         {"transport": 0.20, "stay": 0.30, "experiences": 0.30, "food": 0.15, "misc": 0.05},
    "Business":     {"transport": 0.25, "stay": 0.40, "experiences": 0.15, "food": 0.15, "misc": 0.05}
}

# Cost-of-living multipliers
DESTINATION_COST = {
    "cheap": 0.8,
    "moderate": 1.0,
    "expensive": 1.3
}

def run_budget_agent(prompt, budget, group_size, days, trip_type="Leisure", cost_level="moderate"):
    """
    budget: per-person budget (number)
    returns: (ai_response_text, category_budgets) where category_budgets are GROUP totals
    """
    # Adjust budget for cost-of-living
    adjusted_budget_per_person = budget * DESTINATION_COST.get(cost_level, 1.0)

    # Total group budget (group totals returned)
    total_budget_group = adjusted_budget_per_person * group_size

    # Allocation profile
    allocation = BUDGET_PROFILES.get(trip_type, BUDGET_PROFILES["Leisure"])

    # Calculate category budgets (group totals)
    category_budgets = {cat: round(total_budget_group * pct, 2) for cat, pct in allocation.items()}

    # Prepare AI system message
    messages = [
        {
            "role": "system",
            "content": (
                f"You are a professional travel budget planner for a {days}-day {trip_type.lower()} trip. "
                f"Destination cost level: {cost_level}. "
                f"Adjusted per person budget: {adjusted_budget_per_person:.2f}. "
                f"Total group budget: {total_budget_group:.2f}.\n\n"
                f"Budget Allocation:\n"
                f"- Transport: {category_budgets['transport']}\n"
                f"- Stay: {category_budgets['stay']}\n"
                f"- Experiences: {category_budgets['experiences']}\n"
                f"- Food: {category_budgets['food']}\n"
                f"- Misc: {category_budgets['misc']}\n\n"
                "Give a clear table with daily spending limits and 3 money-saving tips."
            )
        },
        {"role": "user", "content": prompt}
    ]

    ai_response = ask_groq("gemma2-9b-it", messages)

    return ai_response, category_budgets
