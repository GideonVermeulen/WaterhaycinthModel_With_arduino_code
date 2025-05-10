#include <Servo.h>  // Make sure this library is available

// Ultrasonic sensor pins
const int trigPin = 3;
const int echoPin = 2;

// Motor 1 control pins
const int motor1Pin1 = 12;
const int motor1Pin2 = 13;

// Motor 2 control pins
const int motor2Pin1 = 11;
const int motor2Pin2 = 10;

// Servo pin
const int servoPin = 9;
Servo myServo;

long duration;
float distance;

unsigned long previousServoTime = 0;
bool servoUp = false;

void setup() {
  // Motor pins
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(motor2Pin1, OUTPUT);
  pinMode(motor2Pin2, OUTPUT);

  // Ultrasonic pins
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Servo setup
  myServo.attach(servoPin);
  myServo.write(0);  // Start at 0°

  // Serial Monitor
  Serial.begin(9600);
}

void loop() {
  // Measure distance
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.0343 / 2;

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  // Motor control based on distance
  if (distance < 10) {
    // Stop motors
    digitalWrite(motor1Pin1, LOW);
    digitalWrite(motor1Pin2, LOW);
    digitalWrite(motor2Pin1, LOW);
    digitalWrite(motor2Pin2, LOW);
  } else {
    // Move forward
    digitalWrite(motor1Pin1, HIGH);
    digitalWrite(motor1Pin2, LOW);
    digitalWrite(motor2Pin1, HIGH);
    digitalWrite(motor2Pin2, LOW);
  }

  // Move servo every 5 seconds
  unsigned long currentTime = millis();
  if (currentTime - previousServoTime >= 2000) {
    if (servoUp) {
      myServo.write(0);
    } else {
      myServo.write(90);
    }
    servoUp = !servoUp;
    previousServoTime = currentTime;
  }

  delay(100);
}