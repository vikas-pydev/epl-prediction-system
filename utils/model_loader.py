"""
Utility functions for loading models and preprocessing data.
"""

import joblib
import pandas as pd
import numpy as np
from pathlib import Path

MODELS_DIR = Path("models")

def load_model(model_name):
    """Load a trained model from the models directory."""
    model_path = MODELS_DIR / f"{model_name}_model.pkl"
    features_path = MODELS_DIR / f"{model_name}_features.pkl"
    
    model = joblib.load(model_path)
    features = joblib.load(features_path)
    
    return model, features

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
