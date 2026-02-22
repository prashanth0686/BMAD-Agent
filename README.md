# 🧙 BMAD Sentinel: Autonomous PM Peer Reviewer

BMAD Sentinel is an agentic workflow designed for Product Managers. While most AI tools focus on *writing* documentation, **BMAD Sentinel** is built to *critique and improve* it. It acts as an Automated Peer Reviewer, scanning for logic gaps, technical debt, and edge cases before requirements ever reach a developer.

---

## 🚀 How to Run Locally

### 1. Prerequisites
- Python 3.9 or higher installed.
- A Google Gemini API Key.
- Your project files organized in the following structure:
  - `app.py`
  - `core/config.yaml`
  - `core/agents/bmad-master.md`
  - `.env` (containing `GEMINI_API_KEY=your_key_here`)

### 2. Launch the WebApp
Open your terminal in the project root and run:
```bash
python -m streamlit run app.py
