"""
EPL Prediction System - Streamlit Application
Main entry point with navigation to all prediction models.
"""

import streamlit as st
from utils.styles import get_custom_css

# Page configuration
st.set_page_config(
    page_title="EPL Prediction System",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit's default pages navigation  
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

def nav(page_name, message=""):
    st.session_state.current_page = page_name
    st.rerun()

# Main App
if st.session_state.current_page == 'home':
    # Hero Section
    st.markdown("""
<div style="text-align: center; padding: 4rem 0;">
    <h1 style="font-size: 4rem; margin-bottom: 0; text-shadow: 0 0 30px rgba(57, 255, 20, 0.5);">PREMIER LEAGUE</h1>
    <h1 style="font-size: 4rem; margin-top: 0; color: #39FF14;">INTELLIGENCE</h1>
    <p style="font-size: 1.3rem; color: #b0b3b8; letter-spacing: 3px; margin-top: 1rem;">
        ELITE ANALYTICS • POWERED BY SCORESIGHT™
    </p>
</div>
""", unsafe_allow_html=True)
    
    # Enter Arena Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⚽ ENTER THE ARENA", use_container_width=True):
            nav('match_winner', "Entering Arena...")
            
    st.markdown("<div style='height: 3rem'></div>", unsafe_allow_html=True)
    
    # Feature Cards Grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
<div class="glass-card">
    <h3 style="color: #39FF14;">🏆 MATCH WINNER</h3>
    <p style="color: #b0b3b8;">Predict match outcomes with elite accuracy.</p>
</div>
""", unsafe_allow_html=True)
        if st.button("LAUNCH", key="btn_match"):
            nav('match_winner', "Loading Match Predictor...")
            
        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
        
        st.markdown("""
<div class="glass-card">
    <h3 style="color: #00f2ff;">📊 TOTAL POINTS</h3>
    <p style="color: #b0b3b8;">Forecast final league standings.</p>
</div>
""", unsafe_allow_html=True)
        if st.button("PROJECT", key="btn_points"):
            nav('total_points', "Loading Points Model...")

    with col2:
        st.markdown("""
<div class="glass-card">
    <h3 style="color: #ffd700;">👑 LEAGUE WINNER</h3>
    <p style="color: #b0b3b8;">Identify the potential champion.</p>
</div>
""", unsafe_allow_html=True)
        if st.button("PREDICT", key="btn_league"):
            nav('league_winner', "Loading Title Model...")
            
        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
        
        st.markdown("""
<div class="glass-card">
    <h3 style="color: #39FF14;">⚽ PLAYER GOALS</h3>
    <p style="color: #b0b3b8;">Analyze top scorers and goal tallies.</p>
</div>
""", unsafe_allow_html=True)
        if st.button("ANALYZE", key="btn_goals"):
            nav('goals', "Loading Goals Model...")

    with col3:
        st.markdown("""
<div class="glass-card">
    <h3 style="color: #00f2ff;">🎯 PLAYER ASSISTS</h3>
    <p style="color: #b0b3b8;">Track playmakers and assist leaders.</p>
</div>
""", unsafe_allow_html=True)
        if st.button("TRACK", key="btn_assists"):
            nav('assists', "Loading Assists Model...")
            
        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
        
        st.markdown("""
<div class="glass-card pulse-glow" style="border-color: #39FF14;">
    <h3 style="color: #39FF14;">🚀 AI POWERED</h3>
    <p style="color: #b0b3b8;">Real-time machine learning analysis.</p>
</div>
""", unsafe_allow_html=True)

# Import and display pages based on navigation
elif st.session_state.current_page == 'match_winner':
    if st.button("← BACK TO HOME", key="back_match"):
        nav('home', "Returning...")
    from pages import match_winner
    match_winner.show()
    
elif st.session_state.current_page == 'league_winner':
    if st.button("← BACK TO HOME", key="back_league"):
        nav('home', "Returning...")
    from pages import league_winner
    league_winner.show()
    
elif st.session_state.current_page == 'total_points':
    if st.button("← BACK TO HOME", key="back_points"):
        nav('home', "Returning...")
    from pages import total_points
    total_points.show()
    
elif st.session_state.current_page == 'goals':
    if st.button("← BACK TO HOME", key="back_goals"):
        nav('home', "Returning...")
    from pages import goals
    goals.show()
    
elif st.session_state.current_page == 'assists':
    if st.button("← BACK TO HOME", key="back_assists"):
        nav('home', "Returning...")
    from pages import assists
    assists.show()

# Sidebar Navigation
with st.sidebar:
    st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="font-size: 3rem; margin: 0;">⚽</h1>
    <h3 style="margin: 0; color: #39FF14;">EPL PREDICTOR</h3>
    <p style="color: #b0b3b8; font-size: 0.8rem;">v2.0 Elite</p>
</div>
""", unsafe_allow_html=True)
    
    if st.button("🏠 DASHBOARD", use_container_width=True):
        nav('home', "Loading Dashboard...")
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("<p style='color: #b0b3b8; font-size: 0.7rem; letter-spacing: 2px;'>MODELS</p>", unsafe_allow_html=True)
    
    if st.button("🏆 MATCH WINNER", key="sb_match", use_container_width=True):
        nav('match_winner', "Loading Match Predictor...")
    
    if st.button("👑 LEAGUE WINNER", key="sb_league", use_container_width=True):
        nav('league_winner', "Loading Title Model...")
    
    if st.button("📊 TOTAL POINTS", key="sb_points", use_container_width=True):
        nav('total_points', "Loading Points Model...")
    
    if st.button("⚽ PLAYER GOALS", key="sb_goals", use_container_width=True):
        nav('goals', "Loading Goals Model...")
    
    if st.button("🎯 PLAYER ASSISTS", key="sb_assists", use_container_width=True):
        nav('assists', "Loading Assists Model...")
