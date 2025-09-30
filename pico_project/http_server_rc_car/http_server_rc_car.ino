
#include <WiFi.h>
#include <WebServer.h>

// const char* ssid = "Akkodis Nordics DevNet";
// const char* password = "$m3llycat";
const char* ssid = "megan";
const char* password = "meganmegan";// Set up web server on port 80
const char* hostname = "rc2_pi";
WebServer server(80);
bool available_to_connect = true;
bool running = false;

// // set static IP addresses
// IPAddress staticIP(192, 168, 137, 100);
// IPAddress gateway(192, 168, 137, 1);
// IPAddress subnet(255, 255, 255, 0);
// IPAddress dns(0, 0, 0, 0);

// Handler for root path
void handleRoot() {
  server.send(200, "text/plain", "Hello from Arduino Nano ESP32!");
}

void handleReqConnect(){
  Serial.println("handleReqConnect");
  if (available_to_connect){
    server.send(200, "text/plain", "yes");
    available_to_connect = false;
    Serial.println("connected to PC");
  } else{
    server.send(200, "text/plain", "no");
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

void handleReqSpeedChange(){
  Serial.println(" handleReqSpeedChange");
  if(!(available_to_connect) && running) {
    server.send(200, "text/plain", "yes");
    Serial.println("changing speed to" );
  } else{
    server.send(200, "text/plain", "no");
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);


  // if (WiFi.config(staticIP, gateway, subnet, dns, dns) == false) {
  //   Serial.println("Configuration failed.");
  // }
  //WiFi.mode(WIFI_STA);
  WiFi.setHostname(hostname); // Set the hostname

  // Connect to Wi-Fi
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
  Serial.print("DNS 1: ");
  Serial.println(WiFi.dnsIP(0));
  Serial.print("DNS 2: ");
  Serial.println(WiFi.dnsIP(1));


  // Set up HTTP handlers
  server.on("/", handleRoot);
  server.on("/reqconnect", handleReqConnect);
  server.on("/reqstart", handleReqStart);
  server.on("/reqchangespeed", handleReqSpeedChange);

  // Start server
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}