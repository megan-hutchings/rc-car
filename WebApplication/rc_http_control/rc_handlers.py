import streamlit as st
import http.client


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




#OFF
#BWD
#DARTHVADER
def requestChangeSound(ip,sound):
    try:
        connection = http.client.HTTPConnection(st.session_state.chosen_rc_car_ip, 80, timeout=5)
        connection.request("GET", f"/reqchangesound?sound={sound}")
        response = connection.getresponse()
        connection.close()
        st.write(f"Speed set to {sound}. Status: {response.status}, Reason: {response.reason}")
    except Exception as e:
        st.write("Failed to set sound:", e)