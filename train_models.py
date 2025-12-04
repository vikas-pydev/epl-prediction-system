"""
Train and save all EPL prediction models.

This script extracts model training code from the Jupyter notebooks and
saves trained models as pickle files for use in the Streamlit application.
"""

import numpy as np
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

# Set random state for reproducibility
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# Create models directory if it doesn't exist
os.makedirs('models', exist_ok=True)

print("="*60)
print("EPL PREDICTION MODELS TRAINING")
print("="*60)

# ============================================================================
# 1. MATCH WINNER MODEL
# ============================================================================
print("\n[1/5] Training Match Winner Model...")

# Load data
df_match = pd.read_csv("Data/Match Winner.csv")

# Drop unnecessary columns
drop_cols = ['Unnamed: 0', 'Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']
drop_cols = [c for c in drop_cols if c in df_match.columns]
df_match = df_match.drop(columns=drop_cols)

# Engineer features
data = df_match.copy()
data['Goal_Difference_Gap'] = data['HTGD'] - data['ATGD']
data['Points_Gap'] = data['HTP'] - data['ATP']
data['Away_Goal_Difference'] = data['ATGD']
data['Home_Goal_Difference'] = data['HTGD']
data['Form_Gap'] = data['HTFormPts'] - data['ATFormPts']
data['Home_Goals_Scored'] = data['HTGS']
data['Away_Win_Streak'] = data['ATWinStreak5']
data['Home_Goals_Conceded'] = data['HTGC']
data['Away_Goals_Scored'] = data['ATGS']
data['Home_Win_Streak'] = data['HTWinStreak5']

feature_cols = [
    'Goal_Difference_Gap',
    'Points_Gap',
    'Away_Goal_Difference',
    'Home_Goal_Difference',
    'Form_Gap',
    'Home_Goals_Scored',
    'Away_Win_Streak',
    'Home_Goals_Conceded',
    'Away_Goals_Scored',
    'Home_Win_Streak'
]

# Prepare features and target
X = data[feature_cols].copy()
y = data['FTR'].map({'H': 1, 'NH': 0})

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
)

# Train model
match_winner_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=5,
    min_samples_split=10,
    min_samples_leaf=1,
    max_features='sqrt',
    random_state=RANDOM_STATE,
    n_jobs=-1
)
match_winner_model.fit(X_train, y_train)

# Evaluate
accuracy = match_winner_model.score(X_test, y_test)
print(f"  ✓ Match Winner Model Accuracy: {accuracy:.3f}")

# Save model and features
joblib.dump(match_winner_model, 'models/match_winner_model.pkl')
joblib.dump(feature_cols, 'models/match_winner_features.pkl')
print("  ✓ Saved: models/match_winner_model.pkl")

# ============================================================================
# 2. LEAGUE WINNER (CHAMPION) MODEL
# ============================================================================
print("\n[2/5] Training League Winner Model...")

# Load data
df_league = pd.read_csv("Data/ScoreSight_ML_Season_LeagueWinner_Champion.csv")

# Prepare features
drop_cols = [
    "team", "season", "matches_played",
    "target_total_points", "target_league_position",
    "target_top_4", "target_top_6", "target_relegated"
]
X = df_league.drop(columns=drop_cols, errors="ignore")
y = X["target_champion"]
X = X.drop(columns=["target_champion"])

champion_features = list(X.columns)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
)

# Train model
league_winner_model = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        solver="lbfgs",
        random_state=RANDOM_STATE
    ))
])
league_winner_model.fit(X_train, y_train)

# Evaluate
accuracy = league_winner_model.score(X_test, y_test)
print(f"  ✓ League Winner Model Accuracy: {accuracy:.3f}")

# Save model and features
joblib.dump(league_winner_model, 'models/league_winner_model.pkl')
joblib.dump(champion_features, 'models/league_winner_features.pkl')
print("  ✓ Saved: models/league_winner_model.pkl")

# ============================================================================
# 3. TOTAL POINTS MODEL (using same features as champion)
# ============================================================================
print("\n[3/5] Training Total Points Model...")

# Prepare features and target
data_league = df_league.copy()
# Use only requested features
features_for_points = ["goals_scored", "goals_conceded", "goal_difference"]
X = data_league[features_for_points]
y = data_league["target_total_points"]

