"""
Total Points Prediction Page
Predicts total points a team will achieve in the season
"""

import streamlit as st
import pandas as pd
import numpy as np
from utils.model_loader import load_model, prepare_input_dataframe

def show():
    """Display the Total Points prediction page."""
    st.markdown("<h1>📊 Total Points Prediction</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color: white; font-size: 1.1rem; margin-bottom: 2rem;'>"
        "Predict total points a team will achieve in the season</p>",
        unsafe_allow_html=True
    )
    
    # Load model
    try:
        model, features = load_model('total_points')
        st.success("✅ Model loaded successfully!")
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return
    
    # Display feature input form
    st.markdown("<h2 style='color: white;'>Enter Team Season Statistics</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        goals_scored = st.number_input("Goals Scored", value=96.0, min_value=0.0, step=1.0, help="Sample: Man City 23/24")
    with col2:
        goals_conceded = st.number_input("Goals Conceded", value=34.0, min_value=0.0, step=1.0, help="Sample: Man City 23/24")
    with col3:
        goal_difference = st.number_input("Goal Difference", value=62.0, step=1.0, help="Sample: Man City 23/24")
    
    # Info box
    st.info("💡 **Points Guide**: Champion (85-100pts) | Top 4 (65-85pts) | Mid-table (40-60pts) | Relegation (<35pts)")
    
    # Predict button
    if st.button("🔮 Predict Total Points", use_container_width=True):
        # Prepare input data
        input_data = {
            'goals_scored': goals_scored,
            'goals_conceded': goals_conceded,
            'goal_difference': goal_difference
        }
        
        # Create DataFrame
        X = prepare_input_dataframe(input_data, features)
        
        # Make prediction
        predicted_points = model.predict(X)[0]
        
        # Display results
        st.markdown("---")
        st.markdown("<h2 style='color: white;'>Prediction Results</h2>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Determine category
            if predicted_points >= 85:
                category = "Title Contender"
                color = "#f59e0b" # Amber
                glow = "0 0 20px #f59e0b"
                icon = "👑"
            elif predicted_points >= 65:
                category = "Top 4 Finish"
                color = "#10b981" # Emerald
                glow = "0 0 20px #10b981"
                icon = "🏆"
            elif predicted_points >= 40:
                category = "Mid-Table"
                color = "#3b82f6" # Blue
                glow = "0 0 20px #3b82f6"
                icon = "📊"
            else:
                category = "Relegation Battle"
                color = "#ef4444" # Red
                glow = "0 0 20px #ef4444"
                icon = "⚠️"
            
            st.markdown(
                f"<div class='result-card' style='text-align: center; padding: 2rem; background: rgba(255,255,255,0.05); border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);'>"
                f"<div class='result-title' style='color: #94a3b8; font-size: 1.2rem; margin-bottom: 1rem;'>PREDICTED TOTAL POINTS</div>"
                f"<div class='result-value' style='color: {color}; font-size: 5rem; font-weight: 800; text-shadow: {glow}; line-height: 1;'>{icon} {predicted_points:.0f}</div>"
                f"<div class='result-subtitle' style='color: white; font-size: 1.5rem; margin-top: 1rem; font-weight: 600;'>{category}</div>"
                "</div>",
                unsafe_allow_html=True
            )
        
        # Show comparison
        st.markdown("### Performance Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Predicted Points", f"{predicted_points:.0f}")
        with col2:
            st.metric("Goal Difference", f"{goal_difference:.0f}")
            
        st.info("ℹ️ **Sample Data**: Man City 2023-24 (Actual Points: 91)")
        
        # Points per game analysis
        st.markdown("### Historical Context")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            champion_pts = 89  # Average champion points
            st.metric("Champion Level", f"{champion_pts}", 
                     delta=f"{predicted_points - champion_pts:.0f}" if predicted_points >= champion_pts else None)
        with col2:
            top4_pts = 70  # Average top 4 cutoff
            st.metric("Top 4 Level", f"{top4_pts}",
                     delta=f"{predicted_points - top4_pts:.0f}" if predicted_points >= top4_pts else None)
        with col3:
            midtable_pts = 50  # Mid-table average
            st.metric("Mid-Table Level", f"{midtable_pts}",
                     delta=f"{predicted_points - midtable_pts:.0f}" if predicted_points >= midtable_pts else None)
        with col4:
            relegation_pts = 35  # Relegation cutoff
            st.metric("Relegation Line", f"{relegation_pts}",
                     delta=f"{predicted_points - relegation_pts:.0f}" if predicted_points > relegation_pts else None,
                     delta_color="normal" if predicted_points > relegation_pts else "inverse")
