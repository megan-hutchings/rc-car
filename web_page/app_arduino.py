import streamlit as st
import pandas as pd
import http.client

st.set_page_config(page_title="Arduino App")

st.write("""
# App For Talking To Arduino Over Wifi!*
""")

if st.button('connect to arduino'):
    st.write('Sending request to arduino!')

    connection = http.client.HTTPConnection("192.168.137.191", 80)
    connection.request("GET", "/")

    response = connection.getresponse()
    st.write("Status: {} and reason: {}".format(response.status, response.reason))

    # Print the response body as text
    st.write(response.read().decode())

    connection.close()