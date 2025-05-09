from ultralytics import YOLO
import cv2
import os

# Load a pre-trained YOLOv8 model
model = YOLO("last.pt")  # Use your trained model

# Supported video formats
video_extensions = ['.mp4', '.webm', '.avi', '.mov', '.mkv']

# Folder containing the videos
video_folder = 'videos'

# Get list of all video files in the 'videos' folder
video_files = [
    f for f in os.listdir(video_folder)
    if os.path.splitext(f)[1].lower() in video_extensions
]

def iou(box1, box2):
    """Calculate Intersection Over Union (IoU) between two boxes."""
    x1, y1, x2, y2 = box1
    a1, b1, a2, b2 = box2

    # Calculate intersection coordinates
    ix1 = max(x1, a1)
    iy1 = max(y1, b1)
    ix2 = min(x2, a2)
    iy2 = min(y2, b2)

    # Calculate intersection area
    intersection_area = max(0, ix2 - ix1) * max(0, iy2 - iy1)

    # Calculate area of both boxes
    box1_area = (x2 - x1) * (y2 - y1)
    box2_area = (a2 - a1) * (b2 - b1)

    # Calculate union area
    union_area = box1_area + box2_area - intersection_area

    # Calculate IoU
    iou = intersection_area / union_area if union_area != 0 else 0
    return iou

def remove_overlapping_boxes(boxes, confidences, threshold=0.5):
    """Remove overlapping boxes with confidence threshold, keeping the highest confidence."""
    keep = []
    for i, box in enumerate(boxes):
        # If a box is already in the keep list, skip it
        if any(iou(box, keep_box) > threshold for keep_box in keep):
            continue

        # Add box to keep list
        keep.append(box)

    return keep

# Process each video
for video_name in video_files:
    video_path = os.path.join(video_folder, video_name)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    print(f"🎥 Processing: {video_name}")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLOv8 inference on the frame
        results = model(frame)

        for result in results:
            boxes_np = result.boxes.xyxy.cpu().numpy()
            confs = result.boxes.conf.cpu().numpy()
            clss = result.boxes.cls.cpu().numpy()

            # Convert to lists for comparison
            boxes = [box.tolist() for box in boxes_np]

            # Remove overlapping boxes
            filtered_boxes = remove_overlapping_boxes(boxes, confs)

            # Draw the filtered boxes
            for i, box in enumerate(filtered_boxes):
                x1, y1, x2, y2 = map(int, box)
                label = f"{model.names[int(clss[i])]} {confs[i]:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the frame with detections
        cv2.imshow(f"YOLOv8 - {video_name}", frame)

        # Exit loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cap.release()
            cv2.destroyAllWindows()
            exit()

    cap.release()
    cv2.destroyAllWindows()
