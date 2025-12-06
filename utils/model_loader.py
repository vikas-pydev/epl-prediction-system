"""
Utility functions for loading models and preprocessing data.
Supports both legacy .pkl files and new .joblib files.
"""

import joblib
import json
import pandas as pd
import numpy as np
from pathlib import Path

MODELS_DIR = Path("models")
JOBLIB_DIR = Path("joblib files")

# Model mapping: model_name -> joblib filename
# Using best performing models for each prediction type
JOBLIB_MODELS = {
    'match_winner': 'match_winner_GradientBoosting.joblib',  # Better predictions than NeuralNetwork
    'league_winner': 'ps1_league_winner_best_model.joblib',  # RandomForest - 95% accuracy
    'total_points': 'ps3_total_points_XGBoost.joblib',
    'goals': 'ps3_top_scorer_goals_model.joblib',
    'assists': 'ps3_top_scorer_assists_model.joblib'
}

# Metadata files for each model
METADATA_FILES = {
    'match_winner': 'ps4_match_winner_metadata.json',
    'league_winner': 'ps1_league_winner_metadata.json',
    'total_points': 'ps3_total_points_metadata.json',
    'goals': 'ps3_top_scorer_goals_metadata.json',
    'assists': 'ps3_top_scorer_assists_metadata.json'
}

# Feature lists for models (some metadata files don't have features)
FEATURE_LISTS = {
    'match_winner': [
        'Points_Gap', 'Goal_Difference_Gap', 'Form_Gap',
        'Home_Goal_Difference', 'Away_Goal_Difference',
        'Home_Win_Streak', 'Away_Win_Streak',
        'Home_Goals_Scored', 'Away_Goals_Scored', 'Home_Goals_Conceded'
    ],
    'league_winner': [
        'wins', 'draws', 'losses', 'points_per_game', 'goals_scored', 'goals_conceded'
    ],
    'total_points': [
        'season_end_year', 'played', 'gf', 'ga', 'gd'
    ],
    # Goals and assists use the same 16 features
    'goals': [
        'position', 'age', 'matches_played', 'starts', 'minutes',
        'goals_per_90', 'assists_per_90', 'xg_per_90', 'npxg_per_90', 'xag_per_90',
        'npxg_plus_xag_per_90', 'non_penalty_goals_per_90', 'goals_per_xg',
        'assists_per_xag', 'xag_impact', 'npxg_impact'
    ],
    'assists': [
        'position', 'age', 'matches_played', 'starts', 'minutes',
        'goals_per_90', 'assists_per_90', 'xg_per_90', 'npxg_per_90', 'xag_per_90',
        'npxg_plus_xag_per_90', 'non_penalty_goals_per_90', 'goals_per_xg',
        'assists_per_xag', 'xag_impact', 'npxg_impact'
    ]
}


def load_model(model_name):
    """Load a trained model from the joblib files directory."""
    # Use new joblib files
    if model_name in JOBLIB_MODELS:
        model_path = JOBLIB_DIR / JOBLIB_MODELS[model_name]
        model = joblib.load(model_path)
        
        # Get features from predefined list or try to load from metadata
        features = FEATURE_LISTS.get(model_name)
        
        if features is None:
            # Try to load from metadata
            metadata_file = METADATA_FILES.get(model_name)
            if metadata_file:
                try:
                    metadata_path = JOBLIB_DIR / metadata_file
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                    features = metadata.get('features_used', [])
                except Exception:
                    features = []
        
        return model, features
    
    # Fallback to old pkl models
    model_path = MODELS_DIR / f"{model_name}_model.pkl"
    features_path = MODELS_DIR / f"{model_name}_features.pkl"
    
    model = joblib.load(model_path)
    features = joblib.load(features_path)
    
    return model, features


def load_metadata(model_name):
    """Load metadata for a model."""
    metadata_file = METADATA_FILES.get(model_name)
    if not metadata_file:
        return {}
    
    metadata_path = JOBLIB_DIR / metadata_file
    try:
        with open(metadata_path, 'r') as f:
            return json.load(f)
    except Exception:
        return {}


def validate_input(data_dict, required_features):
    """Validate that all required features are present and numeric."""
    missing_features = []
    
    if isinstance(required_features, dict):
        # For goals/assists models with categorical and numeric features
        all_features = required_features['categorical'] + required_features['numeric']
    else:
        # For other models with simple list of features
        all_features = required_features
    
    for feature in all_features:
        if feature not in data_dict:
            missing_features.append(feature)
    
    if missing_features:
        raise ValueError(f"Missing features: {', '.join(missing_features)}")
    
    return True


def prepare_input_dataframe(data_dict, features):
    """
    Convert input dictionary to DataFrame with correct feature order.
    
    Args:
        data_dict: Dictionary of feature name -> value
        features: List of feature names or dict with 'categorical' and 'numeric' keys
    
    Returns:
        DataFrame with single row and correct feature order
    """
    if isinstance(features, dict):
        # Goals/Assists models - combine categorical and numeric
        feature_order = features['categorical'] + features['numeric']
    else:
        # Other models - simple list
        feature_order = features
    
    # Create DataFrame with correct column order
    df = pd.DataFrame([data_dict], columns=feature_order)
    
    return df


def get_prediction_probability(model, X):
    """Get prediction and probability scores."""
    prediction = model.predict(X)[0]
    
    # Try to get probability if classifier
    try:
        proba = model.predict_proba(X)[0]
        return prediction, proba
    except AttributeError:
        # Regressor doesn't have predict_proba
        return prediction, None
