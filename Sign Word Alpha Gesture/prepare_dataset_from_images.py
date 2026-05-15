import cv2
import os
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import copy
from app_files import calc_landmark_list, pre_process_landmark
import csv
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_path", type=str, required=True, help="Path to the dataset directory")
    parser.add_argument("--output_csv", type=str, required=True, help="Path to the output CSV file")
    args = parser.parse_args()

    dataset_path = args.dataset_path
    output_csv = args.output_csv

    # Create a HandLandmarker object.
    base_options = python.BaseOptions(model_asset_path='model/keypoint_classifier/hand_landmarker.task')
    options = vision.HandLandmarkerOptions(base_options=base_options,
                                           num_hands=1)
    detector = vision.HandLandmarker.create_from_options(options)

    # Get the list of characters from the folder names
    characters = [f for f in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, f))]

    with open(output_csv, 'w', newline="") as f:
        writer = csv.writer(f)
        for char_index, char_folder in enumerate(characters):
            folder_path = os.path.join(dataset_path, char_folder)
            image_files = os.listdir(folder_path)

            for image_file in image_files:
                image_path = os.path.join(folder_path, image_file)
                print(f"Processing image: {image_path}")
                if not os.path.exists(image_path):
                    print(f"File not found: {image_path}")
                    continue
                
                try:
                    # Read the image using numpy and cv2.imdecode to handle unicode paths
                    img = np.fromfile(image_path, dtype=np.uint8)
                    image = cv2.imdecode(img, cv2.IMREAD_COLOR)

                    if image is None:
                        print(f"Could not read image: {image_path}")
                        continue
                    
                    # Convert the image to the format that mediapipe expects
                    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

                    # Process the image
                    detection_result = detector.detect(mp_image)

                    if detection_result.hand_landmarks:
                        for hand_landmarks in detection_result.hand_landmarks:
                            # Calculate landmarks
                            landmark_list = calc_landmark_list(image, hand_landmarks)
                            pre_processed_landmark_list = pre_process_landmark(landmark_list)

                            # Log the landmarks to the CSV file
                            writer.writerow([char_index, *pre_processed_landmark_list])
                    
                    print(f"Successfully processed {image_path} for character {char_folder} (label: {char_index})")
                except Exception as e:
                    print(f"Could not process image {image_path}. Error: {e}")

    print(f"Dataset processing complete. The {output_csv} file has been created.")

if __name__ == '__main__':
    main()
