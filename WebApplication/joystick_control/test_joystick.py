

import streamlit as st
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from joystick_control import joystick_control_component

from st_joystick import st_joystick


value = st_joystick()
st.write(value)




st.subheader("Component with constant args")

MIN_SPEED = 1000
STOP_SPEED = 1500
MAX_SPEED  = 2000

MIN_DIR = 0
CENTRE_DIR = 90
MAX_DIR  = 180
SPEED_DEADZONE = 100 # range around 1500 where the car does not move - motor/set up specific
INTERVAL_MS = 200

speed,dir = joystick_control_component(MAX_DIR,
                                       MIN_DIR,
                                       CENTRE_DIR,
                                       MAX_SPEED,
                                       MIN_SPEED,
                                       STOP_SPEED,
                                       SPEED_DEADZONE,
                                       INTERVAL_MS)


st.markdown("Speed is %s" % int(speed))
st.markdown("Dir is %s" % int(dir))

