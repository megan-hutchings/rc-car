import streamlit as st
import pandas as pd
import http.client
import socket
import time

st.set_page_config(page_title="RC Car App")

st.write("""
# Connect to RC Car!
""")

if "car_connected" not in st.session_state:
    st.session_state.car_connected = False
if "chosen_rc_car_ip" not in st.session_state:
    st.session_state.chosen_rc_car_ip = None
if "running" not in st.session_state:
    st.session_state.running = False


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

def requestMove(ip, direction):
    st.write(f"Requesting RC car to {direction}")
    st.write(st.session_state.chosen_rc_car_ip)
    try: 
        connection = http.client.HTTPConnection(ip, 80, timeout=5)
        connection.request("GET", "/reqchangespeed?dir="+direction)
        response = connection.getresponse()
        connection.close()
        st.write("Status: {} and reason: {}".format(response.status, response.reason))

        # Print the response body as text
        response_str = response.read().decode()
        st.write("pi confirmed change speed: ",response_str)
        return True

    except Exception as e:
        st.write("Could not connect to RC car.")
        st.write("Make sure the RC car is connected to the wifi and the IP address is correct.")
        return False
    
def requestMoveServo(ip, direction):
    st.write(f"Requesting RC car turn {direction}")
    st.write(st.session_state.chosen_rc_car_ip)
    try: 
        connection = http.client.HTTPConnection(ip, 80, timeout=5)
        connection.request("GET", "/reqchangeservo?dir="+direction)
        response = connection.getresponse()
        connection.close()
        st.write("Status: {} and reason: {}".format(response.status, response.reason))

        # Print the response body as text
        response_str = response.read().decode()
        st.write("pi confirmed change speed: ",response_str)
        return True

    except Exception as e:
        st.write("Could not connect to RC car.")
        st.write("Make sure the RC car is connected to the wifi and the IP address is correct.")
        return False


if st.button('Select Car'):
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


if st.button('Disconnect'):
    success  = requestStop(st.session_state.chosen_rc_car_ip)
    if success:
        st.write("RC car was disconnected!")
        st.session_state.running = True
    else:
        st.write("RC car did not disconnect.")
    st.session_state.running = False
    st.session_state.speed = 0
    st.session_state.car_connected = False



if st.session_state.car_connected:
    if not st.session_state.running:
        if st.button('START'):
            success  = requestStart(st.session_state.chosen_rc_car_ip)
            #success = True
            if success:
                st.write("RC car started in run mode!")
                st.session_state.running = True
            else:
                st.write("RC car did not start.")
    #esc control            
    if st.session_state.running:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button('FWD'):
                st.write("Moving Forward")
                requestMove(st.session_state.chosen_rc_car_ip, 'FWD')
                # Add your FWD logic here
        with col2:
            if st.button('STOP'):
                st.write("Stopping")
                requestMove(st.session_state.chosen_rc_car_ip, 'STOP')
                # Add your STOP logic here
        with col3:
            if st.button('BWD'):
                st.write("Moving Backward")
                requestMove(st.session_state.chosen_rc_car_ip, 'BWD')
                # Add your BWD logic here


        #servo control
        col1, col2 = st.columns(2)

        with col1:
            if st.button("⬅️ LEFT"):
                requestMoveServo(st.session_state.chosen_rc_car_ip, 'LEFTSTART')
                time.sleep(0.2)
                requestMoveServo(st.session_state.chosen_rc_car_ip, 'LEFTSTOP')

        with col2:
            if st.button("RIGHT ➡️"):
                requestMoveServo(st.session_state.chosen_rc_car_ip, 'RIGHTSTART')
                time.sleep(0.2)
                requestMoveServo(st.session_state.chosen_rc_car_ip, 'RIGHTSTOP')

        st.markdown("""
        <style>
        div.stButton > button {
            height: 150px;
            width: 200px;
            font-size: 32px;
            margin: 10px;
        }
        </style>
        """, unsafe_allow_html=True)
        
