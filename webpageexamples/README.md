# Web Page and HTTP Examples
## Contains code for the web application used for interfacing with the RC car

[Information on streamlit](https://streamlit.io/)

## run streamlit application locally
```
streamlit run app.py
```

## link to local page
[http://localhost:8501](http://localhost:8501/)


## Run page locally so that other PCs on the same network can access
```
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
```
(url is still http://localhost:8501/ on the host PC)
## Find IP address of the host PC
```
ipconfig
```
### e.g. 172.24.22.43

## Connect to a page run on the host PC
[http://172.24.22.43:8501](http://172.24.22.43:85011/)


## if doesn't work check can access through the wifi and check the IP address on PC hasn'tchanged
ping 172.24.22.43
ping 172.24.21.6

IP adress changes when you connect to a different network - need to check that IP address hasn't changed if connection doesn't work


# Basic HTTP communication python

## Client
```
python client.py
```

## Server
```
python server.py
```
