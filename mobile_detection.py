import cv2
import torch
from ultralytics import YOLO

# Load trained YOLO model
model = YOLO(r"C:\Users\Disha\OneDrive\Desktop\Cheating-Surveillance-System-main\model\best_yolov12.pt")  
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def process_mobile_detection(frame):
    results = model(frame, verbose=False)
    mobile_detected = False

    for result in results:
        for box in result.boxes:
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())

            if conf < 0.8 or cls != 0:  # Mobile class index is 0
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])  
            label = f"Mobile ({conf:.2f})"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            mobile_detected = True
    
    return frame, mobile_detected

# cap = cv2.VideoCapture(0)

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Process frame
#     frame, mobile_detected = process_mobile_detection(frame)

#     # Display "Mobile Detected" message on the screen
#     if mobile_detected:
#         cv2.putText(frame, "MOBILE DETECTED!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

#     # Show the frame
#     cv2.imshow("Mobile Detection", frame)

#     # Exit on 'q' key press
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release resources
# cap.release()
# cv2.destroyAllWindows()
