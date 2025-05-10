#include <Servo.h>

Servo myServo;
int servoPin = 9;
char incomingByte;

bool isSweeping = false;
bool objectDetected = false;

int sweepStage = 0;
unsigned long lastMoveTime = 0;
unsigned long lastSweepFinishedTime = 0;

const unsigned long delayBetweenSteps = 300;
const unsigned long cooldownBetweenSweeps = 600;
const int sweepAngle = 160;  // Sweep angle

void setup() {
  myServo.attach(servoPin);
  Serial.begin(9600);
}

void loop() {
  // Read from serial input
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    if (incomingByte == '1') {
      objectDetected = true;
    } else if (incomingByte == '0') {
      objectDetected = false;
    }
  }

  // Start a new sweep
  if (objectDetected && !isSweeping && millis() - lastSweepFinishedTime >= cooldownBetweenSweeps) {
    isSweeping = true;
    sweepStage = 1;
    lastMoveTime = millis();
    myServo.write(90 - (sweepAngle / 2)); // Start of sweep
  }

  if (isSweeping) {
    unsigned long now = millis();
    switch (sweepStage) {
      case 1:
        if (now - lastMoveTime >= delayBetweenSteps) {
          myServo.write(90 + (sweepAngle / 2)); // End of sweep
          lastMoveTime = now;
          sweepStage = 2;
        }
        break;

      case 2:
        if (now - lastMoveTime >= delayBetweenSteps) {
          myServo.write(90); // Return to center
          lastMoveTime = now;
          sweepStage = 3;
        }
        break;

      case 3:
        if (now - lastMoveTime >= delayBetweenSteps) {
          isSweeping = false;
          lastSweepFinishedTime = now;
          sweepStage = 0;
        }
        break;
    }
  }
}