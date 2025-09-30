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
if "chosen_rc_car_ip" not in st.session_state:
    st.session_state.chosen_rc_car_ip = None
if "running" not in st.session_state:
    st.session_state.running = False
if "speed" not in st.session_state:
    st.session_state.speed = 0
if "prev_speed" not in st.session_state:
    st.session_state.prev_speed = 0
if "prev_time" not in st.session_state:
    st.session_state.prev_time = time.time()

# search network for all connected devices
def scan_network(prefix="192.168.137.", start=1, end=254, port=80, timeout=0.1):
    devices_list = []
    for i in range(start, end + 1):
        ip = f"{prefix}{i}"
        try:
            sock = socket.create_connection((ip, port), timeout=timeout)
            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except Exception:
                hostname = "Unknown"

            devices_list.append({"IP": ip, "Hostname": hostname})
            sock.close()
        except Exception:
            pass
    return pd.DataFrame(devices_list)

#Hostname selection of RC car - not currently working
def findIPByHost(hostname):
    try:
        return socket.gethostbyname(hostname+".mshome.net")
    except socket.error as err:
        st.write(f"Error resolving hostname {hostname}: {err}")
        return None


# HTTP clients
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

def requestChangeSpeed(ip):
    st.write(ip)
    try: 
        connection = http.client.HTTPConnection(ip, 80, timeout=5)
        #requests.get(url, headers=head, data=json.dumps({"user_id": 436186}))
    
        connection.request("GET", "/reqchangespeed?speed="+str(st.session_state.speed))

        response = connection.getresponse()
        connection.close()
        st.write("Status: {} and reason: {}".format(response.status, response.reason))

        # Print the response body as text
        response_str = response.read().decode()
        st.write("arduino recieved speed change: ",response_str)
        if response_str == "success":
            return True
        else:       
            return False
        
    except Exception as e:
        #st.write("Error: ", e)
        st.write("Could not connect to RC car.")
        st.write("Make sure the RC car is connected to the wifi and the IP address is correct.")
        return False

# calculate speed based on button press
def calcSpeed(direction):
    current_time = time.time()
    elapsed_time = current_time - st.session_state.prev_time

    if direction == "FWD":
        speed = min(st.session_state.speed + 1, 10)  # Accelerate forward
    elif direction == "REV":
        speed = max(st.session_state.speed - 1, -10)  # Accelerate backward
    st.session_state.prev_time = current_time

    return speed



# Hostname selection of RC car - not currently working
if st.button('connect to rc car 2 -pi'):
    st.session_state.chosen_rc_car_ip = findIPByHost("PicoW")
    st.write(f"IP found : {st.session_state.chosen_rc_car_ip}") 
    if st.session_state.chosen_rc_car_ip:
        if requestControl(st.session_state.chosen_rc_car_ip):
            st.write("You can now control the RC car!")
            st.session_state.car_connected = True
        else:
            st.write("RC car did not allow connection.")
            st.session_state.car_connected = False
    else:
        st.write("Could not find IP for rc2_pi. Make sure the hostname is correct and try again.")

if st.button('Find all rc cars on the network'):
    st.write('Scanning for RC cars on the network...')
    devices = scan_network()
    if not devices.empty:
        st.write("Found devices:")
        st.table(devices)
        st.session_state.chosen_rc_car_ip = st.selectbox("Select an RC Car IP:", devices.IP)
        st.write(f"You selected: {st.session_state.chosen_rc_car_ip}")


        st.write(f'Sending request to RC car at {st.session_state.chosen_rc_car_ip}!')
        if requestControl(st.session_state.chosen_rc_car_ip):
            st.write("You can now control the RC car!")
            st.session_state.car_connected = True
        else:
            st.write("RC car did not allow connection.")
            st.session_state.car_connected = False
    else:
        st.write("No devices found.")
        st.session_state.chosen_rc_car_ip = None

#st.session_state.car_connected = True



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


    if st.session_state.running:
        # RC car control buttons
        #FWD
        row1 = st.columns(3)
        with row1[1]:
            if st.button('W', key="w_btn"):
                st.write(f'W clicked!, moving forward at speed {st.session_state.speed}')
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

        # TODO: loop to automatically slow down the speed if it hasn't been clicked

        # loop to check for speed changes to send to arduino
        if st.session_state.speed != st.session_state.prev_speed:
            # send new speed to arduino
            st.write("updating speed to: ", st.session_state.speed)
            requestChangeSpeed(st.session_state.chosen_rc_car_ip)
            st.session_state.prev_speed = st.session_state.speed


        # show speed gague
        streamviz.gauge(gVal=st.session_state.speed, gSize="LRG", 
        gTitle="Speed", gMode="gauge+number",
        grLow=3, grMid=6, gcLow="red",
        gcMid="orange", gcHigh="green", arTop=10)


        


