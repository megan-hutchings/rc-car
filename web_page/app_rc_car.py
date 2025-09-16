import streamlit as st
import pandas as pd
import http.client
import socket
import streamlit_shortcuts as shrt
import streamviz
import time

st.set_page_config(page_title="RC Car App")

st.write("""
# Connect to RC Car!
""")


if "car_connected" not in st.session_state:
    st.session_state.car_connected = False
if "chosen_rc_car" not in st.session_state:
    st.session_state.chosen_rc_car = None
if "show_control_buttons" not in st.session_state:
    st.session_state.show_control_buttons = False
if "speed" not in st.session_state:
    st.session_state.speed = 0
if "prev_speed" not in st.session_state:
    st.session_state.prev_speed = 0
if "prev_time" not in st.session_state:
    st.session_state.prev_time = time.time()



def scan_network(prefix="192.168.137.", start=1, end=254, port=80, timeout=0.1):
    found_devices = []
    for i in range(start, end + 1):
        ip = f"{prefix}{i}"
        try:
            sock = socket.create_connection((ip, port), timeout=timeout)
            found_devices.append(ip)
            sock.close()
        except Exception:
            pass
    return found_devices

# def findIPByHost(hostname):
#     try:
#         return socket.gethostbyname(hostname)
#     except socket.error as err:
#         st.write(f"Error resolving hostname {hostname}: {err}")
#         return None

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
        #st.write("Error: ", e)
        st.write("Could not connect to RC car.")
        st.write("Make sure the RC car is connected to the wifi and the IP address is correct.")
        return False
    
def changeSpeed(ip):
    try: 
        connection = http.client.HTTPConnection(ip, 80, timeout=5)
        #requests.get(url, headers=head, data=json.dumps({"user_id": 436186}))
    
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
        #st.write("Error: ", e)
        st.write("Could not connect to RC car.")
        st.write("Make sure the RC car is connected to the wifi and the IP address is correct.")
        return False

# if st.button('connect to rc car 1'):
#     ip_rc1 = findIPByHost("rc1")
#     if ip_rc1:
#         if requestControl(ip_rc1):
#             st.write("You can now control the RC car!")
#             st.session_state.car_connected = True
#         else:
#             st.write("RC car did not allow connection.")
#     else:
#   
#      st.write("Could not find IP for rc1. Make sure the hostname is correct and try again.")

def calcSpeed(direction):
    current_time = time.time()
    elapsed_time = current_time - st.session_state.prev_time

    if direction == "FWD":
        speed = min(st.session_state.speed + 1, 10)  # Accelerate forward
    elif direction == "REV":
        speed = max(st.session_state.speed - 1, -10)  # Accelerate backward
    st.session_state.prev_time = current_time

    return speed

# def calcSpeed(direction):
#     current_time = time.time()
#     elapsed_time = current_time - st.session_state.prev_time

#     if direction == "FWD":
#         speed = min(st.session_state.speed + elapsed_time * 2, 10)  # Accelerate forward
#     elif direction == "REV":
#         speed = max(st.session_state.speed - elapsed_time * 2, -10)  # Accelerate backward
#     else:
#         # Gradually slow down to 0 if no direction is pressed
#         if st.session_state.speed > 0:
#             speed = max(st.session_state.speed - elapsed_time * 2, 0)
#         elif st.session_state.speed < 0:
#             speed = min(st.session_state.speed + elapsed_time * 2, 0)
#         else:
#             speed = 0

#     st.session_state.prev_time = current_time

#     return speed




if st.button('find all rc cars on the network'):
    st.write('Scanning for RC cars on the network...')
    devices = scan_network()
    if devices:
        st.write("Found devices:")
        st.write(devices)
        st.chosen_rc_car = st.selectbox("Select an RC Car IP:", devices)
        st.write(f"You selected: {st.chosen_rc_car}")

        st.write(f'Sending request to RC car at {st.chosen_rc_car}!')
        if requestControl(st.chosen_rc_car):
            st.write("You can now control the RC car!")
            st.session_state.car_connected = True
        else:
            st.write("RC car did not allow connection.")
            st.session_state.car_connected = False
    else:
        st.write("No devices found.")
        chosen_rc_car = None


st.session_state.car_connected = True

if st.session_state.car_connected:
    if st.button('START'):
        st.session_state.show_control_buttons = True

    if st.session_state.show_control_buttons:

        # could select speed using a gague
        # st.session_state.speed = st.slider('Set speed', min_value=-10, max_value=10, value=0,key="speed_slider")
        # st.write(f"Selected speed: {st.session_state.speed}")
        # send speed command

        # RC car control buttons
        #FWD
        row1 = st.columns(3)
        with row1[1]:
            if st.button('W', key="w_btn"):
                st.write(f'W clicked!, moving forward at speed {st.session_state.speed}')
                print("w")
                st.session_state.speed = calcSpeed("FWD")
        #LEFT, RIGHT
        row2 = st.columns(3)
        with row2[0]:
            if st.button('A', key="a_btn"):
                st.write('A clicked!')
        with row2[2]:
            if st.button('D', key="d_btn"):
                st.write('D clicked!')

        #REV
        row3 = st.columns(3)
        with row3[1]:
            if st.button('S', key="s_btn"):
                st.write('S clicked!')
                st.session_state.speed = calcSpeed("REV")

        shrt.add_shortcuts(
            speed_slider=["space", "shift+space:left"],
            w_btn=["arrowup", "w"],
            a_btn=["arrowleft", "a"],
            d_btn=["arrowright", "d"],
            s_btn=["arrowdown", "s"]
        )

        # loop to automatically slow down the speed if it hasn't been clicked

        # loop to check for speed changes to send to arduino
        if st.session_state.speed != st.session_state.prev_speed:
            # send new speed to arduino
            st.write("updating speed to: ", st.session_state.speed)
            st.session_state.prev_speed = st.session_state.speed

        # show speed gague
        streamviz.gauge(gVal=st.session_state.speed, gSize="LRG", 
        gTitle="Speed", gMode="gauge+number",
        grLow=3, grMid=6, gcLow="red",
        gcMid="orange", gcHigh="green", arTop=10)



