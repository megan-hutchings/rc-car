
#include <WiFi.h>
#include <WebServer.h>
#include <ESP32Ping.h>
// const char* ssid = "Akkodis Nordics DevNet";
// const char* password = "$m3llycat";
const char* ssid = "megan";
const char* password = "meganmegan";// Set up web server on port 80
WebServer server(80);

// // set static IP addresses
// IPAddress staticIP(192, 168, 137, 100);
// IPAddress gateway(192, 168, 137, 1);
// IPAddress subnet(255, 255, 255, 0);
// IPAddress dns(0, 0, 0, 0);

// Handler for root path
void handleRoot() {
  server.send(200, "text/plain", "Hello from Arduino Nano ESP32!");
}

void setup() {
  Serial.begin(115200);
  delay(1000);


  // if (WiFi.config(staticIP, gateway, subnet, dns, dns) == false) {
  //   Serial.println("Configuration failed.");
  // }

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi...");
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


  // Set up HTTP handler
  server.on("/", handleRoot);

  // Start server
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}