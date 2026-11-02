# Insurance Analytics Dashboard

An interactive Python dashboard for exploring insurance policy performance, claims trends, risk indicators and unusual claim patterns.

## Dashboard features

- KPI cards: policies, reported claims, claim frequency and incurred loss ratio
- Policy distribution by insurance type
- Claim amount share by region
- Monthly claims trend
- Rule-based unusual-claim review table
- Filters for insurance type and region
- Upload your own CSV and download filtered records

## Tech stack

Python · Streamlit · Pandas · NumPy · Plotly

## Run locally

1. Install Python 3.10 or newer.
2. Open this project folder in VS Code or a terminal.
3. Create and activate a virtual environment (recommended).
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

6. Open the local URL shown in the terminal (usually `http://localhost:8501`).

## Dataset

`data/insurance_data.csv` is a synthetic sample dataset created for this project. It contains policy IDs, policy dates, insurance type, region, customer age, annual premium, claim indicator, claim amount and days to claim.

You can upload a CSV with the same column names from the dashboard sidebar.

## GitHub upload

1. Create a new GitHub repository, for example `insurance-analytics-dashboard`.
2. Extract this ZIP file.
3. Upload the **contents** of the extracted folder (not the ZIP itself) to the repository.
4. Commit the files.
5. Add the repository URL to your resume or portfolio.

## Important note

The unusual-claim review uses transparent example rules (top 5% claim amount or claim reported within 3 days). These flags are for learning and prioritization only; they do not prove fraud. Real insurance decisions require validated models, suitable data, privacy controls, bias testing and human review. The included dataset is synthetic and must not be treated as real customer or insurer data.
