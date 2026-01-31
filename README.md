# Forex Trading App Funnel & Conversion Analysis (Python + SQL)

This project simulates event-tracking data for a Forex trading app and analyzes the onboarding funnel using SQLite (SQL) and Python (pandas).

For a deeper discussion of funnel bottlenecks, channel quality, and product recommendations, see [Analysis.md](Analysis.md).

## Funnel Stages
visit -> sign_up -> kyc_start -> kyc_approved -> first_deposit -> first_trade -> retained_7d

## Key Results (From SQL)

- visit: 10000
- sign_up: 4539
- kyc_start: 3419
- kyc_approved: 2582
- first_deposit: 1295
- first_trade: 1029
- retained_7d: 397

### Funnel Users by Stage
![Funnel Users by Stage](reports/figures/01_funnel_users_by_stage.png)

### Step Conversion Rates
![Step Conversion Rates](reports/figures/02_step_conversion_rates.png)

### Channel Performance: First Trade vs Retention
![Channel Trade vs Retention](reports/figures/03_channel_trade_vs_retention.png)

## How to Run
1. Install Dependencies:
   ```bash
   pip install -r requirments.txt
   
2. Generate the Dataset:
   ```bash
   py src\data_generation.py
   
3. Load Data into SQLite
   ```bash
   py src\load_to_sqlite.py
   
4. Run the Analysis Notebook:
   - Open "notebooks/01_funnel_analysis.ipynb"
   - Run all cells