"""
Custom CSS styling for the Streamlit app.
Stadium Night Theme with Glassmorphism.
"""

def get_custom_css():
    """Return custom CSS for beautiful UI styling."""
    return """
<style>
/* Import Fonts - Oswald & Roboto Condensed + Material Icons */
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@300;400;500;700&family=Roboto+Condensed:wght@300;400;700&display=swap');
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

/* CLEAN SOLUTION: Hide all sidebar toggle controls completely */
/* The sidebar is always expanded by default, so users can still navigate */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebar"] button[kind="header"],
[data-testid="stSidebar"] [data-testid="stBaseButton-header"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

/* Global Variables - Stadium Night Theme */
:root {
    --bg-dark: #0e1117;
    --primary-accent: #39FF14;
    --secondary-accent: #00f2ff;
    --text-primary: #ffffff;
    --text-secondary: #b0b3b8;
    --glass-bg: rgba(14, 17, 23, 0.7);
    --glass-border: rgba(255, 255, 255, 0.1);
}

/* Main Container & Background - Stadium Night */
[data-testid="stAppViewContainer"] {
    background-color: var(--bg-dark) !important;
    background-image: 
        radial-gradient(ellipse at 50% 0%, rgba(57, 255, 20, 0.15) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(0, 242, 255, 0.1) 0%, transparent 40%),
        radial-gradient(ellipse at 20% 80%, rgba(0, 242, 255, 0.08) 0%, transparent 40%) !important;
    background-attachment: fixed !important;
    color: var(--text-primary) !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Oswald', sans-serif !important;
    color: var(--text-primary) !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

p, div, span, label, input, button, li {
    font-family: 'Roboto Condensed', sans-serif !important;
}

/* Glassmorphism Cards */
.glass-card {
    background: var(--glass-bg) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 16px !important;
    padding: 1.5rem !important;
    transition: transform 0.3s ease, box-shadow 0.3s ease !important;
    margin-bottom: 1rem !important;
}

.glass-card:hover {
    transform: scale(1.02) !important;
    box-shadow: 0 0 25px rgba(57, 255, 20, 0.3) !important;
    border-color: var(--primary-accent) !important;
}

/* Custom Buttons - Green Theme */
.stButton > button {
    background: transparent !important;
    border: 2px solid var(--primary-accent) !important;
    color: var(--primary-accent) !important;
    border-radius: 8px !important;
    font-family: 'Oswald', sans-serif !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
    letter-spacing: 1px !important;
    transition: all 0.3s ease !important;
    padding: 0.75rem 1.5rem !important;
}

.stButton > button:hover {
    background: var(--primary-accent) !important;
    color: #000 !important;
    box-shadow: 0 0 20px var(--primary-accent) !important;
}

/* Inputs - Cyan Focus with VISIBLE TEXT */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid var(--glass-border) !important;
    color: #000000 !important;
    border-radius: 8px !important;
    -webkit-text-fill-color: #000000 !important;
}

/* Selectbox with white background */
.stSelectbox > div > div {
    background-color: #ffffff !important;
    border: 1px solid var(--glass-border) !important;
    color: #000000 !important;
    border-radius: 8px !important;
}

.stSelectbox > div > div > div {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

/* Dropdown menu options */
[data-baseweb="select"] > div,
[data-baseweb="popover"] {
    background-color: #ffffff !important;
}

[data-baseweb="menu"] {
    background-color: #ffffff !important;
}

[data-baseweb="menu"] li {
    color: #000000 !important;
    background-color: #ffffff !important;
}

[data-baseweb="menu"] li:hover {
    background-color: #f0f0f0 !important;
}

/* Force visible text in all input fields - BLACK text on white bg */
input[type="text"], 
input[type="number"],
.stTextInput input,
.stNumberInput input {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    opacity: 1 !important;
    caret-color: #000000 !important;
}

/* Input placeholder text - dark gray */
input::placeholder {
    color: rgba(0, 0, 0, 0.5) !important;
    -webkit-text-fill-color: rgba(0, 0, 0, 0.5) !important;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stSelectbox > div > div:focus-within {
    border-color: var(--secondary-accent) !important;
    box-shadow: 0 0 15px rgba(0, 242, 255, 0.3) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: rgba(14, 17, 23, 0.95) !important;
    border-right: 1px solid var(--glass-border) !important;
}

/* Sidebar Buttons */
[data-testid="stSidebar"] .stButton > button {
    border: none !important;
    border-left: 3px solid transparent !important;
    border-radius: 0 !important;
    text-align: left !important;
    padding-left: 1rem !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(90deg, rgba(57, 255, 20, 0.1) 0%, transparent 100%) !important;
    border-left-color: var(--primary-accent) !important;
    box-shadow: none !important;
}

/* Animations */
@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 10px rgba(57, 255, 20, 0.4); }
    50% { box-shadow: 0 0 25px rgba(57, 255, 20, 0.8); }
}

.pulse-glow {
    animation: pulse-glow 2s infinite !important;
}

/* Versus Badge */
.vs-badge {
    font-family: 'Oswald', sans-serif !important;
    font-size: 3rem !important;
    font-weight: 700 !important;
    color: var(--secondary-accent) !important;
    text-shadow: 0 0 20px rgba(0, 242, 255, 0.5) !important;
}

/* Form Guide Dots */
.form-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    display: inline-block;
    margin: 0 3px;
}
.form-dot.win { background: #22c55e; }
.form-dot.draw { background: #94a3b8; }
.form-dot.loss { background: #ef4444; }

/* Hide Streamlit Elements */
#MainMenu {visibility: hidden !important;}
footer {visibility: hidden !important;}
header {background: transparent !important;}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.3);
}

/* Label Colors */
label {
    color: var(--text-secondary) !important;
}
@keyframes bounceY { 0%, 100% { transform: translateY(0) } 50% { transform: translateY(-18px) } }
@keyframes glowPulse { 0%,100% { text-shadow: 0 0 10px rgba(0, 242, 255, 0.5) } 50% { text-shadow: 0 0 24px rgba(0, 242, 255, 0.9) } }
.fs-overlay { position: fixed; inset: 0; z-index: 9999; background: rgba(0,0,0,0.75); display: flex; align-items: center; justify-content: center; }
.fs-center { text-align: center; }
.fs-ball { font-size: 4rem; filter: drop-shadow(0 0 14px rgba(57,255,20,0.6)); animation: bounceY 0.9s ease-in-out infinite; }
.fs-text { margin-top: 1rem; font-family: 'Oswald', sans-serif; letter-spacing: 2px; color: #00f2ff; font-size: 1.2rem; animation: glowPulse 1.8s ease-in-out infinite; }
</style>
"""
