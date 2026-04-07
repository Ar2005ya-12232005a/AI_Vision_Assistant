#define TRIG_PIN 9
#define ECHO_PIN 10
#define BUZZER_PIN 8

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {
  // Trigger ultrasonic pulse
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Read echo
  long duration = pulseIn(ECHO_PIN, HIGH, 30000);
  int distance = duration * 0.034 / 2;

  // Clamp invalid readings
  if (distance <= 0 || distance > 400) {
    distance = 400;
  }

  // Send to Python
  Serial.println(distance);

  // Buzzer feedback
  if (distance < 50) {
    tone(BUZZER_PIN, 1000, 100);
    delay(150);
  } else if (distance < 100) {
    tone(BUZZER_PIN, 700, 100);
    delay(400);
  } else {
    noTone(BUZZER_PIN);
    delay(200);
  }
}