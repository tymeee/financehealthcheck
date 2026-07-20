from __future__ import annotations

import json

from google import genai
from google.genai import types

from models import ExtractedBudget, FinancialMetrics


def extract_budget(api_key: str, model: str, budget_text: str) -> ExtractedBudget:
    prompt = (
        "Extract budgeting transactions from the sanitized input. Amounts must be positive magnitudes; "
        "classify each as income or expense, choose a useful category, and mark recurring only when supported. "
        "Note ambiguities and do not invent missing transactions.\n\nINPUT:\n" + budget_text
    )
    with genai.Client(api_key=api_key) as client:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0,
                response_mime_type="application/json",
                response_schema=ExtractedBudget,
            ),
        )
    if response.parsed:
        return ExtractedBudget.model_validate(response.parsed)
    return ExtractedBudget.model_validate_json(response.text)


def analyze_budget(api_key: str, model: str, budget: ExtractedBudget, metrics: FinancialMetrics) -> str:
    payload = {"budget": budget.model_dump(mode="json"), "calculated_metrics": metrics.model_dump()}
    prompt = (
        "Analyze this budget using only the supplied data and calculated metrics. Explain the current "
        "position, identify 3 prioritized actions, and state uncertainties. Never claim certainty, provide tax/legal "
        "advice, or invent missing data. Keep it practical and concise.\n\n" 
        """
        Write the financial analysis in clean Markdown.
        
        Formatting rules:
        - Never use LaTeX or mathematical notation.
        - Never use the $ currency symbol.
        - Write currency as "USD 2,089.00" or "THB 2,089.00".
        - Put a space between numbers and surrounding words.
        - Use Markdown bold only for headings and important values.
        - Do not place Markdown formatting inside currency values.
        """+ json.dumps(payload)
    )
    with genai.Client(api_key=api_key) as client:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.2),
        )
    return response.text or "No analysis was returned."
