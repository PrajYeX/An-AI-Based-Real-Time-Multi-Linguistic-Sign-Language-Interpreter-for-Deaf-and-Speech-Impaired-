
import tkinter as tk
from tkinter import ttk, font
import speech_recognition as sr
import threading
from PIL import Image, ImageTk
import tempfile
import pygame
import os

pygame.mixer.init()

class VoiceToSignApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice to Sign Language")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f2f5')

        # --- Fonts and Styles ---
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.info_font = font.Font(family="Helvetica", size=12)
        self.status_font = font.Font(family="Helvetica", size=14, weight="bold")
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 12, 'bold'), padding=12, background='#1a73e8', foreground='#000000')
        style.map('TButton', background=[('active', '#1557b0')], foreground=[('active', '#000000')])
        style.configure('Exit.TButton', font=('Helvetica', 12, 'bold'), padding=12, background='#d63031', foreground='#000000')
        style.map('Exit.TButton', background=[('active', '#c92a1f')], foreground=[('active', '#000000')])


        # --- UI Elements ---
        self.main_frame = tk.Frame(root, bg='#f0f2f5', padx=20, pady=20)
        self.main_frame.pack(fill='both', expand=True)

        self.title_label = tk.Label(self.main_frame, text="Voice to Sign", font=self.title_font, bg='#f0f2f5', fg='#1a73e8')
        self.title_label.pack(pady=(0, 20))

        # This frame will contain the sign images
        self.image_container = tk.Frame(self.main_frame, bg='#ffffff', relief='solid', borderwidth=1)
        self.image_container.pack(pady=20, expand=True, fill='both')

        self.status_label = tk.Label(self.main_frame, text="Press 'Listen' and speak a word.", font=self.status_font, bg='#f0f2f5')
        self.status_label.pack(pady=10)

        self.recognized_text_label = tk.Label(self.main_frame, text="", font=self.info_font, bg='#f0f2f5')
        self.recognized_text_label.pack(pady=10)

        # Frame for buttons
        button_frame = tk.Frame(self.main_frame, bg='#f0f2f5')
        button_frame.pack(pady=20)

        # Language Selector
        self.lang_var = tk.StringVar(value="English")
        self.lang_combo = ttk.Combobox(button_frame, textvariable=self.lang_var, values=["English", "Kannada", "Hindi"], state="readonly", width=10)
        self.lang_combo.pack(side='left', padx=10)

        self.listen_button = ttk.Button(button_frame, text="Listen", command=self.start_listening_thread)
        self.listen_button.pack(side='left', padx=10)

        self.speak_button = ttk.Button(button_frame, text="Speak", command=self.speak_text)
        self.speak_button.pack(side='left', padx=10)
        
        self.exit_button = ttk.Button(button_frame, text="Exit", command=self.exit_to_main, style='Exit.TButton')
        self.exit_button.pack(side='right', padx=10)


        # --- Recognizer & State ---
        self.recognizer = sr.Recognizer()
        self.is_listening = False

    def speak_text(self):
        text = self.recognized_text_label.cget("text")
        if text and "You said: " in text:
            text_to_speak = text.replace("You said: ", "")
            try:
                from gtts import gTTS
                lang = 'en'
                if self.lang_var.get() == "Kannada":
                    lang = 'kn'
                elif self.lang_var.get() == "Hindi":
                    lang = 'hi'
                tts = gTTS(text=text_to_speak, lang=lang, slow=False)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)
                    temp_audio_file = fp.name
                
                pygame.mixer.music.stop()
                pygame.mixer.music.load(temp_audio_file)
                pygame.mixer.music.play()

                # Wait for the music to finish playing
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)

                # Clean up the temporary file
                import time
                for _ in range(5):
                    try:
                        os.remove(temp_audio_file)
                        break
                    except PermissionError:
                        time.sleep(0.1)
            except Exception as e:
                print(f"Error in TTS: {e}")

    def start_listening_thread(self):
        if not self.is_listening:
            self.is_listening = True
            self.listen_button.config(state=tk.DISABLED)
            self.recognized_text_label.config(text="") # Clear previous text
            self.clear_images() # Clear previous images
            threading.Thread(target=self.listen_and_process, daemon=True).start()

    def clear_images(self):
        """Destroy all child widgets (image labels) in the container."""
        for widget in self.image_container.winfo_children():
            widget.destroy()

    def listen_and_process(self):
        """
        Runs in a background thread to handle audio capture and recognition.
        Schedules GUI updates on the main thread using root.after().
        """
        # Print the list of available microphones
        print("Available microphones:")
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"  {index}: {name}")
            
        self.root.after(0, lambda: self.status_label.winfo_exists() and self.status_label.config(text="Listening..."))
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source)

            self.root.after(0, lambda: self.status_label.winfo_exists() and self.status_label.config(text="Recognizing..."))
            
            lang_code = 'en-US'
            if self.lang_var.get() == "Kannada":
                lang_code = 'kn-IN'
            elif self.lang_var.get() == "Hindi":
                lang_code = 'hi-IN'
            text = self.recognizer.recognize_google(audio, language=lang_code).lower()
            
            # Schedule GUI updates for the recognized text and start the image display
            if self.root.winfo_exists():
                self.root.after(0, lambda: self.recognized_text_label.config(text=f"You said: {text}"))
                self.root.after(0, lambda: self.display_signs_for_text(text))

        except sr.UnknownValueError:
            if self.root.winfo_exists():
                self.root.after(0, lambda: self.status_label.config(text="Sorry, I could not understand the audio."))
                self.root.after(100, self.reset_ui_state)
        except sr.RequestError:
            if self.root.winfo_exists():
                self.root.after(0, lambda: self.status_label.config(text="API unavailable. Check internet connection."))
                self.root.after(100, self.reset_ui_state)
        except Exception as e:
            if self.root.winfo_exists():
                self.root.after(0, lambda e=e: self.status_label.config(text=f"An error occurred: {e}"))
                self.root.after(100, self.reset_ui_state)

    def display_signs_for_text(self, text):
        """
        Loads, resizes, and displays all sign images for the given text at once.
        This method is called on the main thread via root.after().
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if not self.status_label.winfo_exists():
            return
        self.status_label.config(text="Displaying signs...")
        
        selected_language = self.lang_var.get()
        image_paths = []
        
        # Define characters to ignore (vowel signs, special characters, etc.)
        kannada_chars_to_ignore = ['್', 'ಾ', 'ಿ', 'ೀ', 'ು', 'ೂ', 'ೃ', 'ೆ', 'ೇ', 'ೈ', 'ೊ', 'ೋ', 'ೌ', 'ಂ', 'ಃ']
        hindi_chars_to_ignore = ['्', 'ा', 'ि', 'ी', 'ु', 'ू', 'ृ', 'े', 'ै', 'ो', 'ौ', 'ं', 'ः']

        for char in text:
            if not char.strip(): continue # Skip spaces
            
            image_path = None
            if selected_language == "Kannada":
                if char in kannada_chars_to_ignore: continue
                char_folder = os.path.join(script_dir, 'Kannada Dataset', char)
                if os.path.isdir(char_folder):
                    images_in_folder = [f for f in os.listdir(char_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                    if images_in_folder:
                        image_path = os.path.join(char_folder, images_in_folder[0])
            elif selected_language == "Hindi":
                if char in hindi_chars_to_ignore: continue
                char_folder = os.path.join(script_dir, 'HindiSignImages', char)
                if os.path.isdir(char_folder):
                    images_in_folder = [f for f in os.listdir(char_folder) if f.lower().endswith(('.png', 'jpg', 'jpeg'))]
                    if images_in_folder:
                        image_path = os.path.join(char_folder, images_in_folder[0])
            else: # English
                image_path = os.path.join(script_dir, f"dataset/{char}.jpeg")
            
            if image_path and os.path.exists(image_path):
                image_paths.append(image_path)
            else:
                if selected_language == "Kannada":
                    print(f"Image not found for Kannada character '{char.encode('unicode_escape').decode('ascii')}' at path: {image_path}")
                elif selected_language == "Hindi":
                    print(f"Image not found for Hindi character '{char.encode('unicode_escape').decode('ascii')}' at path: {image_path}")
                else:
                    print(f"Image not found for English character '{char}' at path: {image_path}")

        if not image_paths:
            self.status_label.config(text="No signs to display for that word.")
            self.reset_ui_state()
            return

        for image_path in image_paths:
            try:
                img = Image.open(image_path)
                img.thumbnail((150, 150), Image.LANCZOS) # Resize to a smaller thumbnail
                photo = ImageTk.PhotoImage(img)
                
                img_label = tk.Label(self.image_container, image=photo, bg='#ffffff')
                img_label.image = photo # Keep a reference!
                img_label.pack(side='left', padx=5, pady=5)

            except Exception as e:
                print(f"Could not display image {image_path}: {e}")
        
        # UI state is reset only when the user clicks "Listen" again
        self.is_listening = False
        self.listen_button.config(state=tk.NORMAL)
        self.status_label.config(text="Done. Press 'Listen' to try again.")


    def reset_ui_state(self):
        """Resets the UI to the initial state, ready for the next listen."""
        self.is_listening = False
        self.listen_button.config(state=tk.NORMAL)
        self.status_label.config(text="Press 'Listen' and speak a word.")

    def exit_to_main(self):
        """Destroy the current window."""
        self.root.destroy()

def main(root=None):
    if root:
        app = VoiceToSignApp(root)
    else:
        root = tk.Tk()
        app = VoiceToSignApp(root)
        root.mainloop()

if __name__ == "__main__":
    main()
