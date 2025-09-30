cloned https://github.com/streamlit/component-template.git


cd rc-car\learn_components\test\speed_button

1. set up npm
cd frontend
npm install  # only have to do this oncec- installs dependancies described in package.json
npm run start # runs the front end as a server (component like a little webpage)

2. in another terminal run 
pip install -e . to install dependancies
and
streamlit run test_speed_control.py
to run page
