#include <WiFi.h>
#include <WebServer.h>
#include <ESP32Servo.h>
#include <ESP32Ping.h>
#include "pitches.h"
#include "melodies.h"
//#include "http_handlers.h"
//#include "car_control.h"


// run state
extern bool available_to_connect = true;
extern bool running = false;

// wifi set up
const char* ssid = "gabriel";
const char* password = "gabrielgabriel";
WebServer server(80);
// wifi check
unsigned long lastCheck = 0;
const unsigned long checkInterval = 10000;

// ESC control
#define ESC_PIN    2 
#define BUZZER_PIN 9 
// Servo control
#define SERVO_PIN  6
Servo esc;       
Servo myServo;

// Sound Control
#define SPEAKER_PIN 9         // Pin for speaker/buzzer
#define BUZZER_CHANNEL 3      // Pick a safe PWM channel (0–15)
#define TONE_RESOLUTION 8 
bool play_sound = false;
int* melody = melody_darth_vader;
int melodyLength = sizeof(melody_darth_vader) / sizeof(melody_darth_vader[0]);
int tempo = 120; // change this to make the song slower or faster
int notes = sizeof(melody) / sizeof(melody[0]) / 2;
// this calculates the duration of a whole note in ms
int wholenote = (60000 * 4) / tempo;
int divider = 0, noteDuration = 0;
int stop_current = false;

// WIFI Functions
// connection check
bool isOnline() {
  IPAddress test_ip(8,8,8,8);
  return (WiFi.status() == WL_CONNECTED) && Ping.ping(test_ip);
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
    digitalWrite(LED_BUILTIN, HIGH);   // Turn LED ON
    Serial.println("\nConnected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nFailed to connect to WiFi.");
  }
}

// // HTTP handlers
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

void handleReqSoundChange(){
  Serial.println("handleReqSoundChange");
  String sound = server.arg("sound");
  server.send(200, "text/plain", "yes");
  Serial.println(sound);
  if (sound == "OFF"){
    stop_current = true;
    play_sound = false;
  }else{
    stop_current = true; // interrupt the song that is currently playing 
    chooseMelody(sound);
    stop_current = false;
    play_sound = true;
  }
}


// MUSIC functions
void myTone(int pin, int freq, int channel = 3, int duty = 128) {
  ledcSetup(channel, freq, 8);         // 8-bit resolution, freq in Hz
  ledcAttachPin(pin, channel);
  ledcWrite(channel, duty);            // 128 = 50% duty cycle
}
void myNoTone(int channel = 3) {
  ledcWrite(channel, 0);               // Stop PWM signal
}

void chooseMelody(String current_sound){
  if (current_sound ="DARTHVADER"){
    melody = melody_darth_vader;
    melodyLength = sizeof(melody_darth_vader) / sizeof(melody_darth_vader[0]);
  } else if (current_sound = "BWD"){
    melody = melody_bwd;
    melodyLength = sizeof(melody_bwd) / sizeof(melody_bwd[0]);
  }
  tempo = 120; // change this to make the song slower or faster
  notes = sizeof(melody) / sizeof(melody[0]) / 2;
  // this calculates the duration of a whole note in ms
  wholenote = (60000 * 4) / tempo;
  divider = 0, noteDuration = 0;
}


void playMusicAndHTTPListen() {
  //for (int thisNote = 0; thisNote < notes * 2; thisNote += 2) {
  for (int thisNote = 0; thisNote < melodyLength; thisNote += 2) {
    if (stop_current){
      play_sound = false;
      break; // interupt looping song
    }
    server.handleClient(); // Process any incoming HTTP requests

    int divider = melody[thisNote + 1];
    if (divider > 0) {
      noteDuration = wholenote / divider;
    } else if (divider < 0) {
      noteDuration = (wholenote / abs(divider)) * 1.5;
    }

    int note = melody[thisNote];

    if (note > 0) {
      myTone(SPEAKER_PIN, note, BUZZER_CHANNEL);
    } else {
      myNoTone(BUZZER_CHANNEL); // REST
    }

    delay(noteDuration); // Wait full note duration
    myNoTone(BUZZER_CHANNEL); // Stop the tone
  }
}




void setup() {
  Serial.begin(115200);
  delay(1000);

  pinMode(LED_BUILTIN, OUTPUT);  // Set the internal LED pin as output

  // Connect to WiFi
  connectToWiFi();

  // ESC control
  esc.attach(ESC_PIN, 1000, 2000);
  Serial.println("ESC controller ready.");
  setESC("1500");  // Initialize ESC with STOP signal

  // Servo control
  myServo.attach(SERVO_PIN);
  Serial.println("Servo PWM initialized.");
  setServo("90");

  // set up handlers (common)
  server.on("/", handleRoot);
  server.on("/reqconnect", handleReqConnect);
  server.on("/reqstart", handleReqStart);
  server.on("/reqchangespeed", handleReqSpeedChange);
  server.on("/reqchangeservo", handleReqServoChange);
  server.on("/reqstop", handleReqStop);
  server.on("/reqchangesound", handleReqSoundChange);

  // Start server
  server.begin();
  Serial.println("HTTP server started");
}

// void loop() {
//   server.handleClient();
// }

void loop() {
  if (!play_sound){
    server.handleClient();
  } else {
    playMusicAndHTTPListen();
  }
}


// // functions for ESC control
void setESC(String speed) {
  Serial.print("Setting ESC speed to ");
  int speed_int = speed.toInt(); // Convert string to integer
  Serial.println(speed_int);

  esc.writeMicroseconds(speed_int); // Send pulse in microseconds (1000-2000 typical)
  if (speed_int < 1500){
    Serial.print("Double_SIGNAL");
    delay(100);
    esc.writeMicroseconds(1500);
    delay(100);
    esc.writeMicroseconds(speed_int);
  }
}

// Function to control Servo using angle
void setServo(String angle) {
  Serial.print("Setting servo angle to ");
  Serial.println(angle);

  int angle_int = angle.toInt();
  myServo.write(angle_int);
}
