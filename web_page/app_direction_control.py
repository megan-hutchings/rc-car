import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
import streamviz


st.set_page_config(page_title="Direction Control")
st.write("""
# Control Direction!
""")

if "current_angle" not in st.session_state:
    st.session_state.current_angle = 90
if "button_held" not in st.session_state:
    st.session_state.button_held = None



#servo control
max_angle = 180 #180
min_angle = 0 #0
col1, col2 = st.columns(2)

with col1:
    if st.button("⬅️ LEFT"):
        new_angle = max(st.session_state.current_angle - 15, min_angle)
        #requestMoveServo(st.session_state.chosen_rc_car_ip, new_angle)
        st.session_state.current_angle = new_angle


with col2:
    if st.button("RIGHT ➡️"):
        new_angle = min(st.session_state.current_angle + 15, max_angle)
        #requestMoveServo(st.session_state.chosen_rc_car_ip, new_angle)
        st.session_state.current_angle = new_angle

st.write(f"Current Angle: {st.session_state.current_angle}°")


# --- Buttons ---
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("◀️ Left", key="left"):
        st.session_state.button_held = "left"
with col3:
    if st.button("Right ▶️", key="right"):
        st.session_state.button_held = "right"

# Stop button or auto stop when no click
if not any([st.session_state.get("left"), st.session_state.get("right")]):
    if st.session_state.button_held:
        st.session_state.button_held = None

# --- Auto-refresh every 100ms ---
if st.session_state.button_held:
    st_autorefresh(interval=100, limit=None, key="auto_refresh")

    # Adjust speed
    if st.session_state.button_held == "right":
        st.session_state.current_angle = max(st.session_state.current_angle - 15, min_angle)
    elif st.session_state.button_held == "left":
        st.session_state.current_angle = min(st.session_state.current_angle + 15, max_angle)


# --- Display gauge ---
streamviz.gauge(
    gVal=st.session_state.current_angle,
    gSize="LRG",
    gTitle="Angle",
    gMode="gauge+number",
    grLow=3,
    grMid=6,
    gcLow="red",
    gcMid="orange",
    gcHigh="green",
    arTop=10,
)