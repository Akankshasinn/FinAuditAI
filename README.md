# finAuditAI

A beginner-friendly financial audit automation MVP using FastAPI, MySQL and Python.

## Features in this starter
- MySQL-backed transaction storage
- CSV transaction upload
- Transaction listing API
- Basic rule-based flags for repeated payment references and high-value transactions
- Audit results API
- Interactive API documentation at `/docs`

## Setup (Windows PowerShell)
1. Install Python, MySQL Server and VS Code.
2. Create a MySQL database by running `database/schema.sql` in MySQL Workbench.
3. Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
5. Copy `.env.example` to `.env` and replace `YOUR_MYSQL_PASSWORD` with your local MySQL password.
6. Start the API:
   ```powershell
   uvicorn app:app --reload
   ```
7. Open `http://127.0.0.1:8000/docs`.
8. Upload `data/sample_transactions.csv` using `POST /transactions/upload`, run `POST /audit/run`, then view `GET /audit/results`.

## Required CSV columns
`transaction_date`, `vendor_name`, `amount`, `payment_reference`; optional: `category`.

## Important
This is an educational prototype. Its rules and thresholds are illustrative, not professional fraud-detection advice. A flagged transaction requires human review. Do not upload real personal or confidential financial data to this demo.
