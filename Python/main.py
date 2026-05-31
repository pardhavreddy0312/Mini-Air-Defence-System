import cv2
import serial
import time
import requests

from datetime import datetime
from ultralytics import YOLO

# ---------------- SETTINGS ----------------
ARDUINO_PORT = 'COM11'
BAUD_RATE = 115200

CONFIDENCE = 0.5

# bottle, phone, book, cup, backpack
TARGET_CLASSES = [39, 67, 73, 41, 24]

# ---------- TELEGRAM ----------
BOT_TOKEN = "YOUR TOKEN"
CHAT_ID = "YOUR CHAT ID"

# ------------------------------------------

print("Initializing Sky_Forge Vision System...")

# ---------- TELEGRAM ALERT ----------
def send_telegram_alert():

    current_time = datetime.now().strftime("%H:%M:%S")

    message = f"""
🚨 TARGET ELIMINATED
Auto Turret Fired Successfully

Time: {current_time}
"""

    url = f"https://api.telegram.org/bot8057290238:AAGg4KnvtIou4jfa6Kmo-8d-663KmUhY3cE/sendMessage"

    data = {
        "chat_id": 8013272467,
        "text": message
    }

    try:

        requests.post(url, data=data)

        print("Telegram Alert Sent")

    except Exception as e:

        print("Telegram Error:", e)


# ---------- SEND TARGET PHOTO ----------
def send_telegram_photo(image_path):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    try:

        with open(image_path, "rb") as photo:

            files = {
                "photo": photo
            }

            data = {
                "chat_id": CHAT_ID,
                "caption": "📸 TARGET CAPTURED"
            }

            requests.post(
                url,
                files=files,
                data=data
            )

        print("Target Image Sent")

    except Exception as e:

        print("Photo Error:", e)


# ---------- ARDUINO CONNECTION ----------
try:

    arduino = serial.Serial(
        port=ARDUINO_PORT,
        baudrate=BAUD_RATE,
        timeout=0.1
    )

    time.sleep(2)

    print("Arduino Connected")

except Exception as e:

    print("Connection Failed:", e)

    exit()

# ---------- LOAD YOLO ----------
model = YOLO("yolo11n.pt")

# FORCE CPU MODE
model.to("cpu")

print("YOLO Model Loaded")

# ---------- EXTERNAL WEBCAM ----------
# 0 = laptop webcam
# 1 = external webcam

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not cap.isOpened():

    print("External webcam not found")
    print("Trying laptop camera...")

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():

        print("No camera detected")

        exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Camera Started")
print("SYSTEM READY")

# ---------- CREATE WINDOW ----------
cv2.namedWindow("Sky Forge Vision HUD", cv2.WINDOW_NORMAL)

# ---------- DETECTION FUNCTION ----------
def scan_frame(frame):

    # RUN YOLO ON CPU
    results = model(frame, verbose=False, device="cpu")

    threat_detected = False

    for result in results:

        if result.boxes is None:
            continue

        for box in result.boxes:

            cls_id = int(box.cls[0])

            conf = float(box.conf[0])

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            label = model.names[cls_id]

            # ---------- TARGET DETECTED ----------
            if cls_id in TARGET_CLASSES and conf > CONFIDENCE:

                threat_detected = True

                # GREEN BOX
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    3
                )

                cv2.putText(
                    frame,
                    f"{label} {conf:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

            else:

                # RED BOX
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 0, 255),
                    1
                )

    return threat_detected


# ---------- MAIN LOOP ----------
while True:

    ret, frame = cap.read()

    if not ret:

        print("Frame capture failed")

        continue

    frame = cv2.resize(frame, (640, 480))

    # ---------- YOLO DETECTION ----------
    threat = scan_frame(frame)

    # ---------- STATUS ----------
    if threat:

        status = "NOT SAFE"

        color = (0, 0, 255)

    else:

        status = "SAFE"

        color = (0, 255, 0)

    cv2.putText(
        frame,
        status,
        (frame.shape[1] - 200, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        3
    )

    # ---------- SERIAL COMMUNICATION ----------
    if arduino.in_waiting > 0:

        try:

            msg = arduino.readline().decode().strip()

            print("Arduino:", msg)

            if "TARGET_FOUND" in msg:

                print("Sensor triggered")

                if threat:

                    print("VALID TARGET -> FIRE")

                    arduino.write(b'F\n')

                    # ---------- SAVE IMAGE ----------
                    image_name = f"target_{int(time.time())}.jpg"

                    cv2.imwrite(image_name, frame)

                    print("Image Saved")

                    # ---------- TELEGRAM ALERT ----------
                    send_telegram_alert()

                    # ---------- SEND PHOTO ----------
                    send_telegram_photo(image_name)

                else:

                    print("FALSE TARGET")

        except Exception as e:

            print("Serial Error:", e)

    # ---------- DISPLAY ----------
    cv2.imshow("Sky Forge Vision HUD", frame)

    # ---------- KEYBOARD ----------
    key = cv2.waitKey(1) & 0xFF

    # ---------- MANUAL FIRE ----------
    if key == ord('f'):

        print("MANUAL FIRE")

        arduino.write(b'F\n')

        # ---------- SAVE IMAGE ----------
        image_name = f"manual_{int(time.time())}.jpg"

        cv2.imwrite(image_name, frame)

        # ---------- TELEGRAM ALERT ----------
        send_telegram_alert()

        # ---------- SEND PHOTO ----------
        send_telegram_photo(image_name)

    # ---------- EXIT ----------
    if key == ord('q'):

        break


# ---------- CLEANUP ----------
cap.release()

cv2.destroyAllWindows()

arduino.close()

print("System Shutdown")