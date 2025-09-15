import streamlit as st
import pandas as pd
import streamlit_shortcuts as shrt

st.set_page_config(page_title="RC Control")

st.write("""
# RC Web Control
Click to drive
""")

# Row 1: Button in position 2
row1 = st.columns(3)
with row1[1]:
    if st.button('W', key="w_btn"):
        st.write('W clicked!')

# Row 2: Buttons in positions 1 and 3
row2 = st.columns(3)
with row2[0]:
    if st.button('A', key="a_btn"):
        st.write('A clicked!')
with row2[2]:
    if st.button('D', key="d_btn"):
        st.write('D clicked!')

# Row 3: Button in position 2
row3 = st.columns(3)
with row3[1]:
    if st.button('S', key="s_btn"):
        st.write('S clicked!')

shrt.add_shortcuts(
    w_btn=["arrowup", "w"],
    a_btn=["arrowleft", "a"],
    d_btn=["arrowright", "d"],
    s_btn=["arrowdown", "s"]
)