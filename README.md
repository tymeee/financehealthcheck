# Budget Analyzer

A Streamlit MVP implementing this budget pipeline:

1. Accept CSV/Excel, locally OCR'd images, or pasted text.
2. Show the imported content.
3. Ask Gemini for schema-constrained transaction extraction.
4. Calculate auditable metrics in Python.
5. Ask Gemini to explain the results.

## Run

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Put your Gemini API key in .env
streamlit run app.py
```

Image OCR requires the Tesseract executable installed locally and available on `PATH`. The extracted text—not the original image—is sent to Gemini.

## Privacy warning

This prototype does not screen or redact personal information. Do not upload sensitive financial data until privacy controls, encryption, retention/deletion rules, access controls, and a documented consent policy are implemented.
