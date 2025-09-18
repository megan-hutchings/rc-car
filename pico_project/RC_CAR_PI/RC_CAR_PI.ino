#include <WiFi.h>
#include <WebServer.h>

// add servo libraroes
#include "RP2040_PWM.h"

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
#define PWM_PIN 15
#define LED_PIN LED_BUILTIN
RP2040_PWM* escPWM = nullptr;
const float PWM_FREQUENCY = 50.0f; 

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

void handleReqSpeedChange(){
  Serial.println(" handleReqSpeedChange");
  String direction = server.arg("dir");

  if(!(available_to_connect) && running) {
    server.send(200, "text/plain", "yes");
    Serial.print("Changing speed/movement to: ");
    Serial.println(direction);
    setESC(direction);
    Serial.println("finished setting PWM");
  } else{
    server.send(200, "text/plain", "no");
  }
}


void setup() {
  Serial.begin(115200);
  delay(1000);

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

  ////////////////////// Board Specific
  // ESC control
  escPWM = new RP2040_PWM(PWM_PIN, PWM_FREQUENCY, 0.0f);
  if (escPWM) {
    escPWM->setPWM(PWM_PIN, PWM_FREQUENCY, 0.0f);
  }
  Serial.println("ESC controller ready.");
  setESC("STOP");  // Initialize ESC with STOP signal
  pinMode(LED_PIN, OUTPUT);

  // Servo control

  // set up handlers (common)
  server.on("/", handleRoot);
  server.on("/reqconnect", handleReqConnect);
  server.on("/reqstart", handleReqStart);
  server.on("/reqchangespeed", handleReqSpeedChange);
  server.on("/reqstop", handleReqStop);

  // Start server
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}


////////////////////////////////////Board Specific
// functions for ESC control
void setPWM_us(RP2040_PWM* pwmObj, int pulse_us) {
  if (!pwmObj) return;
  // For 50 Hz, period is 20000 microseconds
  float duty = (float)pulse_us / 20000.0f;   // e.g. 1000 => 0.05, 1500 => 0.075, 2000 => 0.10
  pwmObj->setPWM(pwmObj->getPin(), PWM_FREQUENCY, duty * 100.0f);  // duty in percent
}

void setESC(String direction) {
  int pulse = 1500;  // STOP by default

  if (direction == "FWD") {
    pulse = 1200;
    digitalWrite(LED_PIN, HIGH);   // Turn LED ON
  } else if (direction == "BWD") {
    pulse = 1000;
    digitalWrite(LED_PIN, HIGH);   // Turn LED ON
  } else if (direction == "STOP") {
    pulse = 1500;
    digitalWrite(LED_PIN, LOW);    // Turn LED OFF
  }

  Serial.print("Setting direction to ");
  Serial.print(direction);
  Serial.print(" with pulse width: ");
  Serial.println(pulse);

  // Use PWM library
  setPWM_us(escPWM, pulse);
}
