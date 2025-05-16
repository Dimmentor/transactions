CATEGORY_KEYWORDS = {
    "Food": ["restaurant", "cafe", "snackbar", "pizzeria"],
    "Transport": ["taxi", "bus", "metro", "airplane", "car-rent", "ride"],
    "Entertainment": ["cinema", "airsoft", "paintball"],
    "Utilities": ["electricity", "water", "gas"],
}


async def categorize_transaction(description: str) -> str:
    desc = description.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(word in desc for word in keywords):
            return category
    return "Other"
