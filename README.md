# ⚽ EPL Prediction System

A machine learning-powered application to predict English Premier League outcomes, including match winners, league champions, player goals, and assists.

## 🚀 How to Run

### 1. Prerequisites
Ensure you have **Python** installed on your system.

### 2. Install Dependencies
Open your terminal (Command Prompt or PowerShell) in the project folder and run:
```bash
pip install -r requirements.txt
```

### 3. Start the Application
Run the following command to launch the app:
```bash
python -m streamlit run app.py
```
*The application should automatically open in your default web browser at `http://localhost:8501`.*

---

## 📊 Features

- **Match Winner**: Predict the outcome of a specific match (Home Win vs. Non-Home Win).
- **League Winner**: Predict if a team has the stats to be a Champion.
- **Total Points**: Estimate a team's total season points based on goal stats.
- **Goals Prediction**: Predict a player's expected goal tally.
- **Assists Prediction**: Predict a player's expected assist tally.

## 🛠️ Troubleshooting

- **"Streamlit is not recognized"**: Ensure you installed the requirements and use `python -m streamlit run app.py` instead of just `streamlit run`.
- **Changes not showing?**: If you edit code, refresh the browser page. If that fails, stop the server (Ctrl+C) and run the start command again.
