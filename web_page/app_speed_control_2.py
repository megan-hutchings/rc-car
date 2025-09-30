import streamlit as st
import pandas as pd
import http.client
import socket
import time

st.set_page_config(page_title="Speed Control")
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

hostname_list = ["PicoW","esp32s3-2ED890"]
selected_hostname = st.selectbox("Select RC Car Hostname:", hostname_list)

def findIPByHost(hostname):
    try:
        return socket.gethostbyname(hostname+".mshome.net")
    except socket.error as err:
        st.write(f"Error resolving hostname {hostname}: {err}")
        return None

def requestControl(ip):
    try: 
        connection = http.client.HTTPConnection(ip, 80, timeout=5)
    
        connection.request("GET", "/reqconnect")

        response = connection.getresponse()
        connection.close()
        st.write("Status: {} and reason: {}".format(response.status, response.reason))

        # Print the response body as text
        response_str = response.read().decode()
        st.write("rc allowed connection: ",response_str)
        if response_str == "yes":
            return True
        else:       
            return False

    except Exception as e:
        st.write("Could not connect to RC car.")
        st.write("Make sure the RC car is connected to the wifi and the IP address is correct.")
        return False

def requestStop(ip):
    st.write("Requesting RC car to stop...")
    st.write(st.session_state.chosen_rc_car_ip)
    try: 
        connection = http.client.HTTPConnection(ip, 80, timeout=5)
        connection.request("GET", "/reqstop")
        response = connection.getresponse()
        connection.close()
        st.write("Status: {} and reason: {}".format(response.status, response.reason))

        # Print the response body as text
        response_str = response.read().decode()
        st.write("run mode stop: ",response_str)
        if response_str == "yes":
            return True
        else:       
            return False

    except Exception as e:
        st.write("Could not connect to RC car.")
        st.write("Make sure the RC car is connected to the wifi and the IP address is correct.")
        return False




def requestStart(ip):
    st.write("Requesting RC car to start...")
    st.write(st.session_state.chosen_rc_car_ip)
    try: 
        connection = http.client.HTTPConnection(ip, 80, timeout=5)
        connection.request("GET", "/reqstart")
        response = connection.getresponse()
        connection.close()
        st.write("Status: {} and reason: {}".format(response.status, response.reason))

        # Print the response body as text
        response_str = response.read().decode()
        st.write("run mode started: ",response_str)
        if response_str == "yes":
            return True
        else:       
            return False

    except Exception as e:
        st.write("Could not connect to RC car.")
        st.write("Make sure the RC car is connected to the wifi and the IP address is correct.")
        return False
    

# def requestMoveServo(ip, direction):
#     st.write(f"Requesting RC car turn {direction}")
#     st.write(st.session_state.chosen_rc_car_ip)
#     try: 
#         connection = http.client.HTTPConnection(ip, 80, timeout=5)
#         connection.request("GET", "/reqchangeservo?dir="+direction)
#         response = connection.getresponse()
#         connection.close()
#         st.write("Status: {} and reason: {}".format(response.status, response.reason))

#         # Print the response body as text
#         response_str = response.read().decode()
#         st.write("pi confirmed change speed: ",response_str)
#         return True

#     except Exception as e:
#         st.write("Could not connect to RC car.")
#         st.write("Make sure the RC car is connected to the wifi and the IP address is correct.")
#         return False
    
def requestChangeSpeed(ip,speed):
    try:
        connection = http.client.HTTPConnection(st.session_state.chosen_rc_car_ip, 80, timeout=5)
        connection.request("GET", f"/reqchangespeed?speed={speed}")
        response = connection.getresponse()
        connection.close()
        st.write(f"Speed set to {speed}. Status: {response.status}, Reason: {response.reason}")
    except Exception as e:
        st.write("Failed to set speed:", e)

def requestMoveServo(ip,angle):
    try:
        connection = http.client.HTTPConnection(st.session_state.chosen_rc_car_ip, 80, timeout=5)
        connection.request("GET", f"/reqchangeservo?angle={angle}")
        response = connection.getresponse()
        connection.close()
        st.write(f"angle set to {angle}. Status: {response.status}, Reason: {response.reason}")
    except Exception as e:
        st.write("Failed to set angle:", e)



col1, col2 = st.columns(2)

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



if st.session_state.car_connected:
    if not st.session_state.running:
        st.header("Run Mode: Not Activated")
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
        st.header("Run Mode: Activated")
        # stop button
        if st.button('STOP'):
                st.write("Stopping")
                requestChangeSpeed(st.session_state.chosen_rc_car_ip,"1500")
                st.session_state["speed_slider"] = 1500  # Reset slider to 1500
                new_angle = 90
                requestMoveServo(st.session_state.chosen_rc_car_ip, new_angle)
                st.session_state.current_angle = new_angle

        # FWD/BWD
        speed = st.slider("Set Speed", min_value=1000, max_value=2000, value=1500, key="speed_slider") # speed is in us PWM

        # Track previous value to detect changes
        if "prev_speed" not in st.session_state:
            st.session_state.prev_speed = speed

        if speed != st.session_state.prev_speed:
            st.session_state.prev_speed = speed
            requestChangeSpeed(st.session_state.chosen_rc_car_ip,str(speed))

        

        #servo control
        max_angle = 180 #180
        min_angle = 0 #0
        col1, col2 = st.columns(2)

        with col1:
            if st.button("⬅️ LEFT"):
                new_angle = max(st.session_state.current_angle - 15, min_angle)
                requestMoveServo(st.session_state.chosen_rc_car_ip, new_angle)
                st.session_state.current_angle = new_angle


        with col2:
            if st.button("RIGHT ➡️"):
                new_angle = min(st.session_state.current_angle + 15, max_angle)
                requestMoveServo(st.session_state.chosen_rc_car_ip, new_angle)
                st.session_state.current_angle = new_angle











