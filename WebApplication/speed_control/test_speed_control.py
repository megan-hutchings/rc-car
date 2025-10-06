import streamlit as st
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from speed_control import speed_control_component

st.subheader("Component with constant args")

MIN_SPEED = 1000
STOP_SPEED = 1500
MAX_SPEED  = 2000
INCREMENT = 10
INTERVAL_MS = 100

num_clicks = speed_control_component(MAX_SPEED,MIN_SPEED,STOP_SPEED,INCREMENT,INTERVAL_MS)




st.markdown("Speed is %s" % int(num_clicks))