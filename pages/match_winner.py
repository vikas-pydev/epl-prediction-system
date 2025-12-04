"""
Match Winner Prediction Page
Predicts whether home team will win or not (Home Win vs Non-Home Win)
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
from utils.model_loader import load_model, prepare_input_dataframe, get_prediction_probability

def show():
    """Display the Match Winner prediction page."""
    # Back button handled in app.py
    
    st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>MATCHDAY PREDICTOR</h1>", unsafe_allow_html=True)
    
    # Load model
    try:
        model, features = load_model('match_winner')
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return
    
    # Layout: Left Column (Inputs) | Right Column (Visuals)
    main_col1, main_col2 = st.columns([1, 2])
    
    with main_col1:
        st.markdown("""
<div class="glass-card fadeInUp" style="padding: 1.5rem;">
<h3 style="margin-top: 0;">MATCH SETUP</h3>
<hr style="border-color: rgba(255,255,255,0.1);">
</div>
""", unsafe_allow_html=True)
        
        # Inputs wrapped in a container
        with st.container():
            st.markdown("#### Team Stats")
            home_goals_scored = st.number_input("Home Goals Scored", value=45, step=1, help="Sample Data")
            home_goals_conceded = st.number_input("Home Goals Conceded", value=67, step=1, help="Sample Data")
            away_goals_scored = st.number_input("Away Goals Scored", value=50, step=1, help="Sample Data")
            
            st.markdown("#### Form Guide")
            home_win_streak = st.slider("Home Win Streak", 0, 5, 1)
            away_win_streak = st.slider("Away Win Streak", 0, 5, 2)
            form_gap = st.number_input("Form Gap", value=-5.0, step=1.0, help="Sample Data")
            
            st.markdown("#### Differentials")
            goal_diff_gap = st.number_input("Goal Diff Gap", value=-10.0, step=0.1, help="Sample Data")
            points_gap = st.number_input("Points Gap", value=-8.0, step=0.1, help="Sample Data")
            home_goal_diff = st.number_input("Home Goal Diff", value=-22.0, step=0.1, help="Sample Data")
            away_goal_diff = st.number_input("Away Goal Diff", value=-12.0, step=0.1, help="Sample Data")

    with main_col2:
        # Versus Screen Visual
        # Versus Screen Visual
        st.markdown("""
<div class="glass-card stagger-1" style="text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; background: radial-gradient(circle, rgba(15,23,42,0.8) 0%, rgba(2,6,23,0.9) 100%); border: 1px solid rgba(255,255,255,0.1);">
<div class="versus-container">
<div style="text-align: center;">
<div class="team-logo" style="background: #ef4444; border-radius: 50%; width: 120px; height: 120px; display: flex; align-items: center; justify-content: center; font-size: 3rem;">🏠</div>
<h3 style="margin-top: 1rem;">HOME</h3>
</div>
<div class="vs-badge">VS</div>
<div style="text-align: center;">
<div class="team-logo" style="background: #3b82f6; border-radius: 50%; width: 120px; height: 120px; display: flex; align-items: center; justify-content: center; font-size: 3rem;">✈️</div>
<h3 style="margin-top: 1rem;">AWAY</h3>
</div>
</div>
<div style="margin-top: 2rem; color: #94a3b8;">
<p>Last 5 Meetings: Home 3 Wins | Draw 1 | Away 1 Win</p>
</div>
</div>
""", unsafe_allow_html=True)
        
        st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)
        
        # Analyze Button
        if st.button("ANALYZE MATCHUP", use_container_width=True):
            # Loading Animation
            progress_placeholder = st.empty()
            with progress_placeholder.container():
                st.markdown("""
