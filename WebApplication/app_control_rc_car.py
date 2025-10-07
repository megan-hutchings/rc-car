import streamlit as st
import pandas as pd
import datetime
import socket
from rc_http_control import requestControl, requestStop, requestStart, requestChangeSpeed, requestMoveServo, requestChangeSound  
from speed_control import speed_control_component
from direction_control import dir_control_component
from joystick_control import joystick_control_component
import time

st.set_page_config(page_title="RC Car Controller")
st.write("""
# RC CAR APP!!
""")


if "car_connected" not in st.session_state:
    st.session_state.car_connected = False
if "chosen_rc_car_ip" not in st.session_state:
    st.session_state.chosen_rc_car_ip = None
if "running" not in st.session_state:
    st.session_state.running = False
if "current_angle" not in st.session_state:
    st.session_state.current_angle = 90
if "prev_speed" not in st.session_state:
    st.session_state.prev_speed = 1500
if "sound" not in st.session_state:
    st.session_state.sound = False
if "current_sound" not in st.session_state:
    st.session_state.current_sound = "OFF"


hostname_list = ["PicoW","esp32s3-2ED890"]
selected_hostname = st.selectbox("Select RC Car Hostname:", hostname_list)

# #ESC
# MIN_SPEED = 1200
# STOP_SPEED = 1500
# MAX_SPEED  = 1700 #2000
# ESC_INCREMENT = 50
# ESC_INTERVAL_MS = 500 #100 

# #SERVO
# MIN_POS = 30 #30
# STOP_POS = 90
# MAX_POS  = 150 #150
# INCREMENT = 10
# INTERVAL_MS = 100


MIN_SPEED = 1000
STOP_SPEED = 1500
MAX_SPEED  = 2000
INCREMENT_SPEED = 10

MIN_DIR = 30 #0
CENTRE_DIR = 90
MAX_DIR  = 150 #180
INCREMENT_DIR = 10
SPEED_DEADZONE = 100 # range around 1500 where the car does not move - motor/set up specific

INTERVAL_MS = 200


def findIPByHost(hostname):
    try:
        return socket.gethostbyname(hostname+".mshome.net")
    except socket.error as err:
        st.write(f"Error resolving hostname {hostname}: {err}")
        return None

# Connection Functionality
col1, col2, col3 = st.columns(3)

with col1:
    if st.button('Click to connect to car'):
        st.session_state.chosen_rc_car_ip = findIPByHost(selected_hostname)
        st.write(f"IP for {selected_hostname} found : {st.session_state.chosen_rc_car_ip}") 
        if st.session_state.chosen_rc_car_ip:
            if requestControl(st.session_state.chosen_rc_car_ip):
                st.write("You can now control the RC car!")
                st.session_state.car_connected = True
            else:
                st.write("RC car did not allow connection.")
                st.session_state.car_connected = False
        else:
            st.write(f"Could not find IP for  {selected_hostname}. Make sure the hostname is correct and try again.")

with col2:
    if st.button('Disconnect car from PC'):
        success  = requestStop(st.session_state.chosen_rc_car_ip)
        if success:
            st.write("RC car was disconnected!")
        else:
            st.write("RC car did not disconnect.")
        st.session_state.running = False
        st.session_state.speed = 0
        st.session_state.car_connected = False
with col3:
    if st.toggle("SOUND", value=False):
        st.session_state.sound = True
    else:
        st.session_state.sound = False
        if st.session_state.current_sound != "OFF":
            print("stopping music")
            requestChangeSound(st.session_state.chosen_rc_car_ip, "OFF")
            st.session_state.current_sound = "OFF"


# Driving Functionality
if st.session_state.car_connected:
    if not st.session_state.running:
        if st.button('Click To Start Car'):
            success  = requestStart(st.session_state.chosen_rc_car_ip)
            #success = True
            if success:
                st.write("RC car started in run mode!")
                st.session_state.running = True
            else:
                st.write("RC car did not start.")
    #esc control            
    if st.session_state.running:
        if st.session_state.sound:
            if st.session_state.current_sound == "OFF":
                print("starting music")
                requestChangeSound(st.session_state.chosen_rc_car_ip, "DARTHVADER")
                st.session_state.current_sound = "DARTHVADER"


        if st.toggle("Drag Control", value=False):
            st.subheader("DRAG CONTROL")
            speed,angle = joystick_control_component(MAX_DIR,
                                                MIN_DIR,
                                                CENTRE_DIR,
                                                MAX_SPEED,
                                                MIN_SPEED,
                                                STOP_SPEED,
                                                SPEED_DEADZONE,
                                                INTERVAL_MS)
            
            if speed != st.session_state.prev_speed:
                st.session_state.prev_speed = speed
                requestChangeSpeed(st.session_state.chosen_rc_car_ip,str(speed))
            if angle != st.session_state.current_angle:
                print("angle:",angle)
                requestMoveServo(st.session_state.chosen_rc_car_ip, angle)
                st.session_state.current_angle = angle

            st.markdown("Speed is %s" % int(speed))
            st.markdown("Dir is %s" % int(angle))


        else:
            #FWD/BWD
            Acceleration = st.slider("Set FWD Speed (1-10)", min_value=1, max_value=10, value=5, key="speed_slider") # speed is in us PWM
            MAX_SPEED = 1500 + Acceleration*50

            speed = speed_control_component(MAX_SPEED,MIN_SPEED,STOP_SPEED,INCREMENT_SPEED,INTERVAL_MS)
            print(datetime.datetime.now())
            print("speed:",speed)
            print("prev_speed:",st.session_state.prev_speed)

            if speed != st.session_state.prev_speed:
                st.session_state.prev_speed = speed
                requestChangeSpeed(st.session_state.chosen_rc_car_ip,str(speed))
                # if speed < 1500:
                #     if st.session_state.current_sound != "BWD":
                #         print("changing to BWD")
                #         requestChangeSound(st.session_state.chosen_rc_car_ip, "BWD")
                #         st.session_state.current_sound = "BWD"
                # else:
                #     if st.session_state.current_sound != "DARTHVADER":
                #         print("changing to DARTHVADER")
                #         requestChangeSound(st.session_state.chosen_rc_car_ip, "DARTHVADER")
                #         st.session_state.current_sound = "DARTHVADER"

            angle = dir_control_component(MAX_DIR,MIN_DIR,CENTRE_DIR,INCREMENT_DIR,INTERVAL_MS)
            if angle != st.session_state.current_angle:
                print("angle:",angle)
                requestMoveServo(st.session_state.chosen_rc_car_ip, angle)
                st.session_state.current_angle = angle

            st.header(f"Current Speed:{st.session_state.prev_speed} Current DIR:{st.session_state.current_angle}")


        