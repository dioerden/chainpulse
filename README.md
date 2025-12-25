# Web3 VC Data Scientist Portfolio: Protocol Health Analysis

> **Objective:** Evaluate the organic traction and economic sustainability of a GameFi/SocialFi protocol to determine investment viability for a Venture Capital firm.

![Traction Chart](assets/traction_chart.png)
*(Note: View `scripts/traction_chart.html` for interactive visualization)*

## 📂 Project Overview
This repository simulates a **Due Diligence** process performed by a Data Scientist at a top-tier Web3 VC (e.g., a16z, Dragonfly). It focuses on separating "Mercenary Capital" (farmers/bots) from "Real Users."

### Key Components
1.  **[VC Metrics Framework](docs/vc_metrics_framework.md)**: A playbook defining 5 critical on-chain metrics (Stickiness, Adjusted Retention, etc.).
2.  **[SQL Logic (Dune/Flipside)](sql/cohort_retention.sql)**: Production-ready SQL to calculate "Bot-Filtered Retention Rates."
3.  **[Investment Memo](docs/investment_memo.md)**: A professional write-up for the Investment Committee (IC) recommending a **PASS** based on the data.
4.  **[Traction Analysis (Python)](scripts/traction_analysis.py)**: Python script generating the synthetic data and visualization.

## 📊 Methodology
We define **Real Traction** using the following filter:
-   **Exclude:** Wallets with < 5 lifetime transactions.
-   **Exclude:** Wallets with < $10 entry volume (Sybil protection).
-   **Measure:** Week-over-week retention of the remaining cohorts.

## 🛠 Tech Stack
-   **SQL**: PostgreSQL / Dune V2 Engine
-   **Python**: Pandas (Data Manipulation), Plotly (Interactive Viz), Numpy (Simulation)
-   **Analysis**: Fundamental Valuation & Tokenomics

## 🚀 Quick Start
1.  Clone the repo:
    ```bash
    git clone https://github.com/dioerden/web3.git
    ```
2.  Install dependencies:
    ```bash
    pip install pandas plotly numpy
    ```
3.  Run the analysis script:
    ```bash
    python scripts/traction_analysis.py
    ```

---
*Created by [Your Name] as a Data Science Portfolio Project.*
