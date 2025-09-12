import streamlit as st
import pandas as pd
import http.client

st.set_page_config(page_title="Arduino App")

st.write("""
# App For Talking To Arduino Over Wifi!*
""")

if st.button('connect to arduino'):
    st.write('Sending request to arduino!')

    try: 
        connection = http.client.HTTPConnection("192.168.137.152", 80,timeout = 5)
    
        connection.request("GET", "/")

        response = connection.getresponse()
        st.write("Status: {} and reason: {}".format(response.status, response.reason))

        # Print the response body as text
        st.write(response.read().decode())

        connection.close()
    except Exception as e:
        #st.write("Error: ", e)
        st.write("Could not connect to arduino.")
        st.write("Make sure the arduino is connected to the wifi and the IP address is correct.")
    
