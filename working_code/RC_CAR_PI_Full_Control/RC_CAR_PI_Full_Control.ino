#include <WiFi.h>
#include <WebServer.h>
#include <Servo.h>
#include "RP2040_PWM.h"

// wifi set up
const char* ssid = "gabriel";
const char* password = "gabrielgabriel";
WebServer server(80);
// wifi check
unsigned long lastCheck = 0;
const unsigned long checkInterval = 10000;

// run state
bool available_to_connect = true;
bool running = false;

// ESC control
#define PWM_PIN 14
#define LED_PIN LED_BUILTIN
RP2040_PWM* escPWM = nullptr;
const float PWM_FREQUENCY = 50.0f; 

// Servo control
Servo myServo;  // create servo object

// connection check
bool isOnline() {
  IPAddress test_ip(8,8,8,8);  // host PC - update to wifi later
  return (WiFi.status() == WL_CONNECTED)&& (WiFi.ping(test_ip) >= 0);
}


// wifi connect
void connectToWiFi(int maxRetries = 10){
  WiFi.disconnect(true);  // Fully reset Wi-Fi state
  delay(1000);  
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");

  int retries = 0;
  while (WiFi.status() != WL_CONNECTED && retries < maxRetries) {
    delay(500);
    Serial.print(".");
    retries++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    digitalWrite(LED_PIN, HIGH);   // Turn LED ON
    Serial.println("\nConnected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nFailed to connect to WiFi.");
  }
}

// HTTP handlers
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

void handleReqSpeedChange(){
  Serial.println("handleReqSpeedChange");
  String speed = server.arg("speed");

  if(!(available_to_connect) && running) {
    server.send(200, "text/plain", "yes");
    Serial.print("Changing speed/movement to: ");
    Serial.println(speed);
    setESC(speed);
    Serial.println("finished setting PWM");
  } else{
    server.send(200, "text/plain", "no");
  }
}

void handleReqServoChange(){
  Serial.println("handleReqServoChange");
  String angle = server.arg("angle");

  if(!(available_to_connect) && running) {
    server.send(200, "text/plain", "yes");
    Serial.println(angle);
    setServo(angle);
    Serial.println("finished setting Servo");
  } else{
    server.send(200, "text/plain", "no");
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(1000);

  connectToWiFi();

  // ESC control
  escPWM = new RP2040_PWM(PWM_PIN, PWM_FREQUENCY, 0.0f);
  if (escPWM) {
    escPWM->setPWM(PWM_PIN, PWM_FREQUENCY, 0.0f);
  }
  Serial.println("ESC controller ready.");
  setESC("1500");  // Initialize ESC with STOP signal

  pinMode(LED_PIN, OUTPUT);
  // Servo control
  myServo.attach(3);  // attach servo signal to GPIO15
  Serial.println("Servo PWM initialized.");
  setServo("90");

  // set up handlers (common)
  server.on("/", handleRoot);
  server.on("/reqconnect", handleReqConnect);
  server.on("/reqstart", handleReqStart);
  server.on("/reqchangespeed", handleReqSpeedChange);
  server.on("/reqchangeservo", handleReqServoChange);
  server.on("/reqstop", handleReqStop);

  // Start server
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();

  if (millis() - lastCheck > checkInterval) {
    lastCheck = millis();
    if (!isOnline()) {
      setESC("1500");
      digitalWrite(LED_PIN, LOW);
      Serial.println("WiFi lost (ping failed). Reconnecting...");
      connectToWiFi();
    }
  }
}

// functions for ESC control
void setPWM_us(RP2040_PWM* pwmObj, int pulse_us) {
  if (!pwmObj) return;
  // For 50 Hz, period is 20000 microseconds
  float duty = (float)pulse_us / 20000.0f;   // e.g. 1000 => 0.05, 1500 => 0.075, 2000 => 0.10
  pwmObj->setPWM(pwmObj->getPin(), PWM_FREQUENCY, duty * 100.0f);  // duty in percent
}

void setESC(String speed) {
  Serial.print("Setting speed to ");
  int speed_int = speed.toInt();
  Serial.print(speed);
  Serial.print(speed_int);

  // Use PWM library
  setPWM_us(escPWM, speed_int);
}

// functions for Servo control
void setServo(String angle){

  Serial.print("Setting direction to ");
  Serial.print(angle);

  myServo.write(angle.toInt());
}
