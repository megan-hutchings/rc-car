
WEB APPLICATION FOR RC CAR

# STEP 0: Load Arduino Sketch onto car Pi/Arduino
1. in the arduino IDE compile and upload the sketch to the pi, checking the hotspot username and password matches the one set on your hotspot
2. Set up hotspot on windows through Settings>Network & internet>Mobile hotpot
3. when the code is loaded onto the pi it will automatically try to connect to the hotspot. the LED on the board will light up when it is connected and you can also check the connection in the mobile hotspot page in settings. If the board is having difficulties connecting you can open the serial monitor in the arduino IDE and check the logs (pi will need to be connected to the PC via USB for this to work)

# STEP 1: Set Up Frontend Components (Custom Buttons)

## Do Once
0. install Node.js
https://docs.streamlit.io/develop/concepts/custom-components/intro - Custom Components documentation, examples and set up steps. the important ones are below but if something is missing check here

    0. install Node.js
    [Node.js — Download Node.js® ](https://nodejs.org/en/download)
    Download with the windows installer
    Had to add C:\Program Files\nodejs\ to PATH in environmental variables for it to work

    check that everything has been downloaded correctly
    ```
    # Verify the Node.js version:
    node -v # Should print "v22.20.0".
    # Verify npm version:
    npm -v # Should print "10.9.3".
    ```

    NOTE: only works from cmd prompt not powershell

1. set up npm 

```
cd speed_control\frontend
npm install  
```
This will install all the dependancies described in package.json in a nodemodule folder - check that this folder is created

repeat in the direction_control frontend
```
cdcd direction_control\frontend
npm install  
```

2. install additional dependancies for packages
    install dependencies in the setup.py files
    ```
    cd speed_control\
    pip install -e . 
    ```

    ```
    cd direction_control\
    pip install -e . 
    ```
    
    ```
    cd rc_http_control\
    pip install -e . 
    ```
    TODO: create one setup.py folder that can handle all of this

## Do Every Time You Make A Change To The Component


3. start front end components
```
cd speed_control\frontend
npm run build
```

```
cd direction_control\frontend
npm run build
```
Runs the front end as a server (component acts like a little webpage)
You should see a build folder has been created in the frontend. 



# STEP 2: RUN webpage

## LOCAL MODE - all control from 1 PC
```
streamlit run app_control_rc_car.py
```
this will make the page available on your local PC. you can access it here:
[http://localhost:8501](http://localhost:8501/)



## PRODUCTION MODE - control from any PC on the same network
if you want other PCs on the same wifi network to be able to connect:

```
streamlit run app_control_rc_car.py --server.address=0.0.0.0 --server.port=8501
```
to conect you will need the host PC ip address - this can be obtained by running 
```
ipconfig
```
in the terminal of the host pc
then to access the page on a different PC go to
http://IPADDRESS:8501/
e.g.
[http://172.24.22.43:8501](http://172.24.22.43:85011/)

(url is still http://localhost:8501/ on the host PC)

