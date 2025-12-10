"""
Retrain Goals and Assists models for sklearn 1.6+ compatibility.
Run this script locally, then commit and push the new model files.
"""

import numpy as np
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

# Set random state for reproducibility
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# Output directory
JOBLIB_DIR = 'joblib files'

print("="*60)
print("RETRAINING GOALS & ASSISTS MODELS FOR SKLEARN 1.6+")
print("="*60)

# Load data
print("\nLoading data...")
df_goals = pd.read_excel("Data/Goals & Assist.xlsx")
print(f"  Loaded {len(df_goals)} records")

# Clean data
df_clean = df_goals.copy()

# Rename columns to match what the app expects (lowercase with underscores)
column_mapping = {
    'Position': 'position',
    'Age': 'age',
    'Matches Played': 'matches_played',
    'Starts': 'starts',
    'Minutes': 'minutes',
    'Goals Per 90': 'goals_per_90',
    'Assists Per 90': 'assists_per_90',
    'xG Per 90': 'xg_per_90',
    'npxG Per 90': 'npxg_per_90',
    'xAG Per 90': 'xag_per_90',
    'npxG + xAG Per 90': 'npxg_plus_xag_per_90',
    'Non-Penalty Goals Per 90': 'non_penalty_goals_per_90',
    'Goals': 'Goals',
    'Assists': 'Assists'
}

# Check which columns exist and rename them
for old_name, new_name in column_mapping.items():
    if old_name in df_clean.columns:
        df_clean = df_clean.rename(columns={old_name: new_name})

print(f"  Available columns: {list(df_clean.columns)}")

# Define features - these match what the app sends
categorical_features = ['position']

# The 16 features the app uses (from model_loader.py)
numeric_features = [
    'age', 'matches_played', 'starts', 'minutes',
    'goals_per_90', 'assists_per_90', 'xg_per_90', 'npxg_per_90', 'xag_per_90',
    'npxg_plus_xag_per_90', 'non_penalty_goals_per_90'
]

# Add derived features that the app calculates
# These will be computed during prediction, so we need to add them to training data
df_clean['goals_per_xg'] = df_clean['goals_per_90'] / df_clean['xg_per_90'].replace(0, 0.001)
df_clean['assists_per_xag'] = df_clean['assists_per_90'] / df_clean['xag_per_90'].replace(0, 0.001)
df_clean['xag_impact'] = df_clean['xag_per_90'] - df_clean['assists_per_90']
df_clean['npxg_impact'] = df_clean['npxg_per_90'] - df_clean['non_penalty_goals_per_90']

# Clean up infinite values
df_clean = df_clean.replace([np.inf, -np.inf], np.nan)

# Add derived features to the list
numeric_features_full = numeric_features + ['goals_per_xg', 'assists_per_xag', 'xag_impact', 'npxg_impact']

all_features = categorical_features + numeric_features_full

print(f"  Using features: {all_features}")

# ============================================================================
# GOALS MODEL
# ============================================================================
print("\n[1/2] Training Goals Prediction Model...")

# Prepare data for Goals
df_target = df_clean.dropna(subset=["Goals"]).copy()

# Check which features are available
available_features = [f for f in all_features if f in df_target.columns]
print(f"  Available features for training: {available_features}")

X = df_target[available_features]
y = df_target["Goals"].astype(float)

print(f"  Training samples: {len(X)}")

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE
)

# Create preprocessor
cat_features_available = [f for f in categorical_features if f in X.columns]
num_features_available = [f for f in numeric_features_full if f in X.columns]

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
        ("num", num_transformer, num_features_available),
        ("cat", cat_transformer, cat_features_available),
    ],
    remainder="drop"
)

# Train model using GradientBoosting for better predictions
goals_model = Pipeline([
    ("pre", preprocessor),
    ("reg", GradientBoostingRegressor(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=RANDOM_STATE
    ))
])
goals_model.fit(X_train, y_train)

# Evaluate
r2 = goals_model.score(X_test, y_test)
print(f"  ✓ Goals Model R²: {r2:.3f}")

# Save model
goals_model_path = os.path.join(JOBLIB_DIR, 'ps3_top_scorer_goals_model.joblib')
joblib.dump(goals_model, goals_model_path)
print(f"  ✓ Saved: {goals_model_path}")

# ============================================================================
# ASSISTS MODEL
# ============================================================================
print("\n[2/2] Training Assists Prediction Model...")

# Prepare data for Assists
df_target = df_clean.dropna(subset=["Assists"]).copy()
X = df_target[available_features]
y = df_target["Assists"].astype(float)

print(f"  Training samples: {len(X)}")

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE
)

# Train model
assists_model = Pipeline([
    ("pre", preprocessor),
    ("reg", GradientBoostingRegressor(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=RANDOM_STATE
    ))
])
assists_model.fit(X_train, y_train)

# Evaluate
r2 = assists_model.score(X_test, y_test)
print(f"  ✓ Assists Model R²: {r2:.3f}")

# Save model
assists_model_path = os.path.join(JOBLIB_DIR, 'ps3_top_scorer_assists_model.joblib')
joblib.dump(assists_model, assists_model_path)
print(f"  ✓ Saved: {assists_model_path}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*60)
print("✓ MODELS RETRAINED SUCCESSFULLY!")
print("="*60)
print("\nNext steps:")
print("  1. git add 'joblib files/ps3_top_scorer_goals_model.joblib'")
print("  2. git add 'joblib files/ps3_top_scorer_assists_model.joblib'")
print("  3. git commit -m 'Retrain goals/assists models for sklearn 1.6+'")
print("  4. git push")
