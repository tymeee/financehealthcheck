from __future__ import annotations

import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from gemini_service import analyze_budget, extract_budget
from ingestion import ingest
from metrics import calculate_metrics

load_dotenv()
st.set_page_config(page_title="Private Budget Analyzer", page_icon="📊", layout="wide")
st.title("Private Budget Analyzer")
st.caption("Budget input → structured Gemini extraction → deterministic metrics → Gemini explanation")

api_key = st.secrets['api']
model= "gemini-2.5-flash

uploaded = st.file_uploader("Upload budget data", type=["csv", "xlsx", "xls", "png", "jpg", "jpeg", "webp"])
pasted = st.text_area("Or paste/type budget details", height=180, placeholder="Monthly income: 5000\nRent: 1500 ...")

if st.button("Load budget", type="primary"):
    try:
        raw_budget = ingest(uploaded, pasted)
        if not raw_budget.strip():
            raise ValueError("Enter budget text or upload a non-empty file.")
        st.session_state["budget_input"] = raw_budget
    except Exception as exc:
        st.error(f"Could not read input: {exc}")

if budget_input := st.session_state.get("budget_input"):
    st.subheader("Imported budget")
    st.text_area("Content sent to Gemini", budget_input, height=220, disabled=True)
    st.warning("This version does not remove personal information. Uploaded content may be sent to Gemini as displayed above.")
    if st.button("Analyze budget", type="primary"):
        if not api_key:
            st.error("Add a Gemini API key in Settings.")
        else:
            try:
                with st.spinner("Extracting and analyzing..."):
                    budget = extract_budget(api_key, model, budget_input)
                    metrics = calculate_metrics(budget)
                    narrative = analyze_budget(api_key, model, budget, metrics)
                st.session_state.update(budget=budget, metrics=metrics, narrative=narrative)
            except Exception as exc:
                st.error(f"Analysis failed: {exc}")

if metrics := st.session_state.get("metrics"):
    budget = st.session_state["budget"]
    st.subheader("Calculated metrics")
    cols = st.columns(4)
    cols[0].metric("Income", f"{metrics.total_income:,.2f}")
    cols[1].metric("Expenses", f"{metrics.total_expenses:,.2f}")
    cols[2].metric("Net cash flow", f"{metrics.net_cash_flow:,.2f}")
    cols[3].metric("Savings rate", "N/A" if metrics.savings_rate_pct is None else f"{metrics.savings_rate_pct:.1f}%")
    st.dataframe(pd.DataFrame([t.model_dump() for t in budget.transactions]), use_container_width=True)
    st.subheader("Analysis")
    st.markdown(st.session_state["narrative"])
    st.caption("Educational information only—not individualized financial, tax, or legal advice.")
