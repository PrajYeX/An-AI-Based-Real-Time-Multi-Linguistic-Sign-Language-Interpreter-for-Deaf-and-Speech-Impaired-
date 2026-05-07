# Sign Word Alpha Gesture

This project is a desktop application that provides a comprehensive set of tools for learning and using sign language. It features real-time sign language recognition, voice-to-sign translation, and text-to-sign conversion.

## Features

*   **Alphabet Recognition**: Uses the webcam to recognize and translate sign language alphabet gestures into text in real-time.
*   **Voice to Sign**: Converts spoken words into a sequence of sign language images.
*   **Text to Gesture**: Converts typed text into a sequence of sign language images.
*   **Gesture Detection**: A real-time gesture detection feature that can be used to recognize a wider range of gestures.

## Workflow

1.  **Launch the application**: Run `python mainGUI.py` to start the application.
2.  **Main Dashboard**: The main dashboard displays four features: "Alphabet Recognition", "Voice to Sign", "Text to Gesture", and "Gesture Detection".
3.  **Alphabet Recognition**:
    *   Click the "Launch" button under "Alphabet Recognition".
    *   A new window will open with the webcam feed.
    *   Make sign language gestures in front of the camera.
    *   The application will recognize the gestures and display the corresponding text.
    *   Click the "Speak" button to hear the recognized text.
4.  **Voice to Sign**:
    *   Click the "Launch" button under "Voice to Sign".
    *   A new window will open.
    *   Click the "Listen" button and speak a word.
    *   The application will display a sequence of sign language images corresponding to the spoken word.
    *   Click the "Speak" button to hear the recognized word.
5.  **Text to Gesture**:
    *   Click the "Launch" button under "Text to Gesture".
    *   A new window will open.
    *   Type a word or phrase into the text box.
    *   Click the "Translate to Signs" button.
    *   The application will display a sequence of sign language images corresponding to the entered text.
    *   Click the "Speak" button to hear the entered text.
6.  **Gesture Detection**:
    *   Click the "Launch" button under "Gesture Detection".
    *   A new window will open with the webcam feed.
    *   The application will detect and recognize a variety of hand gestures in real-time.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/sign-word-alpha-gesture.git
    ```
2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```
3.  **Activate the virtual environment**:
    *   **Windows**:
        ```bash
        venv\Scripts\activate
        ```
    *   **macOS/Linux**:
        ```bash
        source venv/bin/activate
        ```
4.  **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Activate the virtual environment** (if not already activated).
2.  **Run the application**:
    ```bash
    python mainGUI.py
    ```

## File Descriptions

*   `mainGUI.py`: The main entry point of the application. It creates the main dashboard with four features.
*   `WebCam.py`: Implements the "Alphabet Recognition" feature. It uses the webcam to detect hand gestures and translate them into text.
*   `VoiceToSign.py`: Implements the "Voice to Sign" feature. It listens for voice input and displays the corresponding sign language images.
*   `WordToSign.py`: Implements the "Text to Gesture" feature. It takes text input from the user and displays the corresponding sign language images.
*   `gesture/GestureCamera.py`: Implements the "Gesture Detection" feature using the YOLOv8 model.
*   `model/`: Contains the machine learning models used for sign language recognition.
*   `dataset/`: Contains the images of sign language gestures.
*   `app_files/`: Contains helper functions for image processing and landmark calculation.
*   `requirements.txt`: A list of all the Python libraries required to run the project.
