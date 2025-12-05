"""
Match Winner Prediction Page
"""

import streamlit as st
import time
from utils.model_loader import load_model, prepare_input_dataframe, get_prediction_probability
from utils.ui import render_form_dots, show_fullscreen_bounce

def show():
    """Display the Match Winner prediction page."""
    
    st.markdown("<h1 style='text-align: center; text-shadow: 0 0 20px rgba(57, 255, 20, 0.5);'>🏆 MATCHDAY PREDICTOR</h1>", unsafe_allow_html=True)
    
    # Load model
    try:
        model, features = load_model('match_winner')
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return
    
    # Layout
    col_input, col_visual = st.columns([1, 2])
    
    with col_input:
        st.markdown("""
<div class="glass-card">
    <h3 style="color: #39FF14; margin-top: 0;">MATCH SETUP</h3>
</div>
""", unsafe_allow_html=True)
        
        st.markdown("#### Team Stats")
        home_goals_scored = st.number_input("Home Goals Scored", value=45, step=1)
        home_goals_conceded = st.number_input("Home Goals Conceded", value=67, step=1)
        away_goals_scored = st.number_input("Away Goals Scored", value=50, step=1)
        
        st.markdown("#### Form Guide")
        home_win_streak = st.slider("Home Win Streak", 0, 5, 1)
        away_win_streak = st.slider("Away Win Streak", 0, 5, 2)
        form_gap = st.number_input("Form Gap", value=-5.0, step=1.0)
        home_form = st.text_input("Home Form (W-D-L-W-W)", value="W-D-L-W-W")
        away_form = st.text_input("Away Form (W-W-D-W-L)", value="W-W-D-W-L")
        
        st.markdown("#### Differentials")
        goal_diff_gap = st.number_input("Goal Diff Gap", value=-10.0, step=0.1)
        points_gap = st.number_input("Points Gap", value=-8.0, step=0.1)
        home_goal_diff = st.number_input("Home Goal Diff", value=-22.0, step=0.1)
        away_goal_diff = st.number_input("Away Goal Diff", value=-12.0, step=0.1)

    with col_visual:
        # Versus Display with Form Guide
        st.markdown("""
<div class="glass-card" style="text-align: center; padding: 2rem;">
    <div style="display: flex; justify-content: center; align-items: center; gap: 3rem;">
        <div>
            <div style="background: #ef4444; border-radius: 50%; width: 100px; height: 100px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; margin: 0 auto;">🏠</div>
            <h3 style="margin-top: 1rem;">HOME</h3>
            <div style="margin-top: 0.5rem;">""" + render_form_dots(home_form) + """</div>
        </div>
        <div class="vs-badge">VS</div>
        <div>
            <div style="background: #3b82f6; border-radius: 50%; width: 100px; height: 100px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; margin: 0 auto;">✈️</div>
            <h3 style="margin-top: 1rem;">AWAY</h3>
            <div style="margin-top: 0.5rem;">""" + render_form_dots(away_form) + """</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
        
        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
        
        # Analyze Button
        if st.button("⚽ ANALYZE MATCHUP", use_container_width=True):
            show_fullscreen_bounce("ANALYZING MATCH DATA...", seconds=3.2)
            
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
            
            # Create DataFrame and predict
            X = prepare_input_dataframe(input_data, features)
            prediction, proba = get_prediction_probability(model, X)
            
            # Display Results
            winner_text = "HOME TEAM" if prediction == 1 else "NON-HOME TEAM"
            winner_color = "#39ff14" if prediction == 1 else "#ef4444"
            
            st.markdown(f"""
<div class="glass-card" style="text-align: center; border: 2px solid {winner_color}; box-shadow: 0 0 30px {winner_color};">
    <div style="display: flex; justify-content: center; align-items: center; gap: 3rem; margin-bottom: 1.5rem;">
        <div>
            <div style="font-size: 1.2rem; color: #b0b3b8;">HOME</div>
            <div style="font-size: 5rem; font-weight: 800; color: {'#39ff14' if prediction == 1 else 'white'};">{'2' if prediction == 1 else '0'}</div>
        </div>
        <div style="font-size: 3rem; color: #555;">-</div>
        <div>
            <div style="font-size: 1.2rem; color: #b0b3b8;">AWAY</div>
            <div style="font-size: 5rem; font-weight: 800; color: {'#39ff14' if prediction == 0 else 'white'};">{'1' if prediction == 1 else '1'}</div>
        </div>
    </div>
    <div style="font-size: 1rem; color: #b0b3b8; letter-spacing: 2px;">PREDICTED WINNER</div>
    <div class="pulse-glow" style="font-size: 3rem; font-weight: 800; color: {winner_color}; text-shadow: 0 0 30px {winner_color}; margin-top: 0.5rem;">
        {winner_text}
    </div>
</div>
""", unsafe_allow_html=True)
