"""
Custom CSS styling for the Streamlit app.
"""

def get_custom_css():
    """Return custom CSS for beautiful UI styling."""
    return """
<style>
/* Import Fonts */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@300;400;600&display=swap');

/* Global Variables */
:root {
    --primary-color: #00f2ff;
    --secondary-color: #ff00ff;
    --neon-green: #00f2ff;
    --bg-dark: #0f172a;
    --bg-darker: #020617;
    --glass-bg: rgba(255, 255, 255, 0.05);
    --glass-border: rgba(255, 255, 255, 0.1);
    --text-primary: #ffffff;
    --text-secondary: #94a3b8;
}

/* Keyframes */
@keyframes gradientMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translate3d(0, 30px, 0);
    }
    to {
        opacity: 1;
        transform: translate3d(0, 0, 0);
    }
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}

@keyframes pulse-glow {
    0% { box-shadow: 0 0 0 0 rgba(0, 242, 255, 0.4); }
    70% { box-shadow: 0 0 0 10px rgba(0, 242, 255, 0); }
    100% { box-shadow: 0 0 0 0 rgba(0, 242, 255, 0); }
}

@keyframes scanline {
    0% { transform: translateY(-100%); }
    100% { transform: translateY(100%); }
}

@keyframes shimmer {
    0% { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
}

/* Main Container & Background */
.stApp {
    background-color: var(--bg-dark);
    background-image: 
        radial-gradient(circle at 0% 0%, rgba(118, 75, 162, 0.2) 0%, transparent 50%),
        radial-gradient(circle at 100% 0%, rgba(102, 126, 234, 0.2) 0%, transparent 50%),
        radial-gradient(circle at 100% 100%, rgba(255, 0, 255, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 0% 100%, rgba(0, 242, 255, 0.1) 0%, transparent 50%);
    background-size: 100% 100%;
    background-attachment: fixed;
    color: var(--text-primary);
    font-family: 'Inter', sans-serif;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif;
    color: var(--text-primary);
    font-weight: 700;
    letter-spacing: -0.02em;
}

h1 {
    font-size: 4rem;
    background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 30px rgba(255,255,255,0.1);
    margin-bottom: 1.5rem;
    text-transform: uppercase;
    animation: fadeInUp 0.8s ease-out;
}

/* Glassmorphism Cards */
.glass-card {
    background: var(--glass-bg);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--glass-border);
    border-radius: 24px;
    padding: 2rem;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.8s ease-out backwards;
}

.glass-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(255, 255, 255, 0.05),
        transparent
    );
    transition: 0.5s;
}

.glass-card:hover::before {
    left: 100%;
}

.glass-card:hover {
    transform: translateY(-5px) scale(1.02);
    border-color: rgba(255, 255, 255, 0.3);
    box-shadow: 
        0 20px 40px rgba(0, 0, 0, 0.3),
        0 0 20px rgba(0, 242, 255, 0.2);
}

/* Staggered Animations */
.stagger-1 { animation-delay: 0.1s; }
.stagger-2 { animation-delay: 0.2s; }
.stagger-3 { animation-delay: 0.3s; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
    backdrop-filter: blur(10px);
    border: 1px solid var(--glass-border);
    color: white;
    border-radius: 12px;
    padding: 0.75rem 1.5rem;
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    width: 100%;
    position: relative;
    overflow: hidden;
}

.stButton > button:hover {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    border-color: transparent;
    transform: translateY(-2px);
    box-shadow: 0 0 25px rgba(0, 242, 255, 0.5);
}

.stButton > button:active {
    transform: translateY(1px);
}

/* Enter Arena Button */
.enter-arena-btn {
    background: rgba(0, 242, 255, 0.1);
    border: 2px solid var(--neon-green);
    color: var(--neon-green);
    padding: 1rem 3rem;
    font-size: 1.5rem;
    font-weight: 700;
    border-radius: 8px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    transition: all 0.3s ease;
    box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
    display: inline-block;
    text-decoration: none;
    animation: pulse-glow 2s infinite;
}

.enter-arena-btn:hover {
    background: var(--neon-green);
    color: #000;
    box-shadow: 0 0 50px rgba(0, 242, 255, 0.8);
    transform: scale(1.05);
}

/* Versus Screen */
.versus-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2rem;
    margin: 3rem 0;
    animation: fadeInUp 1s ease-out;
}

.team-logo {
    width: 150px;
    height: 150px;
    filter: drop-shadow(0 0 20px rgba(255,255,255,0.2));
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.team-logo:hover {
    transform: scale(1.15) rotate(5deg);
    filter: drop-shadow(0 0 40px rgba(255,255,255,0.6));
}

.vs-badge {
    font-size: 4rem;
    font-weight: 900;
    font-style: italic;
    background: linear-gradient(180deg, #fff 0%, #94a3b8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 20px rgba(0, 242, 255, 0.5);
    animation: float 4s ease-in-out infinite;
}

/* Scoreboard */
.scoreboard {
    background: rgba(0, 0, 0, 0.8);
    border: 2px solid var(--neon-green);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 0 50px rgba(0, 242, 255, 0.1);
    margin: 2rem 0;
    animation: fadeInUp 0.8s ease-out;
}

.score-display {
    font-family: 'Courier New', monospace;
    font-size: 5rem;
    font-weight: 700;
    color: #fff;
    text-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
}

/* Inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background-color: rgba(0, 0, 0, 0.2);
    border: 1px solid var(--glass-border);
    color: white;
    border-radius: 12px;
    transition: all 0.3s ease;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stSelectbox > div > div:focus-within {
    border-color: var(--primary-color);
    box-shadow: 0 0 20px rgba(0, 242, 255, 0.3);
    background-color: rgba(0, 0, 0, 0.4);
    transform: translateY(-2px);
}

/* Widget Labels */
.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stSlider label {
    color: var(--text-primary) !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    text-shadow: 0 0 10px rgba(0, 0, 0, 0.5) !important;
}

/* General Text Visibility */
p, li, span {
    color: var(--text-primary);
}

/* Small text in widgets */
.stNumberInput div[data-testid="stMarkdownContainer"] p {
    color: var(--text-primary) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: rgba(15, 17, 42, 0.85);
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
}

[data-testid="stSidebar"]:hover {
    box-shadow: 0 0 50px rgba(0, 242, 255, 0.1);
}

/* Sidebar Navigation Buttons */
[data-testid="stSidebar"] button {
    background: transparent !important;
    border: 1px solid transparent !important;
    color: rgba(255, 255, 255, 0.7) !important;
    text-align: left !important;
    padding-left: 1rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

[data-testid="stSidebar"] button:hover {
    background: linear-gradient(90deg, rgba(0, 242, 255, 0.1) 0%, transparent 100%) !important;
    border-left: 3px solid var(--primary-color) !important;
    color: white !important;
    padding-left: 1.5rem !important;
    text-shadow: 0 0 10px var(--primary-color);
}

/* Back Button */
.back-btn-container {
    position: fixed;
    top: 1rem;
    left: 1rem;
    z-index: 999;
}

/* Metrics */
[data-testid="stMetricValue"] {
    font-family: 'Outfit', sans-serif;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.5rem;
    font-weight: 700;
    animation: fadeInUp 0.5s ease-out;
}

/* Animation Classes */
.float-animation {
    animation: float 6s ease-in-out infinite;
}

.pulse-glow {
    animation: pulse-glow 2s infinite;
}

/* Hide Streamlit Elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {background: transparent !important;}


/* Custom Scrollbar */
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
</style>

"""
