from __future__ import annotations

import io

import pandas as pd
import pytesseract
from PIL import Image

def ingest(uploaded_file=None, pasted_text: str = "") -> str:
    if uploaded_file is None:
        return pasted_text
    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(uploaded_file).to_csv(index=False)
    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(uploaded_file).to_csv(index=False)
    if name.endswith((".png", ".jpg", ".jpeg", ".webp")):
        image = Image.open(io.BytesIO(uploaded_file.getvalue()))
        return pytesseract.image_to_string(image)
    raise ValueError("Supported formats: CSV, Excel, PNG, JPG, JPEG, and WebP.")
