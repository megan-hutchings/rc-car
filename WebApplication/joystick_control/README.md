https://github.com/leocorp96/streamlit-joystick

pip install streamlit-joystick

gives an XY value for the joystick control
- nice but doesn't have the 'press down duration characteristic'
- could add something similar as a custom component





All available streamlit options https://cheat-sheet.streamlit.app/




# Custom Component

1. set up npm
cd frontend
npm install  # only have to do this oncec- installs dependancies described in package.json
npm run start # runs the front end as a server (component like a little webpage)

2. in another terminal run 
pip install -e . to install dependancies
and
streamlit run test_joystick.py
to run page