import sys
import enchant
import cv2
import os
import operator
import tkinter as tk
from PIL import Image, ImageTk
from string import ascii_uppercase
from gtts import gTTS
import numpy as np
from tkinter import ttk
import csv
import copy
import cv2 as cv
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.components import processors
from model import KeyPointClassifier
import tempfile
import pygame
from app_files import calc_landmark_list, draw_info_text, draw_landmarks, get_args, pre_process_landmark

pygame.mixer.init()

class ModernApplication:
    def __init__(self, top=None):
        """Initialize the application with a modern UI"""
        self.top = top
        self.current_language = "en_US"
        self.setup_initial_variables()
        self.initialize_detection_system()
        self.setup_window(top)
        self.create_ui_elements(top)
        self.start_video_processing()

    def setup_initial_variables(self):
        """Initialize all required variables and dictionaries"""
        try:
            self.d = enchant.Dict(self.current_language)
        except enchant.errors.DictNotFoundError:
            self.d = None
        self.directory = "model/"
        self.current_image = None
        self.counter = 0
        self.prediction = []
        self.str = ""
        self.word = ""
        self.current_symbol = "Empty"
        self.photo = "Empty"
        self.kannada_characters = ['ಅ', 'ಆ', 'ಇ', 'ಈ', 'ಉ', 'ಊ', 'ಋ', 'ಎ', 'ಏ', 'ಐ', 'ಒ', 'ಓ', 'ಔ', 'ಅಂ', 'ಅಃ', 'ಕ', 'ಖ', 'ಗ', 'ಘ', 'ಙ', 'ಚ', 'ಛ', 'ಜ', 'ಝ', 'ಞ', 'ಟ', 'ಠ', 'ಡ', 'ಢ', 'ಣ', 'ತ', 'ಥ', 'ದ', 'ಧ', 'ನ', 'ಪ', 'ಫ', 'ಬ', 'ಭ', 'ಮ', 'ಯ', 'ರ', 'ಲ', 'ವ', 'ಶ', 'ಷ', 'ಸ', 'ಹ', 'ಳ']
        self.hindi_characters = ['अ','आ','इ','ई','उ','ए','ऐ','ओ','क','क्ष','ख','ग','घ','च','छ','ज','ज्ञ','झ','ट','ठ','ड','ढ','ण','त','थ','द','ध','न','प','फ','ब','भ','म','य','र','ल','व','श','स','ह']
        
        # Initialize character tracking
        self.ct = {'blank': 0}
        if self.current_language == "en_US":
            self.ct.update({char: 0 for char in ascii_uppercase})
        elif self.current_language == "kn_IN":
            self.ct.update({char: 0 for char in self.kannada_characters})
        else:
            self.ct.update({char: 0 for char in self.hindi_characters})

    def change_language(self, lang):
        if lang == "English":
            self.current_language = "en_US"
        elif lang == "Kannada":
            self.current_language = "kn_IN"
        else:
            self.current_language = "hi_IN"
        
        self.initialize_detection_system()
        self.setup_initial_variables()

    def initialize_detection_system(self):
        """Setup video capture and hand detection"""
        args = get_args()
        
        # Configure video capture
        self.cap = cv.VideoCapture(0)  # Changed to directly use 0 for default camera
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)  # Set standard width
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)  # Set standard height

        # Initialize MediaPipe hands
        # Create a HandLandmarker object.
        # Get the directory of the current script to build correct absolute paths
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_asset_path = os.path.join(script_dir, 'model', 'hand_landmarker.task')
        base_options = python.BaseOptions(model_asset_path=model_asset_path)
        options = vision.HandLandmarkerOptions(base_options=base_options,
                                               num_hands=1,
                                               min_hand_detection_confidence=0.7,
                                               min_hand_presence_confidence=0.7,
                                               min_tracking_confidence=0.5,
                                               running_mode=vision.RunningMode.IMAGE) # Change to VIDEO if continuous stream
        self.detector = vision.HandLandmarker.create_from_options(options)

        # Initialize classifier based on language
        if self.current_language == "en_US":
            model_path = os.path.join(script_dir, 'model', 'keypoint_classifier', 'keypoint_classifier_with_numbers.tflite')
            label_path = os.path.join(script_dir, 'model', 'keypoint_classifier', 'keypoint_classifier_label.csv')
        elif self.current_language == "kn_IN":
            model_path = os.path.join(script_dir, 'model', 'keypoint_classifier', 'kannada_keypoint_classifier.tflite')
            label_path = os.path.join(script_dir, 'model', 'keypoint_classifier', 'kannada_keypoint_classifier_label.csv')
        else:
            model_path = os.path.join(script_dir, 'model', 'keypoint_classifier', 'hindi_keypoint_classifier.tflite')
            label_path = os.path.join(script_dir, 'model', 'keypoint_classifier', 'hindi_keypoint_classifier_label.csv')

        self.keypoint_classifier = KeyPointClassifier(model_path=model_path)
        
        # Load classifier labels
        with open(label_path, encoding='utf-8-sig') as f:
            self.keypoint_classifier_labels = [row[0] for row in csv.reader(f)]

    def setup_window(self, top):
        """Configure the main window"""
        top.title("Sign Language Detection System")
        top.state('zoomed')
        top.configure(bg='#f0f2f5')
        
        # Configure styles
        self.configure_styles()

    def configure_styles(self):
        """Setup custom styles for widgets"""
        style = ttk.Style()
        
        # Configure frame styles
        style.configure('Card.TFrame', background='#ffffff', relief='flat')
        
        # Configure label styles
        style.configure('Title.TLabel', 
                       font=('Helvetica', 24, 'bold'),
                       background='#ffffff',
                       foreground='#1a73e8')
        
        style.configure('Heading.TLabel',
                       font=('Helvetica', 16, 'bold'),
                       background='#ffffff')
        
        style.configure('Content.TLabel',
                       font=('Helvetica', 14),
                       background='#ffffff')
        
        # Configure button styles - High contrast
        style.configure('Primary.TButton',
                       font=('Helvetica', 12, 'bold'),
                       padding=10,
                       background='#1a73e8',
                       foreground='#000000')
        style.map('Primary.TButton',
                 background=[('active', '#1557b0')],
                 foreground=[('active', '#000000')])
        
        style.configure('Secondary.TButton',
                       font=('Helvetica', 12, 'bold'),
                       padding=8,
                       background='#2ea44f',
                       foreground='#000000')
        style.map('Secondary.TButton',
                 background=[('active', '#2d9e47')],
                 foreground=[('active', '#000000')])

    def create_ui_elements(self, top):
        """Create all UI elements"""
        # Create main containers
        self.create_header(top)
        main_container = ttk.Frame(top, style='Card.TFrame')
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create two columns
        left_column = ttk.Frame(main_container, style='Card.TFrame')
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        right_column = ttk.Frame(main_container, style='Card.TFrame')
        right_column.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Create video panel
        self.create_video_panel(left_column)
        
        # Create controls and info panels
        self.create_info_panel(right_column)
        self.create_suggestions_panel(right_column)
        self.create_sentence_panel(right_column)

    def create_header(self, parent):
        """Create the header with title and controls"""
        header = ttk.Frame(parent, style='Card.TFrame')
        header.pack(fill='x', padx=20, pady=10)
        
        title = ttk.Label(header, 
                         text="Sign Language Detection System",
                         style='Title.TLabel')
        title.pack(side='left')

        # Language selection dropdown
        self.language_var = tk.StringVar(value="English")
        language_menu = tk.OptionMenu(header, self.language_var, "English", "Kannada", "Hindi", command=self.change_language)
        language_menu.pack(side='left', padx=10)
        
        exit_btn = ttk.Button(header,
                             text="Exit",
                             style='Primary.TButton',
                             command=self.exit_application)
        exit_btn.pack(side='right')

    def create_video_panel(self, parent):
        """Create the video display panel"""
        video_frame = ttk.Frame(parent, style='Card.TFrame')
        video_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.panel = ttk.Label(video_frame)
        self.panel.pack(padx=10, pady=10)

    def create_info_panel(self, parent):
        """Create the prediction and word info panel"""
        info_frame = ttk.Frame(parent, style='Card.TFrame')
        info_frame.pack(fill='x', padx=10, pady=10)
        
        # Prediction display
        pred_frame = ttk.Frame(info_frame, style='Card.TFrame')
        pred_frame.pack(fill='x', pady=5)
        
        ttk.Label(pred_frame,
                 text="Prediction:",
                 style='Heading.TLabel').pack(side='left')
        
        self.lblPrediction = ttk.Label(pred_frame,
                                     style='Content.TLabel')
        self.lblPrediction.pack(side='left', padx=(10, 0))
        
        # Word display
        word_frame = ttk.Frame(info_frame, style='Card.TFrame')
        word_frame.pack(fill='x', pady=5)
        
        ttk.Label(word_frame,
                 text="Word:",
                 style='Heading.TLabel').pack(side='left')
        
        self.lblWords = ttk.Label(word_frame,
                                style='Content.TLabel')
        self.lblWords.pack(side='left', padx=(10, 0))
        
        # New Speak button
        speak_btn = ttk.Button(word_frame,
                               text="Speak",
                               style='Secondary.TButton',
                               command=self.speak_current_word)
        speak_btn.pack(side='left', padx=(10, 0))

    def create_suggestions_panel(self, parent):
        """Create the suggestions panel with buttons"""
        suggestions_frame = ttk.Frame(parent, style='Card.TFrame')
        suggestions_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(suggestions_frame,
                 text="Suggestions",
                 style='Heading.TLabel').pack(pady=(0, 10))
        
        # Create suggestion buttons
        self.suggestion_buttons = []
        buttons_frame = ttk.Frame(suggestions_frame, style='Card.TFrame')
        buttons_frame.pack(fill='x')
        
        for i in range(5):
            btn = ttk.Button(buttons_frame,
                           text=f"Suggestion {i+1}",
                           style='Secondary.TButton',
                           command=lambda x=i: self.set_suggestion(x))
            btn.pack(side='left', padx=5)
            self.suggestion_buttons.append(btn)
        
        # Clear button
        ttk.Button(buttons_frame,
                  text="Clear",
                  style='Primary.TButton',
                  command=self.clear_text).pack(side='left', padx=5)

    def create_sentence_panel(self, parent):
        """Create the sentence display panel"""
        sentence_frame = ttk.Frame(parent, style='Card.TFrame')
        sentence_frame.pack(fill='x', padx=10, pady=10)
        
        self.lblSentence = ttk.Label(sentence_frame,
                                   text="Sentence: ",
                                   style='Content.TLabel',
                                   wraplength=400)
        self.lblSentence.pack(fill='x')

    def set_suggestion(self, index):
        """Handle suggestion button clicks"""
        if self.suggestion_buttons[index]['text']:
            current_sentence = self.lblSentence['text']
            new_word = self.suggestion_buttons[index]['text']
            self.lblSentence.configure(text=f"{current_sentence} {new_word}")
            self.lblWords.configure(text='')

    def clear_text(self):
        """Clear the current word"""
        self.lblWords.configure(text='')
        self.prediction.clear()

    def speak_text(self, text):
        """Convert text to speech in a separate thread"""
        try:
            # A simple mapping for potentially ambiguous characters
            if text == 'I':
                speech_text = "I"
            elif text == 'O':
                speech_text = "O"
            else:
                speech_text = text

            lang = 'en' if self.current_language == 'en_US' else 'kn'
            tts = gTTS(text=speech_text, lang=lang, slow=False)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                temp_audio_file = fp.name
            
            # Play sound using pygame.mixer
            pygame.mixer.music.stop()
            pygame.mixer.music.load(temp_audio_file)
            pygame.mixer.music.play()
            
            # Clean up the temporary file
            os.remove(temp_audio_file)
        except Exception as e:
            print(f"Error in TTS: {e}")

    def speak_current_word(self):
        """Speak the text currently displayed in lblWords"""
        word_to_speak = self.lblWords['text']
        if word_to_speak: # Only speak if there's text
            self.speak_text(word_to_speak)

    def check_all_fingers_up(self, hand_landmarks_list):
        """Check if all fingers are raised"""
        if hand_landmarks_list:
            # Thumb check
            if hand_landmarks_list[4].y < hand_landmarks_list[3].y:
                return False
                
            # Other fingers check
            for finger_tip, finger_base in zip(range(8, 20, 4), range(6, 20, 4)):
                if hand_landmarks_list[finger_tip].y > hand_landmarks_list[finger_base].y:
                    return False
            return True
        return False

    def process_frame(self):
        """Process a single video frame"""
        ret, image = self.cap.read()
        if not ret:
            return
            
        image = cv.flip(image, 1)
        debug_image = copy.deepcopy(image)
        image = cv.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Convert the image to MediaPipe's Image format.
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
        detection_result = self.detector.detect(mp_image)
        
        if detection_result.hand_landmarks:
            for i in range(len(detection_result.hand_landmarks)):
                hand_landmarks = detection_result.hand_landmarks[i]
                handedness_obj = detection_result.handedness[i]
                # Extract handedness label (e.g., "Left" or "Right")
                handedness_label = handedness_obj[0].category_name
                
                # Process landmarks
                landmark_list = calc_landmark_list(debug_image, hand_landmarks)
                pre_processed_landmark_list = pre_process_landmark(landmark_list)
                hand_sign_id = self.keypoint_classifier(pre_processed_landmark_list)
                
                # Draw landmarks
                debug_image = draw_landmarks(debug_image, landmark_list)
                debug_image = draw_info_text(debug_image,
                                          handedness_label, # Pass the extracted label
                                          self.keypoint_classifier_labels[hand_sign_id])
                
                # Handle gestures
                self.handle_gesture(hand_landmarks, 
                                  self.keypoint_classifier_labels[hand_sign_id])
                
        return debug_image

    def handle_gesture(self, hand_landmarks, label):
        """Handle detected gestures"""
        if self.check_all_fingers_up(hand_landmarks):
            # cv2.putText(self.current_image,
            #            'Clear Text',
            #            (100, 100),
            #            cv2.FONT_HERSHEY_SIMPLEX,
            #            1,
            #            (0, 255, 0),
            #            2)
            self.clear_text()
        else:
            self.lblPrediction.config(text=label)
            
            if self.counter == 80:
                self.process_prediction(label)
            else:
                self.counter += 1
                self.prediction.append(label)

    def process_prediction(self, label):
        """Process the accumulated predictions"""
        self.counter = 0
        most_common = max(set(self.prediction), key=self.prediction.count)
        
        current_text = self.lblWords["text"] + most_common
        self.lblWords.config(text=current_text)
        
        # Get word suggestions only for English
        if self.d and self.current_language == "en_US" and self.d.check(current_text):
            suggestions = self.d.suggest(current_text)
            self.update_suggestions(suggestions)
        
        self.prediction.clear()

    def update_suggestions(self, suggestions):
        """Update suggestion buttons with new words"""
        for i, button in enumerate(self.suggestion_buttons):
            if i < len(suggestions):
                button.config(text=suggestions[i])
            else:
                button.config(text='')

    def start_video_processing(self):
        """Start the video processing loop"""
        self.video_loop()

    def video_loop(self):
        """Main video processing loop"""
        debug_image = self.process_frame()
        if debug_image is not None:
            self.current_image = debug_image
            self.update_video_display()
        self.top.after(30, self.video_loop)

    def update_video_display(self):
        """Update the video display panel"""
        cv2image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGBA)
        self.current_image = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=self.current_image)
        self.panel.imgtk = imgtk
        self.panel.config(image=imgtk)

    def exit_application(self):
        """Clean up and exit the application"""
        self.cap.release()
        self.top.destroy()

def vp_start_gui():
    """Start the application"""
    root = tk.Tk()
    app = ModernApplication(root)
    root.mainloop()
