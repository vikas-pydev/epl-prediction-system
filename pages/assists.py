"""
Assists Prediction Page
Predicts number of assists a player will make
"""

import streamlit as st
import pandas as pd
import numpy as np
from utils.model_loader import load_model, prepare_input_dataframe

def show():
    """Display the Assists prediction page."""
    st.markdown("<h1>🎯 Assists Prediction</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color: white; font-size: 1.1rem; margin-bottom: 2rem;'>"
        "Predict how many assists a player will provide</p>",
        unsafe_allow_html=True
    )
    
    # Load model
    try:
        model, features = load_model('assists')
        st.success("✅ Model loaded successfully!")
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return
    
    # Display feature input form
    st.markdown("<h2 style='color: white;'>Enter Player Statistics</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Basic Information")
        position = st.selectbox("Position", ['AT', 'MT', 'DF', 'GK'], index=0)
        age = st.number_input("Age", value=31, min_value=16, max_value=45, step=1, help="Sample: Mohamed Salah")
        matches_played = st.number_input("Matches Played", value=32, min_value=0, max_value=50, step=1, help="Sample: Mohamed Salah")
        starts = st.number_input("Starts", value=28, min_value=0, max_value=50, step=1, help="Sample: Mohamed Salah")
        minutes = st.number_input("Minutes Played", value=2536, min_value=0, step=10, help="Sample: Mohamed Salah")
        ninety_s = st.number_input("90s Played", value=28.2, min_value=0.0, step=0.1, help="Sample: Mohamed Salah")
        
        st.markdown("#### Discipline")
        penalty_goals = st.number_input("Penalty Goals Made", value=5, min_value=0, step=1, help="Sample: Mohamed Salah")
        penalty_attempts = st.number_input("Penalty Attempts", value=7, min_value=0, step=1, help="Sample: Mohamed Salah")
        yellow_cards = st.number_input("Yellow Cards", value=2, min_value=0, step=1, help="Sample: Mohamed Salah")
        red_cards = st.number_input("Red Cards", value=0, min_value=0, step=1, help="Sample: Mohamed Salah")
    
    with col2:
        st.markdown("#### Expected Goals (xG) Metrics")
        xG = st.number_input("xG (Expected Goals)", value=21.1, min_value=0.0, step=0.1, help="Sample: Mohamed Salah")
        npxG = st.number_input("npxG (Non-Penalty xG)", value=15.6, min_value=0.0, step=0.1, help="Sample: Mohamed Salah")
        xAG = st.number_input("xAG (Expected Assisted Goals)", value=11.4, min_value=0.0, step=0.1, help="Sample: Mohamed Salah")
        npxG_xAG = st.number_input("npxG + xAG", value=27.0, min_value=0.0, step=0.1, help="Sample: Mohamed Salah")
        
        st.markdown("#### Advanced Metrics")
        progressive_carries = st.number_input("Progressive Carries", value=107, min_value=0, step=1, help="Sample: Mohamed Salah")
        progressive_passes = st.number_input("Progressive Passes", value=149, min_value=0, step=1, help="Sample: Mohamed Salah")
        progressive_receives = st.number_input("Progressive Receives", value=348, min_value=0, step=1, help="Sample: Mohamed Salah")
        
        st.markdown("#### Per 90 Stats")
        xG_per90 = st.number_input("xG Per 90", value=0.75, min_value=0.0, step=0.01, help="Sample: Mohamed Salah")
        xAG_per90 = st.number_input("xAG Per 90", value=0.41, min_value=0.0, step=0.01, help="Sample: Mohamed Salah")
        npxG_per90 = st.number_input("npxG Per 90", value=0.55, min_value=0.0, step=0.01, help="Sample: Mohamed Salah")
    
    # Info box
    st.info("💡 **Top Playmakers** typically have xAG > 10, high progressive passes (100+), and xAG Per 90 > 0.3")
    
    # Predict button
    if st.button("🔮 Predict Assists", use_container_width=True):
        # Prepare input data
        input_data = {
            'Position': position,
            'Age': age,
            'Matches Played': matches_played,
            'Starts': starts,
            'Minutes': minutes,
            '90s Played': ninety_s,
            'Penalty Goals Made': penalty_goals,
            'Penalty Attempts': penalty_attempts,
            'Yellow Cards': yellow_cards,
            'Red Cards': red_cards,
            'xG': xG,
            'npxG': npxG,
            'xAG': xAG,
            'npxG + xAG': npxG_xAG,
            'Progressive Carries': progressive_carries,
            'Progressive Passes': progressive_passes,
            'Progressive Receives': progressive_receives,
            'xG Per 90': xG_per90,
            'xAG Per 90': xAG_per90,
            'npxG Per 90': npxG_per90
        }
        
        # Create DataFrame
        X = prepare_input_dataframe(input_data, features)
        
        # Make prediction
        raw_prediction = model.predict(X)[0]
        predicted_assists = int(round(raw_prediction))
        
        # Display results
        st.markdown("---")
        st.markdown("<h2 style='color: white;'>Prediction Results</h2>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Determine category
            if predicted_assists >= 15:
                category = "Elite Playmaker"
                color = "#f59e0b" # Amber
                glow = "0 0 20px #f59e0b"
                icon = "🌟"
            elif predicted_assists >= 8:
                category = "Creative Force"
                color = "#10b981" # Emerald
                glow = "0 0 20px #10b981"
                icon = "🎯"
            elif predicted_assists >= 4:
                category = "Contributing Player"
                color = "#3b82f6" # Blue
                glow = "0 0 20px #3b82f6"
                icon = "📊"
            else:
                category = "Limited Creation"
                color = "#9ca3af" # Gray
                glow = "none"
                icon = "📉"
            
            st.markdown(
                f"<div class='result-card' style='text-align: center; padding: 2rem; background: rgba(255,255,255,0.05); border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);'>"
                f"<div class='result-title' style='color: #94a3b8; font-size: 1.2rem; margin-bottom: 1rem;'>PREDICTED ASSISTS</div>"
                f"<div class='result-value' style='color: {color}; font-size: 5rem; font-weight: 800; text-shadow: {glow}; line-height: 1;'>{icon} {predicted_assists}</div>"
                f"<div class='result-subtitle' style='color: white; font-size: 1.5rem; margin-top: 1rem; font-weight: 600;'>{category}</div>"
                "</div>",
                unsafe_allow_html=True
            )
        
        # Show detailed metrics
        st.markdown("### Creativity Analysis")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            assists_per_90 = (predicted_assists / ninety_s) if ninety_s > 0 else 0
            st.metric("Predicted Assists/90", f"{assists_per_90:.2f}")
        with col2:
            st.metric("Expected Assists (xAG)", f"{xAG:.1f}")
        with col3:
            overperformance = predicted_assists - xAG
            st.metric("Over/Under xAG", f"{overperformance:+.1f}",
                     delta="Overperforming" if overperformance > 0 else "Underperforming")
        with col4:
            if ninety_s > 0:
                key_passes_est = (progressive_passes / ninety_s) * 90
                st.metric("Key Actions/90", f"{key_passes_est:.1f}")
            else:
                st.metric("Key Actions", "N/A")
        
        # Playmaking style analysis
        st.markdown("### Playmaking Style")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Progressive Passes", progressive_passes,
                     delta="High" if progressive_passes > 60 else "Low")
        with col2:
            st.metric("Progressive Carries", progressive_carries,
                     delta="High" if progressive_carries > 60 else "Low")
        with col3:
            st.metric("Progressive Receives", progressive_receives,
                     delta="High" if progressive_receives > 50 else "Low")
