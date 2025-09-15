import streamlit as st
import pandas as pd
import http.client
import socket

st.set_page_config(page_title="RC Car App")

st.write("""
# Connect to RC Car!
""")


if "car_connected" not in st.session_state:
    st.session_state.car_connected = False
if "chosen_rc_car" not in st.session_state:
    st.session_state.chosen_rc_car = None
if "show_slider" not in st.session_state:
    st.session_state.show_slider = False


def scan_network(prefix="192.168.137.", start=200, end=254, port=80, timeout=0.5):
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

def findIPByHost(hostname):
    try:
        return socket.gethostbyname(hostname)
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
        #st.write("Error: ", e)
        st.write("Could not connect to RC car.")
        st.write("Make sure the RC car is connected to the wifi and the IP address is correct.")
        return False


if st.button('connect to rc car 1'):
    ip_rc1 = findIPByHost("rc1")
    if ip_rc1:
        if requestControl(ip_rc1):
            st.write("You can now control the RC car!")
            st.session_state.car_connected = True
        else:
            st.write("RC car did not allow connection.")
    else:
        st.write("Could not find IP for rc1. Make sure the hostname is correct and try again.")


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


if st.session_state.car_connected:
    if st.button('START'):
        st.session_state.show_slider = True

    if st.session_state.show_slider:
        speed = st.slider('Set speed', min_value=-10, max_value=10, value=0)
        st.write(f"Selected speed: {speed}")

        

