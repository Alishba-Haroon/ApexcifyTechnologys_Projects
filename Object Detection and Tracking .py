import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

# Initialize YOLOv8 model (download automatically)
model = YOLO("yolov8n.pt")  # Use YOLOv8n for small and fast model

# Initialize Deep SORT tracker
tracker = DeepSort(max_age=30)

# Start webcam
cap = cv2.VideoCapture(0)  # 0 = default webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run object detection
    results = model.predict(frame, stream=True)  # stream=True for batch processing

    detections = []
    for r in results:
        for box in r.boxes:  # boxes detected in frame
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            # Append to tracker input (format: [x1, y1, x2, y2, confidence])
            detections.append([x1, y1, x2, y2, conf])

    # Update tracker
    tracks = tracker.update_tracks(detections, frame=frame)

    # Draw boxes and IDs
    for track in tracks:
        if not track.is_confirmed():
            continue
        track_id = track.track_id
        ltrb = track.to_ltrb()  # left, top, right, bottom
        x1, y1, x2, y2 = map(int, ltrb)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"ID:{track_id}", (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Display output
    cv2.imshow("Object Detection & Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
