"""
Total Points Prediction Page
"""

import streamlit as st
import time
from utils.model_loader import load_model, prepare_input_dataframe
from utils.ui import show_fullscreen_bounce
from utils.ui import show_fullscreen_bounce

def show():
    """Display the Total Points prediction page."""
    st.markdown("<h1 style='text-align: center; text-shadow: 0 0 20px rgba(0, 242, 255, 0.5);'>📊 POINTS PROJECTOR</h1>", unsafe_allow_html=True)
    
    # Load model
    try:
        model, features = load_model('total_points')
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return
    
    # Layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
<div class="glass-card">
    <h3 style="color: #00f2ff; margin-top: 0;">TEAM METRICS</h3>
</div>
""", unsafe_allow_html=True)
        
        goals_scored = st.number_input("Goals Scored", value=96.0, min_value=0.0, step=1.0)
        goals_conceded = st.number_input("Goals Conceded", value=34.0, min_value=0.0, step=1.0)
        goal_difference = st.number_input("Goal Difference", value=62.0, step=1.0)

    with col2:
        st.markdown("""
<div class="glass-card" style="text-align: center;">
    <h3 style="color: #00f2ff;">POINTS FORECAST</h3>
    <p style="color: #b0b3b8;">Predict final points based on goal metrics.</p>
</div>
""", unsafe_allow_html=True)
        
        if st.button("📊 PROJECT POINTS", use_container_width=True):
            show_fullscreen_bounce("RUNNING SEASON SIMULATION...", seconds=3.2)
            
            input_data = {
                'goals_scored': goals_scored,
                'goals_conceded': goals_conceded,
                'goal_difference': goal_difference
            }
            
            X = prepare_input_dataframe(input_data, features)
            predicted_points = model.predict(X)[0]
            
            # Determine category
            if predicted_points >= 85:
                category, color, icon = "Title Contender", "#ffd700", "👑"
            elif predicted_points >= 65:
                category, color, icon = "Top 4 Finish", "#10b981", "🏆"
            elif predicted_points >= 40:
                category, color, icon = "Mid-Table", "#3b82f6", "📊"
            else:
                category, color, icon = "Relegation Battle", "#ef4444", "⚠️"
            
            st.markdown(f"""
<div class="glass-card" style="text-align: center; border: 2px solid {color}; box-shadow: 0 0 30px {color};">
    <div style="font-size: 1.2rem; color: #b0b3b8;">PROJECTED FINISH</div>
    <div style="font-size: 5rem; font-weight: 800; color: {color}; text-shadow: 0 0 20px {color};">{icon} {predicted_points:.0f}</div>
    <div style="font-size: 1.5rem; color: white; margin-top: 0.5rem;">{category}</div>
</div>
""", unsafe_allow_html=True)
            
            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a:
                st.metric("Champion", "89", delta=f"{predicted_points - 89:.0f}")
            with col_b:
                st.metric("Top 4", "70", delta=f"{predicted_points - 70:.0f}")
            with col_c:
                st.metric("Mid-Table", "50", delta=f"{predicted_points - 50:.0f}")
            with col_d:
                st.metric("Safety", "35", delta=f"{predicted_points - 35:.0f}")
