from __future__ import annotations

from collections import defaultdict

from models import ExtractedBudget, FinancialMetrics


def calculate_metrics(budget: ExtractedBudget| None  = None) -> FinancialMetrics:
    income = sum(t.amount for t in budget.transactions if t.kind == "income")
    expenses = sum(t.amount for t in budget.transactions if t.kind == "expense")
    fixed = sum(t.amount for t in budget.transactions if t.kind == "expense" and t.recurring)
    categories: dict[str, float] = defaultdict(float)
    for item in budget.transactions:
        if item.kind == "expense":
            categories[item.category] += item.amount
    top = max(categories, key=categories.get) if categories else None
    return FinancialMetrics(
        total_income=round(income, 2),
        total_expenses=round(expenses, 2),
        net_cash_flow=round(income - expenses, 2),
        savings_rate_pct=round((income - expenses) / income * 100, 2) if income else None,
        expense_ratio_pct=round(expenses / income * 100, 2) if income else None,
        fixed_expense_pct=round(fixed / expenses * 100, 2) if expenses else None,
        top_expense_category=top,
        top_expense_category_amount=round(categories.get(top, 0), 2) if top else 0,
    )

