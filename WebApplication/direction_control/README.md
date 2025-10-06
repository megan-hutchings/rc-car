cloned https://github.com/streamlit/component-template.git




1. set up npm
cd frontend
npm install  # only have to do this oncec- installs dependancies described in package.json
npm run start # runs the front end as a server (component like a little webpage)

2. in another terminal run 
pip install -e . to install dependancies
and
streamlit run test_dir_control.py
to run page



1. set up npm (dev mode)

```
cd speed_control\frontend
npm install  
```
Only have to do this once, it will install all the dependancies described in package.json
2. start front end component
```
npm run start 
```
Runs the front end as a server (component acts like a little webpage)

3. install additional dependancies for frontend, open a new terminal
```
cd speed_control\
pip install -e . 
```
installs dependencies in setup.py

at the moment you also need to do this at te Web Application level for the rc_http_control package. TODO: intergrate steup.py files
```
cd rc_http_control\
pip install -e . 
```