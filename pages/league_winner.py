"""
League Winner (Champion) Prediction Page
Predicts whether a team will win the league championship
"""

import streamlit as st
import pandas as pd
import numpy as np
from utils.model_loader import load_model, prepare_input_dataframe, get_prediction_probability

def show():
    """Display the League Winner prediction page."""
    st.markdown("<h1>👑 League Winner Prediction</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color: white; font-size: 1.1rem; margin-bottom: 2rem;'>"
        "Predict whether a team will become Premier League champion</p>",
        unsafe_allow_html=True
    )
    
    # Load model
    try:
        model, features = load_model('league_winner')
        st.success("✅ Model loaded successfully!")
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return
    
    # Display feature input form
    st.markdown("<h2 style='color: white;'>Enter Team Season Statistics</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Match Results")
        wins = st.number_input("Wins", value=28, min_value=0, max_value=38, step=1, help="Sample: Man City 23/24")
        draws = st.number_input("Draws", value=7, min_value=0, max_value=38, step=1, help="Sample: Man City 23/24")
        losses = st.number_input("Losses", value=3, min_value=0, max_value=38, step=1, help="Sample: Man City 23/24")
        points_per_game = st.number_input("Points Per Game", value=2.39, min_value=0.0, max_value=3.0, step=0.01, help="Sample: Man City 23/24")
    
    with col2:
        st.markdown("#### Goal Statistics")
        goals_scored = st.number_input("Goals Scored", value=96.0, min_value=0.0, step=1.0, help="Sample: Man City 23/24")
        goals_conceded = st.number_input("Goals Conceded", value=34.0, min_value=0.0, step=1.0, help="Sample: Man City 23/24")
        goal_difference = st.number_input("Goal Difference", value=62.0, step=1.0, help="Sample: Man City 23/24")
    
    # Info box
    st.info("💡 **Tip**: Champion teams typically have 25+ wins, 85+ points (2.2+ PPG), and positive goal difference of 30+")
    
    # Predict button
    if st.button("🔮 Predict Championship Chances", use_container_width=True):
        # Prepare input data
        input_data = {
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'points_per_game': points_per_game,
            'goals_scored': goals_scored,
            'goals_conceded': goals_conceded,
            'goal_difference': goal_difference
        }
        
        # Create DataFrame
        X = prepare_input_dataframe(input_data, features)
        
        # Make prediction
        prediction, proba = get_prediction_probability(model, X)
        
        # Display results
        st.markdown("---")
        st.markdown("<h2 style='color: white;'>Prediction Results</h2>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if prediction == 1:
                st.markdown(
                    f"<div class='result-card' style='text-align: center; padding: 2rem; background: rgba(255,255,255,0.05); border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);'>"
                    f"<div class='result-title' style='color: #94a3b8; font-size: 1.2rem; margin-bottom: 1rem;'>CHAMPIONSHIP PREDICTION</div>"
                    f"<div class='result-value' style='color: #f59e0b; font-size: 4rem; font-weight: 800; text-shadow: 0 0 20px #f59e0b; line-height: 1.2;'>👑 CHAMPION</div>"
                    f"<div class='result-subtitle' style='color: white; font-size: 1.5rem; margin-top: 1rem;'>Probability: <span style='color: #f59e0b;'>{proba[1]*100:.1f}%</span></div>"
                    "</div>",
                    unsafe_allow_html=True
                )
                st.balloons()
            else:
                st.markdown(
                    f"<div class='result-card' style='text-align: center; padding: 2rem; background: rgba(255,255,255,0.05); border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);'>"
                    f"<div class='result-title' style='color: #94a3b8; font-size: 1.2rem; margin-bottom: 1rem;'>CHAMPIONSHIP PREDICTION</div>"
                    f"<div class='result-value' style='color: #9ca3af; font-size: 4rem; font-weight: 800; line-height: 1.2;'>❌ NOT CHAMPION</div>"
                    f"<div class='result-subtitle' style='color: white; font-size: 1.5rem; margin-top: 1rem;'>Probability: <span style='color: #f59e0b;'>{proba[1]*100:.1f}%</span></div>"
                    "</div>",
                    unsafe_allow_html=True
                )
        
        # Show probabilities
        st.markdown("### Probability Breakdown")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Champion Probability", f"{proba[1]*100:.1f}%", 
                     delta="High Chance" if proba[1] > 0.5 else "Low Chance")
        with col2:
            st.metric("Non-Champion Probability", f"{proba[0]*100:.1f}%")
        
        # Estimated total points
        estimated_points = wins * 3 + draws
        st.markdown("### Performance Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Estimated Total Points", f"{estimated_points}")
        with col2:
            st.metric("Win Ratio", f"{wins/38*100:.1f}%")
        with col3:
            st.metric("Goal Difference", f"{goal_difference:+.0f}")
