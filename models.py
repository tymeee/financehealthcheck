from __future__ import annotations

from datetime import date as Date
from typing import Literal

from pydantic import BaseModel, Field


class Transaction(BaseModel):
    date: Date | None = None
    description: str = "Unspecified"
    amount: float = Field(description="Positive magnitude")
    kind: Literal["income", "expense"]
    category: str = "Other"
    recurring: bool = False


class ExtractedBudget(BaseModel):
    currency: str = "USD"
    period: str = "monthly"
    transactions: list[Transaction]
    extraction_notes: list[str] = Field(default_factory=list)


class FinancialMetrics(BaseModel):
    total_income: float
    total_expenses: float
    net_cash_flow: float
    savings_rate_pct: float | None
    expense_ratio_pct: float | None
    fixed_expense_pct: float | None
    top_expense_category: str | None
    top_expense_category_amount: float
    runway_months: float | None = None
