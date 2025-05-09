from ultralytics import YOLO
import cv2
import os

# Load the trained YOLOv8 model
model = YOLO("last.pt")

# Supported image formats
image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']

# Folder containing the images
image_folder = 'pics'

# Get list of all image files in the 'pics' folder
image_files = [
    f for f in os.listdir(image_folder)
    if os.path.splitext(f)[1].lower() in image_extensions
]

# Process each image
for image_name in image_files:
    image_path = os.path.join(image_folder, image_name)

    # Read the image
    image = cv2.imread(image_path)

    # Run YOLOv8 inference on the image
    results = model(image)

    # Plot the results (bounding boxes, labels)
    for result in results:
        annotated_image = result.plot()

    # Show the result
    cv2.imshow(f"Detection - {image_name}", annotated_image)
    print(f"🔍 Showing results for: {image_name}")

    # Wait for key press to move to next image or quit
    key = cv2.waitKey(0)
    if key == ord('q'):
        break

# Cleanup
cv2.destroyAllWindows()
