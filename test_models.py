import joblib
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

print("=== Testing Total Points Models ===")
for model in ['ps3_total_points_XGBoost.joblib', 'ps3_total_points_RandomForest.joblib', 'ps3_total_points_Ridge.joblib', 'ps3_total_points_best_model.joblib']:
    try:
        m = joblib.load(f'joblib files/{model}')
        X = pd.DataFrame([[2024, 20, 35, 25, 10]], columns=['season_end_year', 'played', 'gf', 'ga', 'gd'])
        pred = m.predict(X)[0]
        print(f'{model}: {pred:.1f} points')
    except Exception as e:
        print(f'{model}: Error - {e}')

print("\n=== Testing Match Winner Models ===")
for model in ['match_winner_GradientBoosting.joblib', 'match_winner_RandomForest.joblib', 'match_winner_XGBoost.joblib', 'match_winner_CalibratedStacking.joblib']:
    try:
        m = joblib.load(f'joblib files/{model}')
        X = pd.DataFrame([[32.0, 5.0, 4.0, 15.0, 0.0, 4, 0, 20, 5, 2]], columns=['Points_Gap', 'Goal_Difference_Gap', 'Form_Gap', 'Home_Goal_Difference', 'Away_Goal_Difference', 'Home_Win_Streak', 'Away_Win_Streak', 'Home_Goals_Scored', 'Away_Goals_Scored', 'Home_Goals_Conceded'])
        pred = m.predict(X)[0]
        proba = m.predict_proba(X)[0]
        home_win = proba[1] * 100 if len(proba) > 1 else 0
        print(f'{model}: Pred={pred}, Home Win={home_win:.1f}%')
    except Exception as e:
        print(f'{model}: Error - {e}')

print("\n=== Testing League Winner Models ===")
for model in ['ps1_league_winner_best_model.joblib', 'league_winner_RandomForest.joblib']:
    try:
        m = joblib.load(f'joblib files/{model}')
        features = m.feature_names_in_ if hasattr(m, 'feature_names_in_') else ['wins', 'draws', 'losses', 'points_per_game', 'goals_scored', 'goals_conceded']
        print(f'{model}: Features = {list(features)}')
    except Exception as e:
        print(f'{model}: Error - {e}')

print("\n=== Testing Goals/Assists Models ===")
for model in ['ps3_top_scorer_goals_model.joblib', 'ps3_top_scorer_assists_model.joblib']:
    try:
        m = joblib.load(f'joblib files/{model}')
        features = m.feature_names_in_ if hasattr(m, 'feature_names_in_') else 'Unknown'
        print(f'{model}: {len(features)} features')
    except Exception as e:
        print(f'{model}: Error - {e}')