<div style="text-align: center; padding: 4rem;">
<div class="pulse-glow" style="width: 100px; height: 100px; border-radius: 50%; background: var(--neon-green); margin: 0 auto; display: flex; align-items: center; justify-content: center; font-size: 3rem;">⚽</div>
<h2 style="margin-top: 2rem; color: var(--neon-green);">CONSULTING SCORESIGHT ENGINE...</h2>
<div style="width: 100%; height: 4px; background: #333; margin-top: 2rem; border-radius: 2px; overflow: hidden;">
<div class="scanline" style="width: 100%; height: 100%; background: var(--neon-green); animation: scanline 2s infinite;"></div>
</div>
</div>
""", unsafe_allow_html=True)
                time.sleep(3)  # Simulate processing
            
            progress_placeholder.empty()
            
            # Prepare input data
            input_data = {
                'Goal_Difference_Gap': goal_diff_gap,
                'Points_Gap': points_gap,
                'Away_Goal_Difference': away_goal_diff,
                'Home_Goal_Difference': home_goal_diff,
                'Form_Gap': form_gap,
                'Home_Goals_Scored': home_goals_scored,
                'Away_Win_Streak': away_win_streak,
                'Home_Goals_Conceded': home_goals_conceded,
                'Away_Goals_Scored': away_goals_scored,
                'Home_Win_Streak': home_win_streak
            }
            
            # Create DataFrame
            X = prepare_input_dataframe(input_data, features)
            
            # Make prediction
            prediction, proba = get_prediction_probability(model, X)
            
            # Display Results (Scoreboard Style)
            confidence = proba[1] if prediction == 1 else proba[0]
            winner_text = "HOME TEAM" if prediction == 1 else "NON-HOME TEAM"
            winner_color = "#39ff14" if prediction == 1 else "#ef4444"
            
            st.markdown(f"""
<div class="scoreboard fadeInUp" style="padding: 2rem; background: rgba(0,0,0,0.3); border-radius: 20px; border: 1px solid rgba(255,255,255,0.1);">
<div style="display: flex; justify-content: center; align-items: center; gap: 3rem; margin-bottom: 2rem;">
<div style="text-align: center;">
<div style="font-size: 1.5rem; color: #94a3b8; margin-bottom: 0.5rem;">HOME</div>
<div class="score-display" style="font-size: 6rem; font-weight: 800; line-height: 1; color: {winner_color if prediction == 1 else 'white'}; text-shadow: {'0 0 30px ' + winner_color if prediction == 1 else 'none'};">
{'2' if prediction == 1 else '0'}
</div>
</div>
<div style="font-size: 4rem; color: #555; font-weight: 300;">-</div>
<div style="text-align: center;">
<div style="font-size: 1.5rem; color: #94a3b8; margin-bottom: 0.5rem;">AWAY</div>
<div class="score-display" style="font-size: 6rem; font-weight: 800; line-height: 1; color: {winner_color if prediction == 0 else 'white'}; text-shadow: {'0 0 30px ' + winner_color if prediction == 0 else 'none'};">
{'1' if prediction == 1 else '1'}
</div>
</div>
</div>
<div style="text-align: center; margin-top: 1rem;">
<div style="font-size: 1.2rem; color: #94a3b8; letter-spacing: 2px;">PREDICTED WINNER</div>
<div class="pulse-glow" style="font-size: 3rem; font-weight: 800; color: {winner_color}; text-shadow: 0 0 20px {winner_color}; margin-top: 0.5rem;">
{winner_text}
</div>
</div>
</div>

<div class="glass-card stagger-1" style="border-color: #ffd700;">
<h3 style="color: #ffd700; margin-top: 0;">SCORESIGHT™ ANALYSIS</h3>
<div style="display: flex; align-items: center; gap: 2rem;">
<div style="flex: 1;">
<div style="font-size: 3rem; font-weight: 700; color: white;">{confidence*100:.0f}%</div>
<div style="color: #94a3b8;">CONFIDENCE</div>
</div>
<div style="flex: 2; text-align: left;">
<p style="color: #ccc;">
The ScoreSight engine has analyzed team form, goal differentials, and historical data.
We are <strong>{confidence*100:.0f}%</strong> confident in a <strong>{winner_text}</strong> result.
</p>
</div>
</div>
</div>
""", unsafe_allow_html=True)
