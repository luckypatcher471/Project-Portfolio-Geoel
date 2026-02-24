// --- Configuration ---
#define TRIG_PIN 9
#define ECHO_PIN 10
const int PROXIMITY_THRESHOLD_CM = 40; // You can adjust this threshold (40cm is a good starting point)
// --- State Tracking ---
int currentState = -1; // -1 for initial state, 0 for break, 1 for work

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  Serial.begin(9600); // Must match the baud rate used by the Python script
}

// Function to get distance from HC-SR04
long getDistance() {
  // Clear the trigger pin
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  // Send 10us pulse to trigger
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Measure the duration of the echo pulse
  long duration = pulseIn(ECHO_PIN, HIGH);
  
  // Convert time to distance (speed of sound is 343 m/s or 29 us/cm)
  // Distance = (duration / 2) / 29.1 
  long distanceCm = duration / 58; 
  
  return distanceCm;
}

void loop() {
  long distance = getDistance();
  int newState;
  // 1. Determine the State based on the threshold
  if (distance > 0 && distance <= PROXIMITY_THRESHOLD_CM) {
    // Desk is occupied (working)
    newState = 1; 
  } else {
    // Desk is vacant (on break or away)
    newState = 0;
  }
  
  // 2. Only send the STATE (1 or 0) if it changes
  
  //Serial.println(distance);
  Serial.println(newState);


  // Wait a moment before the next reading
  delay(500); // Reading every 0.5 seconds
}