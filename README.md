# CodeExplain – Streamlit App

## Run on Windows CMD
1. Extract this ZIP.
2. Open CMD and move to the folder, for example:
   `cd /d D:\CodeExplain_Streamlit`
3. Create environment: `py -m venv venv`
4. Activate: `venv\Scripts\activate`
5. Install: `python -m pip install -r requirements.txt`
6. Run: `python -m streamlit run app.py`
7. Open the URL shown in CMD, normally http://localhost:8501.

You can also double-click `run_app.bat`.

## Features
- Streamlit interface
- Python AST code analysis
- Function, parameter, class, method and import extraction
- Rule-based natural-language explanations
- Approximate cyclomatic complexity
- Download documentation as Markdown

## NLP explanation
This prototype uses keyword/pattern analysis, feature extraction, Python AST parsing, and rule-based natural-language generation. It does not currently use a trained Transformer or ML model. Python is structurally supported; other languages need their own parser.
