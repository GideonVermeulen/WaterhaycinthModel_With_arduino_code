from ultralytics import YOLO
import cv2

# Load a pre-trained YOLOv8 model
model = YOLO("Best.pt")  # Use your trained model

# Open the webcam (0 for default webcam)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLOv8 inference on the frame
    results = model(frame)

    # Filter detections based on confidence (≥ 55%)
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()  # Get the bounding box coordinates
        confidences = result.boxes.conf.cpu().numpy()  # Get the confidence scores
        classes = result.boxes.cls.cpu().numpy()  # Get the class labels
        
        # Loop through detections and only draw boxes with confidence ≥ 55%
        for i, conf in enumerate(confidences):
            if conf >= 0.65:  # Only show boxes with confidence 55% or more
                x1, y1, x2, y2 = map(int, boxes[i])  # Get coordinates of the box
                label = f"{model.names[int(classes[i])]} {conf:.2f}"  # Label with class and confidence
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw bounding box
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  # Put text label

    # Display the frame with detections
    cv2.imshow("YOLOv8 Object Detection - Webcam", frame)

    # Exit loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
