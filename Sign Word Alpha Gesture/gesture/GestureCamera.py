import cv2
import datetime
from gesture.yolov8 import YOLOv8
from threading import Thread
import winsound
import threading



def detect(video_file_path):
    video_capture = cv2.VideoCapture(video_file_path)

    model_path = r"gesture/models/yolo_best.onnx"
    object_detector = YOLOv8(model_path, confidence_threshold=0.5, iou_threshold=0.5)

    send_counter = 0
    cv2.namedWindow("Gesture Detection Result", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Gesture Detection Result", 800, 600)  # Set the window size

    while video_capture.isOpened():
        if cv2.waitKey(1) == ord('q'):  # Press 'q' to stop
            break

        try:
            ret, frame = video_capture.read()
            if not ret:
                break
        except Exception as e:
            print(e)
            continue


        boxes, scores, class_ids = object_detector(frame)
        combined_image, label = object_detector.draw_detections(frame)


        cv2.imshow("Detected Objects", combined_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            video_capture.release()
            break

    video_capture.release()

    
