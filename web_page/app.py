import streamlit as st
import pandas as pd

st.set_page_config(page_title="My First App")

st.write("""
# My first app
Hello *world!*
""")

if st.button('Click Me'):
    st.write('Button was clicked!')