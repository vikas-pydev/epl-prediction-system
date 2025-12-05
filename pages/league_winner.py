"""
League Winner (Champion) Prediction Page
"""

import streamlit as st
import time
from utils.model_loader import load_model, prepare_input_dataframe, get_prediction_probability
from utils.ui import show_fullscreen_bounce
from utils.ui import show_fullscreen_bounce

def show():
    """Display the League Winner prediction page."""
    st.markdown("<h1 style='text-align: center; text-shadow: 0 0 20px rgba(255, 215, 0, 0.5);'>👑 LEAGUE CHAMPION</h1>", unsafe_allow_html=True)
    
    # Load model
    try:
        model, features = load_model('league_winner')
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return
    
    # Layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
<div class="glass-card">
    <h3 style="color: #ffd700; margin-top: 0;">SEASON STATS</h3>
</div>
""", unsafe_allow_html=True)
        
        wins = st.number_input("Wins", value=28, min_value=0, max_value=38, step=1)
        draws = st.number_input("Draws", value=7, min_value=0, max_value=38, step=1)
        losses = st.number_input("Losses", value=3, min_value=0, max_value=38, step=1)
        points_per_game = st.number_input("Points Per Game", value=2.39, min_value=0.0, max_value=3.0, step=0.01)
        goals_scored = st.number_input("Goals Scored", value=96.0, min_value=0.0, step=1.0)
        goals_conceded = st.number_input("Goals Conceded", value=34.0, min_value=0.0, step=1.0)
        goal_difference = st.number_input("Goal Difference", value=62.0, step=1.0)
    
    with col2:
        st.markdown("""
<div class="glass-card" style="text-align: center;">
    <h3 style="color: #ffd700;">CHAMPIONSHIP POTENTIAL</h3>
    <p style="color: #b0b3b8;">Analyze if this team can lift the trophy.</p>
</div>
""", unsafe_allow_html=True)
        
        if st.button("👑 PREDICT CHAMPIONSHIP", use_container_width=True):
            show_fullscreen_bounce("CALCULATING TITLE ODDS...", seconds=3.2)
            
            input_data = {
                'wins': wins, 'draws': draws, 'losses': losses,
                'points_per_game': points_per_game, 'goals_scored': goals_scored,
                'goals_conceded': goals_conceded, 'goal_difference': goal_difference
            }
            
            X = prepare_input_dataframe(input_data, features)
            prediction, proba = get_prediction_probability(model, X)
            
            if prediction == 1:
                st.markdown(f"""
<div class="glass-card pulse-glow" style="text-align: center; border: 2px solid #ffd700; box-shadow: 0 0 40px rgba(255, 215, 0, 0.5);">
    <div style="font-size: 1.2rem; color: #b0b3b8;">PREDICTION</div>
    <div style="font-size: 4rem; color: #ffd700; text-shadow: 0 0 30px #ffd700;">👑 CHAMPION</div>
    <div style="font-size: 1.5rem; color: white; margin-top: 1rem;">Probability: <span style="color: #ffd700;">{proba[1]*100:.1f}%</span></div>
</div>
""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
<div class="glass-card" style="text-align: center; border: 2px solid #94a3b8;">
    <div style="font-size: 1.2rem; color: #b0b3b8;">PREDICTION</div>
    <div style="font-size: 4rem; color: #94a3b8;">❌ NOT CHAMPION</div>
    <div style="font-size: 1.5rem; color: white; margin-top: 1rem;">Probability: <span style="color: #ffd700;">{proba[1]*100:.1f}%</span></div>
</div>
""", unsafe_allow_html=True)
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Est. Points", f"{wins * 3 + draws}")
            with col_b:
                st.metric("Win Rate", f"{wins/38*100:.1f}%")
            with col_c:
                st.metric("Goal Diff", f"{goal_difference:+.0f}")
