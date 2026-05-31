#include <Servo.h>

// ---------- Pins ----------
const int TRIG_PIN          = 9;
const int ECHO_PIN          = 10;
const int SERVO_RADAR_PIN   = 6;
const int SERVO_AIM_PIN     = 5;
const int SERVO_TRIGGER_PIN = 3;
const int LED_PIN           = 12;
const int BUZZER_PIN        = 2;

// ---------- Sweep ----------
const int SCAN_MIN_ANGLE = 0;
const int SCAN_MAX_ANGLE = 180;
const int SCAN_STEP      = 1;
const int STEP_DELAY_MS  = 25;

const int DETECT_DISTANCE_CM = 20;

// ---------- Fire ----------
const int FIRE_REST_ANGLE  = 80;
const int FIRE_SHOOT_ANGLE = 15;
const int FIRE_HOLD_MS     = 300;
const int COOLDOWN_MS      = 1000;

// ---------- Servos ----------
Servo servoRadar;
Servo servoAim;
Servo servoTrigger;

// ---------- State ----------
int scanAngle = SCAN_MIN_ANGLE;
int scanDir   = 1;

bool lockedOnTarget = false;

// ---------- Distance ----------
long readDistance() {

  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 18000);

  if (duration == 0)
    return 999;

  return duration / 29 / 2;
}

// ---------- Fire ----------
void executeFireSequence() {

  digitalWrite(LED_PIN, HIGH);
  digitalWrite(BUZZER_PIN, HIGH);

  servoTrigger.write(FIRE_SHOOT_ANGLE);

  delay(FIRE_HOLD_MS);

  servoTrigger.write(FIRE_REST_ANGLE);

  digitalWrite(LED_PIN, LOW);
  digitalWrite(BUZZER_PIN, LOW);

  delay(COOLDOWN_MS);
}

// ---------- Setup ----------
void setup() {

  Serial.begin(115200);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  servoRadar.attach(SERVO_RADAR_PIN);
  servoAim.attach(SERVO_AIM_PIN);
  servoTrigger.attach(SERVO_TRIGGER_PIN);

  servoRadar.write(scanAngle);

  servoAim.write(90);

  servoTrigger.write(FIRE_REST_ANGLE);

  Serial.println("RADAR_READY");
}

// ---------- Loop ----------
void loop() {

  // ---------- RADAR SWEEP ----------
  servoRadar.write(scanAngle);

  delay(STEP_DELAY_MS);

  long distance = readDistance();

  // ---------- SEND DATA TO PROCESSING ----------
  Serial.print("scan a=");
  Serial.print(scanAngle);
  Serial.print(" d=");
  Serial.println(distance);

  // ---------- DETECTION ----------
  if (distance < DETECT_DISTANCE_CM) {

    servoAim.write(scanAngle);

    Serial.println("TARGET_FOUND");
  }

  // ---------- SERIAL COMMANDS ----------
  if (Serial.available()) {

    String cmd = Serial.readStringUntil('\n');

    cmd.trim();

    // ---------- MANUAL FIRE ----------
    if (cmd.startsWith("A")) {

      int fireAngle = cmd.substring(1).toInt();

      Serial.print("MANUAL_FIRE_AT:");
      Serial.println(fireAngle);

      servoAim.write(fireAngle);

      delay(200);

      executeFireSequence();
    }

    // ---------- PYTHON AUTO FIRE ----------
    if (cmd == "F") {

      Serial.println("AUTO_FIRE");

      executeFireSequence();
    }
  }

  // ---------- SWEEP DIRECTION ----------
  scanAngle += scanDir * SCAN_STEP;

  if (scanAngle >= SCAN_MAX_ANGLE)
    scanDir = -1;

  if (scanAngle <= SCAN_MIN_ANGLE)
    scanDir = 1;
}