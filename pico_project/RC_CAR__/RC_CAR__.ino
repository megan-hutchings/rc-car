#include <WiFi.h>
#include <WebServer.h>

// add servo libraries

////////////////////// Common parts
// wifi set up
const char* ssid = "megan";
const char* password = "meganmegan";
WebServer server(80);

// run state
bool available_to_connect = true;
bool running = false;


////////////////////// Board Specific
// ESC control

// Servo control


// Handlers (common)
void handleRoot() {
  server.send(200, "text/plain", "Hello from Pi");
}

void handleReqConnect(){
  Serial.println("handleReqConnect");
  if (available_to_connect){
    server.send(200, "text/plain", "yes");
    available_to_connect = false;
    Serial.println("connected to PC");
  } else{
    server.send(200, "text/plain", "no"); //change
    Serial.println("denied connection to PC");
  }
}

void handleReqStart(){
  Serial.println("handleReqStart");
  if(!(available_to_connect)) {
    server.send(200, "text/plain", "yes");
    running = true;
    Serial.println("starting run mode"); 
  } else{
    server.send(200, "text/plain", "not_connected");
  }
}

void handleReqStop(){
  Serial.println("handleReqStop");
  if(!(available_to_connect)) {
    server.send(200, "text/plain", "yes");
    running = false;
    available_to_connect = true;
    Serial.println("stopping run mode"); 
  } else{
    server.send(200, "text/plain", "not_connected");
  }
}

// void handleReqServo


void setup() {
  Serial.begin(115200);
  delay(1000);

  // Connect to Wi-Fi (common)
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  Serial.print("Subnet Mask: ");
  Serial.println(WiFi.subnetMask());
  Serial.print("Gateway IP: ");
  Serial.println(WiFi.gatewayIP());

////////////////////// Board Specific
// ESC control

// Servo control

// set up handlers (common)
server.on("/", handleRoot);
server.on("/reqconnect", handleReqConnect);
server.on("/reqstart", handleReqStart);
server.on("/reqchangespeed", handleReqSpeedChange);
server.on("/reqstop", handleReqStop);
//server.on("/reqstop", handleReqServo);

// Start server
server.begin();
Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}



////////////////////////////////////Board Specific
// functions for ESC control
// void setESC(String direction) {

// functions for servo control


// functions for servo control
