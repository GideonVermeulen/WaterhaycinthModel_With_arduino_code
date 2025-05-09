from ultralytics import YOLO
import cv2
import serial
import time

# Initialize serial connection (adjust COM port as needed)
arduino = serial.Serial('COM3', 9600)  # Change 'COM3' to match your setup
time.sleep(2)  # Wait for Arduino to initialize

model = YOLO("best.pt")

cap = cv2.VideoCapture(0)


last_sent = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break


    results = model(frame)

    object_detected = False
    box_drawn = False

    for result in results:
        if len(result.boxes) > 0:
            for box in result.boxes:
                if box.conf > 0.55:  # Only consider boxes with > 55% confidence
                    object_detected = True

                    if not box_drawn:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
                        label = f"{model.names[int(box.cls[0])]}: {float(box.conf[0]):.2f}"
                        cv2.putText(frame, label, (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                        box_drawn = True
                    break

    # Debounced serial communication
    if object_detected and last_sent != b'1':
        arduino.write(b'1')
        last_sent = b'1'
    elif not object_detected and last_sent != b'0':
        arduino.write(b'0')
        last_sent = b'0'

    # Show webcam feed with overlays
    cv2.imshow("YOLOv8 Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
arduino.close()