# Update feature list for saving
champion_features = features_for_points

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE
)

# Train model
total_points_model = Pipeline([
    ("scaler", StandardScaler()),
    ("reg", Ridge(alpha=1.0, random_state=RANDOM_STATE))
])
total_points_model.fit(X_train, y_train)

# Evaluate
r2 = total_points_model.score(X_test, y_test)
print(f"  ✓ Total Points Model R²: {r2:.3f}")

# Save model and features
joblib.dump(total_points_model, 'models/total_points_model.pkl')
joblib.dump(champion_features, 'models/total_points_features.pkl')
print("  ✓ Saved: models/total_points_model.pkl")

# ============================================================================
# 4. GOALS PREDICTION MODEL
# ============================================================================
print("\n[4/5] Training Goals Prediction Model...")

# Load data
df_goals = pd.read_excel("Data/Goals & Assist.xlsx")

# Clean data
df_clean = df_goals.copy()
drop_cols = [
    "Unnamed: 0", "Player", "Nation",
    "Goals + Assists", "Goals + Assists Per 90",
    "Non-Penalty Goals + Assists Per 90",
    "xG + xAG Per 90", "npxG + xAG Per 90"
]
drop_cols = [c for c in drop_cols if c in df_clean.columns]
df_clean = df_clean.drop(columns=drop_cols)

# Define features
categorical_features = ['Position']
all_numeric = df_clean.select_dtypes(include="number").columns.tolist()
leak_like_cols = [
    "Goals", "Assists", "Goals Per 90", "Assists Per 90",
    "Goals + Assists Per 90", "Non-Penalty Goals Per 90",
    "Non-Penalty Goals + Assists Per 90", "Non-Penalty Goals"
]
numeric_features = [c for c in all_numeric if c not in leak_like_cols]

# Prepare data for Goals
df_target = df_clean.dropna(subset=["Goals"]).copy()
X = df_target[categorical_features + numeric_features]
y = df_target["Goals"].astype(float)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE
)

# Create preprocessor
num_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])
cat_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])
preprocessor = ColumnTransformer(
    transformers=[
        ("num", num_transformer, numeric_features),
        ("cat", cat_transformer, categorical_features),
    ],
    remainder="drop"
)

# Train model
goals_model = Pipeline([
    ("pre", preprocessor),
    ("reg", Ridge(alpha=1.0, random_state=RANDOM_STATE))
])
goals_model.fit(X_train, y_train)

# Evaluate
r2 = goals_model.score(X_test, y_test)
print(f"  ✓ Goals Model R²: {r2:.3f}")

# Save model and features
joblib.dump(goals_model, 'models/goals_model.pkl')
joblib.dump({
    'categorical': categorical_features,
    'numeric': numeric_features
}, 'models/goals_features.pkl')
print("  ✓ Saved: models/goals_model.pkl")

# ============================================================================
# 5. ASSISTS PREDICTION MODEL
# ============================================================================
print("\n[5/5] Training Assists Prediction Model...")

# Prepare data for Assists
df_target = df_clean.dropna(subset=["Assists"]).copy()
X = df_target[categorical_features + numeric_features]
y = df_target["Assists"].astype(float)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE
)

# Train model (same preprocessor as goals)
assists_model = Pipeline([
    ("pre", preprocessor),
    ("reg", Ridge(alpha=1.0, random_state=RANDOM_STATE))
])
assists_model.fit(X_train, y_train)

# Evaluate
r2 = assists_model.score(X_test, y_test)
print(f"  ✓ Assists Model R²: {r2:.3f}")

# Save model and features
joblib.dump(assists_model, 'models/assists_model.pkl')
joblib.dump({
    'categorical': categorical_features,
    'numeric': numeric_features
}, 'models/assists_features.pkl')
print("  ✓ Saved: models/assists_model.pkl")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*60)
print("✓ ALL MODELS TRAINED AND SAVED SUCCESSFULLY!")
print("="*60)
print("\nSaved models:")
print("  1. models/match_winner_model.pkl")
print("  2. models/league_winner_model.pkl")
print("  3. models/total_points_model.pkl")
print("  4. models/goals_model.pkl")
print("  5. models/assists_model.pkl")
print("\nYou can now run the Streamlit app: streamlit run app.py")
