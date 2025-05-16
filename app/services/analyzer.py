from collections import defaultdict


async def analyze_transactions(transactions):
    stats = {"total_spent": 0, "by_category": defaultdict(float), "daily": defaultdict(float)}

    for tx in transactions:
        if not hasattr(tx, "category") or tx.category is None:
            continue
        if tx.amount < 0:
            stats["total_spent"] += -tx.amount
            stats["by_category"][tx.category.name] += -tx.amount
            stats["daily"][tx.timestamp.date()] += -tx.amount

    days = len(stats["daily"]) or 1

    return {
        "total_spent": round(stats["total_spent"], 2),
        "by_category": {key: round(value, 2) for key, value in stats["by_category"].items()},
        "daily_average": round(stats["total_spent"] / days, 2)
    }