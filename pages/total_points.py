"""
Total Points Prediction Page
"""

import streamlit as st
import time
from utils.model_loader import load_model, prepare_input_dataframe
from utils.ui import show_fullscreen_bounce

def show():
    """Display the Total Points prediction page."""
    
    # Clear old session state on page load
    if 'total_points_result' in st.session_state:
        del st.session_state.total_points_result
    
    st.markdown("<h1 style='text-align: center; color: #00f2ff; text-shadow: 0 0 20px rgba(0, 242, 255, 0.5);'>TOTAL POINTS</h1>", unsafe_allow_html=True)
    
    # Load model
    try:
        model, features = load_model('total_points')
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return
    
    # Layout: inputs on left, button and results on right
    col_input, col_result = st.columns([1, 2])
    
    with col_input:
        st.markdown("""
<div class="glass-card">
    <h3 style="color: #00f2ff; margin-top: 0;">📊 CURRENT SEASON STATS</h3>
</div>
""", unsafe_allow_html=True)
        
        # Input fields matching the image
        played = st.number_input("Matches Played", value=20, min_value=0, max_value=38, step=1)
        gf = st.number_input("Goals Scored (GF)", value=35, min_value=0, step=1)
        ga = st.number_input("Goals Conceded (GA)", value=25, min_value=0, step=1)
        
        # Auto-calculate Goal Difference
        gd = gf - ga
        st.info(f"Calculated Goal Difference (GD): {gd}")
    
    with col_result:
        st.markdown("""
<div class="glass-card" style="text-align: center;">
    <p style="color: #ffd700;">👆 Enter current team stats to project the final season tally.</p>
</div>
""", unsafe_allow_html=True)
        
        # Predict Button on right side
        if st.button("🏆 PREDICT FINAL POINTS", use_container_width=True):
            show_fullscreen_bounce("PROJECTING FINAL POINTS...", seconds=3.2)
            
            # Input data - include season_end_year with default value
            input_data = {
                'season_end_year': 2024,  # Current season
                'played': played,
                'gf': gf,
                'ga': ga,
                'gd': gd
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
    <div style="font-size: 1.2rem; color: #b0b3b8;">PROJECTED POINTS</div>
    <div style="font-size: 5rem; font-weight: 800; color: {color}; text-shadow: 0 0 20px {color};">{icon} {predicted_points:.0f}</div>
    <div style="font-size: 1.5rem; color: white; margin-top: 0.5rem;">{category}</div>
</div>
""", unsafe_allow_html=True)
            
            st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
            
            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a:
                st.metric("Champion", "89", delta=f"{predicted_points - 89:.0f}")
            with col_b:
                st.metric("Top 4", "70", delta=f"{predicted_points - 70:.0f}")
            with col_c:
                st.metric("Mid-Table", "50", delta=f"{predicted_points - 50:.0f}")
            with col_d:
                st.metric("Safety", "35", delta=f"{predicted_points - 35:.0f}")
