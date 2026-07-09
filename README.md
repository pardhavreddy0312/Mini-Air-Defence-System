\# Mini Air Defence System



\## Overview



This project is an AI-powered Mini Air Defence System developed using computer vision, embedded systems, and IoT technologies. It uses a custom-trained YOLO11 model to detect aerial objects in real time and communicates with an Arduino-controlled turret to perform automated target response.



Unlike the default YOLO model trained on the COCO dataset, this project uses a custom dataset specifically prepared for aerial object detection.



The model can detect the following objects:



\* Drone

\* Bird

\* Helicopter

\* Airplane



\## Features



\* Custom-trained YOLO11 object detection model

\* Real-time aerial object detection

\* Arduino-based turret control

\* Ultrasonic sensor integration

\* Automatic target image capture

\* Telegram notifications

\* CUDA GPU acceleration



\## Technologies Used



\### Programming Languages



\* Python

\* Arduino (C/C++)



\### Libraries



\* Ultralytics YOLO11

\* OpenCV

\* PyTorch

\* PySerial

\* Requests



\### Hardware



\* Arduino UNO

\* SG90 Servo Motors

\* HC-SR04 Ultrasonic Sensor

\* USB Webcam



\## Project Structure



```text

Mini-Air-Defence-System

│

├── Arduino

├── Processing

├── Python

│   ├── main.py

│   ├── best.pt

│   └── requirements.txt

│

├── README.md

└── LICENSE

```



\## Installation



Clone the repository.



```bash

git clone https://github.com/pardhavreddy0312/Mini-Air-Defence-System.git

```



Move into the project directory.



```bash

cd Mini-Air-Defence-System

```



Install the required libraries.



```bash

pip install -r requirements.txt

```



Run the project.



```bash

python main.py

```



\## How It Works



1\. The webcam captures live video.

2\. The custom YOLO11 model detects aerial objects.

3\. If a valid target is detected, the Arduino receives the command through serial communication.

4\. The turret performs the configured action.

5\. The detected frame is saved.

6\. A Telegram notification with the captured image is sent.



\## Model Performance



| Class      | mAP@50 |


| Drone      |  85.7% |

| Bird       |  27.9% |

| Helicopter |  67.6% |

| Airplane   |  99.5% |



Overall \*\*mAP@50:\*\* \*\*70.2%\*\*



\## Future Work



\* DeepSORT-based object tracking

\* Kalman Filter for smoother target tracking

\* Multi-target tracking

\* Target prioritization

\* Improved custom dataset



\## Author



\*\*Pardhav Reddy\*\*



B.Tech – Artificial Intelligence (Cyber Physical Systems \& Security)



Amrita Vishwa Vidyapeetham



\## License



This project is licensed under the MIT License.



