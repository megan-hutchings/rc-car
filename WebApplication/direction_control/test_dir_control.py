import streamlit as st
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from direction_control import dir_control_component

st.subheader("Test Dir Control Component")

MIN_POS = 0
STOP_POS = 90
MAX_POS  = 180
INCREMENT = 10
INTERVAL_MS = 100

angle = dir_control_component(MAX_POS,MIN_POS,STOP_POS,INCREMENT,INTERVAL_MS)




st.markdown("Angle is %s" % int(angle))