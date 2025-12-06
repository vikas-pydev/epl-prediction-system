"""
Assists Prediction Page
"""

import streamlit as st
import time
from utils.model_loader import load_model, prepare_input_dataframe
from utils.ui import show_fullscreen_bounce

def show():
    """Display the Assists prediction page."""
    st.markdown("<h1 style='text-align: center; text-shadow: 0 0 20px rgba(0, 242, 255, 0.5);'>🎯 ASSIST PREDICTOR</h1>", unsafe_allow_html=True)
    
    # Load model
    try:
        model, features = load_model('assists')
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return
    
    # Layout: inputs on left, prediction on right
    col_input, col_result = st.columns([1, 2])
    
    with col_input:
        st.markdown("""
<div class="glass-card">
    <h3 style="color: #00f2ff; margin-top: 0;">PLAYMAKER STATS</h3>
</div>
""", unsafe_allow_html=True)
        
        # Two sub-columns for inputs
        sub1, sub2 = st.columns(2)
        
        with sub1:
            position = st.selectbox("Position", ['Forward', 'Midfielder', 'Defender', 'Goalkeeper'], index=1)
            age = st.number_input("Age", value=25, min_value=16, max_value=45, step=1)
            matches_played = st.number_input("Matches Played", value=30, min_value=0, max_value=50, step=1)
            starts = st.number_input("Starts", value=30, min_value=0, max_value=50, step=1)
            minutes = st.number_input("Minutes Played", value=2700, min_value=0, step=10)
        
        with sub2:
            goals_per_90 = st.number_input("Goals per 90", value=0.50, min_value=0.0, step=0.01)
            assists_per_90 = st.number_input("Assists per 90", value=0.20, min_value=0.0, step=0.01)
            xg_per_90 = st.number_input("xG per 90", value=0.45, min_value=0.0, step=0.01)
            npxg_per_90 = st.number_input("npxG per 90", value=0.40, min_value=0.0, step=0.01)
            xag_per_90 = st.number_input("xAG per 90", value=0.20, min_value=0.0, step=0.01)
            npxg_plus_xag_per_90 = st.number_input("npxG + xAG", value=0.60, min_value=0.0, step=0.01)
            non_penalty_goals_per_90 = st.number_input("Non-Penalty Goals per 90", value=0.40, min_value=0.0, step=0.01)
    
    with col_result:
        st.markdown("""
<div class="glass-card" style="text-align: center;">
    <h3 style="color: #00f2ff;">CREATIVITY ENGINE</h3>
    <p style="color: #b0b3b8;">Forecast assist numbers based on metrics.</p>
</div>
""", unsafe_allow_html=True)
        
        if st.button("🎯 PREDICT ASSISTS", use_container_width=True):
            show_fullscreen_bounce("ESTIMATING ASSIST TALLY...", seconds=3.2)
            
            # Calculate derived features
            goals_per_xg = goals_per_90 / xg_per_90 if xg_per_90 > 0 else 1.0
            assists_per_xag = assists_per_90 / xag_per_90 if xag_per_90 > 0 else 1.0
            xag_impact = xag_per_90 - assists_per_90
            npxg_impact = npxg_per_90 - non_penalty_goals_per_90
            
            # Input data matching the 16 features required by the model
            input_data = {
                'position': position,
                'age': age,
                'matches_played': matches_played,
                'starts': starts,
                'minutes': minutes,
                'goals_per_90': goals_per_90,
                'assists_per_90': assists_per_90,
                'xg_per_90': xg_per_90,
                'npxg_per_90': npxg_per_90,
                'xag_per_90': xag_per_90,
                'npxg_plus_xag_per_90': npxg_plus_xag_per_90,
                'non_penalty_goals_per_90': non_penalty_goals_per_90,
                'goals_per_xg': goals_per_xg,
                'assists_per_xag': assists_per_xag,
                'xag_impact': xag_impact,
                'npxg_impact': npxg_impact
            }
            
            X = prepare_input_dataframe(input_data, features)
            predicted_assists = int(round(model.predict(X)[0]))
            
            if predicted_assists >= 15:
                category, color, icon = "Elite Playmaker", "#ffd700", "🌟"
            elif predicted_assists >= 8:
                category, color, icon = "Creative Force", "#10b981", "🎯"
            else:
                category, color, icon = "Contributing Player", "#3b82f6", "📊"
            
            ninety_s = minutes / 90 if minutes > 0 else 1
            
            st.markdown(f"""
<div class="glass-card" style="text-align: center; border: 2px solid {color}; box-shadow: 0 0 30px {color};">
    <div style="font-size: 1.2rem; color: #b0b3b8;">PREDICTED ASSISTS</div>
    <div style="font-size: 5rem; font-weight: 800; color: {color}; text-shadow: 0 0 20px {color};">{icon} {predicted_assists}</div>
    <div style="font-size: 1.5rem; color: white;">{category}</div>
</div>
""", unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Assists per 90", f"{predicted_assists/ninety_s:.2f}" if ninety_s > 0 else "0")
            with col_b:
                xag_total = xag_per_90 * ninety_s
                st.metric("xAG Performance", f"{predicted_assists - xag_total:+.1f}")
