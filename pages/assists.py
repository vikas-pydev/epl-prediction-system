"""
Assists Prediction Page
"""

import streamlit as st
import time
from utils.model_loader import load_model, prepare_input_dataframe
from utils.ui import show_fullscreen_bounce
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
    
    # Layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
<div class="glass-card">
    <h3 style="color: #00f2ff; margin-top: 0;">PLAYMAKER STATS</h3>
</div>
""", unsafe_allow_html=True)
        
        position = st.selectbox("Position", ['AT', 'MT', 'DF', 'GK'], index=0)
        age = st.number_input("Age", value=31, min_value=16, max_value=45, step=1)
        matches_played = st.number_input("Matches", value=32, min_value=0, max_value=50, step=1)
        starts = st.number_input("Starts", value=28, min_value=0, max_value=50, step=1)
        minutes = st.number_input("Minutes", value=2536, min_value=0, step=10)
        ninety_s = st.number_input("90s Played", value=28.2, min_value=0.0, step=0.1)
        xG = st.number_input("xG", value=21.1, min_value=0.0, step=0.1)
        npxG = st.number_input("npxG", value=15.6, min_value=0.0, step=0.1)
        xAG = st.number_input("xAG", value=11.4, min_value=0.0, step=0.1)
        npxG_xAG = st.number_input("npxG + xAG", value=27.0, min_value=0.0, step=0.1)
        progressive_carries = st.number_input("Prog. Carries", value=107, min_value=0, step=1)
        progressive_passes = st.number_input("Prog. Passes", value=149, min_value=0, step=1)
        progressive_receives = st.number_input("Prog. Receives", value=348, min_value=0, step=1)

    with col2:
        st.markdown("""
<div class="glass-card" style="text-align: center;">
    <h3 style="color: #00f2ff;">CREATIVITY ENGINE</h3>
    <p style="color: #b0b3b8;">Forecast assist numbers based on metrics.</p>
</div>
""", unsafe_allow_html=True)
        
        if st.button("🎯 PREDICT ASSISTS", use_container_width=True):
            show_fullscreen_bounce("ESTIMATING ASSIST TALLY...", seconds=3.2)
            
            xG_per90 = xG / ninety_s if ninety_s > 0 else 0
            xAG_per90 = xAG / ninety_s if ninety_s > 0 else 0
            npxG_per90 = npxG / ninety_s if ninety_s > 0 else 0
            
            input_data = {
                'Position': position, 'Age': age, 'Matches Played': matches_played,
                'Starts': starts, 'Minutes': minutes, '90s Played': ninety_s,
                'Penalty Goals Made': 5, 'Penalty Attempts': 7, 'Yellow Cards': 2, 'Red Cards': 0,
                'xG': xG, 'npxG': npxG, 'xAG': xAG, 'npxG + xAG': npxG_xAG,
                'Progressive Carries': progressive_carries, 'Progressive Passes': progressive_passes,
                'Progressive Receives': progressive_receives,
                'xG Per 90': xG_per90, 'xAG Per 90': xAG_per90, 'npxG Per 90': npxG_per90
            }
            
            X = prepare_input_dataframe(input_data, features)
            predicted_assists = int(round(model.predict(X)[0]))
            
            if predicted_assists >= 15:
                category, color, icon = "Elite Playmaker", "#ffd700", "🌟"
            elif predicted_assists >= 8:
                category, color, icon = "Creative Force", "#10b981", "🎯"
            else:
                category, color, icon = "Contributing Player", "#3b82f6", "📊"
            
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
                st.metric("xAG Performance", f"{predicted_assists - xAG:+.1f}")
