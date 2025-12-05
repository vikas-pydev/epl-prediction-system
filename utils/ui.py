import streamlit as st
import time

def show_football_loader(message="Analyzing...", key="loader"):
    return None

def show_overlay_lottie(message=""):
    return st.empty()

def show_corner_bounce(duration=0.0):
    return None

def render_form_dots(seq: str):
    mapping = {"W": "win", "D": "draw", "L": "loss"}
    seq = [s.strip().upper() for s in seq.replace(",", "-").split("-") if s.strip()]
    html = "".join([f'<span class="form-dot {mapping.get(s, "draw")}"></span>' for s in seq[:5]])
    return html

def show_fullscreen_bounce(message: str, seconds: float = 3.2):
    holder = st.empty()
    with holder.container():
        st.markdown(f"""
        <div class="fs-overlay">
            <div class="fs-center">
                <div class="fs-ball">⚽</div>
                <div class="fs-text">{message}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    time.sleep(seconds)
    holder.empty()
