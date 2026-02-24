const int trigPin = 6;
const int echoPin = 7;
const int ledPin  = 4;
const int buzzerPin = 5;

long duration;
int distanceCm;

void setup()
{ 
  Serial.begin(9600);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
}

void loop()
{
  // Generate ultrasonic pulse
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Measure echo time
  duration = pulseIn(echoPin, HIGH);

  // Convert to distance in cm
  distanceCm = duration * 0.034 / 2;

  Serial.print("Distance (cm): ");
  Serial.println(distanceCm);

  // Presence detection threshold
  if(distanceCm < 40)
  {
    digitalWrite(buzzerPin, HIGH);
    digitalWrite(ledPin, HIGH);
  }
  else
  {
    digitalWrite(buzzerPin, LOW);
    digitalWrite(ledPin, LOW);
  }

  delay(100);
}