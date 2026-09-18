# Two-pass rule evaluation: aggregate per-trip totals, then apply composable per-expense and per-trip rules in policy order.
from typing import List, Optional, Any


def evaluateExpenseRules(expenses: List[List[str]]) -> List[List[str]]:
    RESTAURANT_CAP = 75
    EXPENSE_CAP = 250
    TRIP_CAP = 2000
    MEAL_CAP = 200

    trip_total = {}
    trip_meal = {}
    amounts = []
    for row in expenses:
        trip_id = row[1]
        amount = int(row[2])
        expense_type = row[3]
        amounts.append(amount)
        trip_total[trip_id] = trip_total.get(trip_id, 0) + amount
        if expense_type == "MEAL":
            trip_meal[trip_id] = trip_meal.get(trip_id, 0) + amount

    result = []
    for i, row in enumerate(expenses):
        expense_id = row[0]
        trip_id = row[1]
        amount = amounts[i]
        expense_type = row[3]
        vendor_type = row[4]

        out = [expense_id]
        if vendor_type == "RESTAURANT" and amount > RESTAURANT_CAP:
            out.append("RESTAURANT_LIMIT")
        if expense_type == "AIRFARE":
            out.append("NO_AIRFARE")
        if expense_type == "ENTERTAINMENT":
            out.append("NO_ENTERTAINMENT")
        if amount > EXPENSE_CAP:
            out.append("EXPENSE_LIMIT")
        if trip_total.get(trip_id, 0) > TRIP_CAP:
            out.append("TRIP_LIMIT")
        if trip_meal.get(trip_id, 0) > MEAL_CAP:
            out.append("MEAL_LIMIT")
        result.append(out)
    return result
