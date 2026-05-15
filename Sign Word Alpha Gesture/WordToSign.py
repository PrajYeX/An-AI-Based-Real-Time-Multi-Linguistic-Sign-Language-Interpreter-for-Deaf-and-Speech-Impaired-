import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import tempfile
import pygame
import os
import math

pygame.mixer.init()

class ModernTheme:
    # Premium color scheme
    PRIMARY_COLOR = "#6C63FF"  # Modern Purple
    SECONDARY_COLOR = "#FFFFFF"
    BACKGROUND_COLOR = "#F0F2F5"
    CARD_BACKGROUND = "#FFFFFF"
    TEXT_COLOR = "#2D3748"
    HOVER_COLOR = "#5851DB"
    BORDER_COLOR = "#E2E8F0"
    
    def configure_styles():
        style = ttk.Style()
        
        # Configure main styles
        style.configure("Premium.TFrame",
            background=ModernTheme.BACKGROUND_COLOR
        )
        
        # Card frame style
        style.configure("Card.TFrame",
            background=ModernTheme.CARD_BACKGROUND,
            relief="flat"
        )
        
        # Modern button style
        style.configure("Premium.TButton",
            padding=(30, 15),
            font=("Segoe UI", 11, "bold"),
            background=ModernTheme.PRIMARY_COLOR,
            foreground="#000000",
            relief="solid",
            borderwidth=2
        )
        style.map("Premium.TButton",
            background=[("active", ModernTheme.HOVER_COLOR), ("disabled", "#cccccc")],
            foreground=[("active", "#000000"), ("disabled", "#666666")]
        )
        
        # Label styles
        style.configure("Premium.TLabel",
            background=ModernTheme.BACKGROUND_COLOR,
            foreground=ModernTheme.TEXT_COLOR,
            font=("Segoe UI", 11)
        )
        
        # High-contrast button styles
        style.configure("Success.TButton",
            padding=(20, 12),
            font=("Segoe UI", 10, "bold"),
            background="#2ea44f",
            foreground="#000000"
        )
        style.map("Success.TButton",
            background=[("active", "#2d9e47"), ("disabled", "#cccccc")],
            foreground=[("active", "#000000"), ("disabled", "#666666")]
        )
        
        style.configure("Accent.TButton",
            padding=(20, 12),
            font=("Segoe UI", 10, "bold"),
            background="#bf3989",
            foreground="#000000"
        )
        style.map("Accent.TButton",
            background=[("active", "#a03270"), ("disabled", "#cccccc")],
            foreground=[("active", "#000000"), ("disabled", "#666666")]
        )
        
        style.configure("Card.TLabel",
            background=ModernTheme.CARD_BACKGROUND,
            foreground=ModernTheme.TEXT_COLOR,
            font=("Segoe UI", 11)
        )
        
        style.configure("Title.TLabel",
            background=ModernTheme.BACKGROUND_COLOR,
            foreground=ModernTheme.PRIMARY_COLOR,
            font=("Segoe UI", 28, "bold")
        )
        
        style.configure("Subtitle.TLabel",
            background=ModernTheme.BACKGROUND_COLOR,
            foreground=ModernTheme.TEXT_COLOR,
            font=("Segoe UI", 12)
        )

class ImageCard(ttk.Frame):
    def __init__(self, parent, image, char, *args, **kwargs):
        super().__init__(parent, style="Card.TFrame", *args, **kwargs)
        
        # Create card effect using nested frames
        self.outer_frame = ttk.Frame(self, style="Card.TFrame", padding=1)
        self.outer_frame.grid(sticky="nsew")
        
        # Add shadow effect using canvas
        self.canvas = tk.Canvas(
            self.outer_frame,
            width=160,
            height=200,
            highlightthickness=0,
            bg=ModernTheme.CARD_BACKGROUND
        )
        self.canvas.grid(row=0, column=0)
        
        # Create inner content frame
        self.content_frame = ttk.Frame(self.canvas, style="Card.TFrame")
        self.canvas.create_window(80, 100, window=self.content_frame)
        
        # Add image
        self.img_label = ttk.Label(self.content_frame, image=image, style="Card.TLabel")
        self.img_label.grid(row=0, column=0, pady=(10, 5))
        
        # Add character label
        self.char_label = ttk.Label(
            self.content_frame,
            text=char.upper(),
            style="Card.TLabel",
            font=("Segoe UI", 16, "bold")
        )
        self.char_label.grid(row=1, column=0, pady=(5, 10))

class SignLanguageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Language Visualizer")
        self.root.geometry("1200x800")
        self.root.configure(bg=ModernTheme.BACKGROUND_COLOR)
        
        # Configure modern theme
        ModernTheme.configure_styles()
        
        # Create main container with padding
        self.container = ttk.Frame(root, style="Premium.TFrame", padding=40)
        self.container.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(2, weight=1)  # Make results section expandable
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header Section
        self.header_frame = ttk.Frame(self.container, style="Premium.TFrame")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 30))
        
        self.title = ttk.Label(
            self.header_frame,
            text="Sign Language Visualizer",
            style="Title.TLabel"
        )
        self.title.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        self.subtitle = ttk.Label(
            self.header_frame,
            text="Enter text below to visualize its sign language representation",
            style="Subtitle.TLabel"
        )
        self.subtitle.grid(row=1, column=0, sticky="w")
        
        # Input Section
        self.input_frame = ttk.Frame(self.container, style="Premium.TFrame")
        self.input_frame.grid(row=1, column=0, sticky="ew", pady=(0, 30))
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        # Custom entry style
        self.entry_frame = ttk.Frame(self.input_frame, style="Card.TFrame")
        self.entry_frame.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        self.text_input = ttk.Entry(
            self.entry_frame,
            font=("Segoe UI", 14),
            style="Premium.TEntry"
        )
        self.text_input.grid(row=0, column=0, sticky="ew", padx=15, pady=12)
        self.entry_frame.grid_columnconfigure(0, weight=1)
        
        # Language Selector
        self.lang_var = tk.StringVar(value="English")
        self.lang_combo = ttk.Combobox(
            self.input_frame, 
            textvariable=self.lang_var, 
            values=["English", "Kannada", "Hindi"], 
            state="readonly", 
            width=10,
            font=("Segoe UI", 11)
        )
        self.lang_combo.grid(row=0, column=1, padx=(10, 0))

        self.translate_button = ttk.Button(
            self.input_frame,
            text="Translate to Signs",
            style="Premium.TButton",
            command=self.analyze_text
        )
        self.translate_button.grid(row=0, column=2, padx=(10, 0))

        self.speak_button = ttk.Button(
            self.input_frame,
            text="Speak",
            style="Premium.TButton",
            command=self.speak_text
        )
        self.speak_button.grid(row=0, column=3, padx=(10, 0))
        
        # Results Section with vertical scrolling
        self.results_frame = ttk.Frame(self.container, style="Premium.TFrame")
        self.results_frame.grid(row=2, column=0, sticky="nsew")
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_rowconfigure(0, weight=1)
        
        # Create canvas and scrollbar for vertical scrolling
        self.canvas = tk.Canvas(
            self.results_frame,
            bg=ModernTheme.BACKGROUND_COLOR,
            highlightthickness=0
        )
        self.scrollbar = ttk.Scrollbar(
            self.results_frame,
            orient="vertical",
            command=self.canvas.yview
        )
        
        # Grid layout for canvas and scrollbar
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure canvas scrolling
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Create frame for content
        self.scrollable_frame = ttk.Frame(self.canvas, style="Premium.TFrame")
        self.canvas_frame = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )
        
        # Configure scrolling behavior
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind(
            "<Configure>",
            self.on_canvas_configure
        )
        
        # Enable mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Bind keyboard events
        self.text_input.bind('<Return>', lambda e: self.analyze_text())
        
        # Store references
        self.photo_references = []
        
        # Show initial message
        self.show_initial_message()

    def speak_text(self):
        text = self.text_input.get().lower().strip()
        if text:
            try:
                from gtts import gTTS
                lang = 'en'
                if self.lang_var.get() == "Kannada":
                    lang = 'kn'
                elif self.lang_var.get() == "Hindi":
                    lang = 'hi'
                tts = gTTS(text=text, lang=lang, slow=False)
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
                os.remove(temp_audio_file)
            except Exception as e:
                print(f"Error in TTS: {e}")
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def on_canvas_configure(self, event):
        # Update the width of the frame to fill the canvas
        self.canvas.itemconfig(self.canvas_frame, width=event.width)
        
        # Configure grid columns in scrollable frame
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)
        self.scrollable_frame.grid_columnconfigure(2, weight=1)
        self.scrollable_frame.grid_columnconfigure(3, weight=1)
        self.scrollable_frame.grid_columnconfigure(4, weight=1)
    
    def show_initial_message(self):
        message = ttk.Label(
            self.scrollable_frame,
            text="Your sign translations will appear here",
            style="Premium.TLabel",
            font=("Segoe UI", 12)
        )
        message.grid(row=0, column=0, columnspan=5, pady=50)
    
    def analyze_text(self):
        # Clear previous content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.photo_references.clear()
        
        text = self.text_input.get().lower().strip()
        
        if not text:
            self.show_initial_message()
            return
        
        found_any = False

        selected_language = self.lang_var.get()

        kannada_chars_to_ignore = ['್', 'ಾ', 'ಿ', 'ೀ', 'ು', 'ೂ', 'ೃ', 'ೆ', 'ೇ', 'ೈ', 'ೊ', 'ೋ', 'ೌ', 'ಂ', 'ಃ']
        hindi_chars_to_ignore = ['्', 'ा', 'ि', 'ी', 'ु', 'ू', 'ृ', 'े', 'ै', 'ो', 'ौ', 'ं', 'ः']
        
        chars = []
        for char in text:
            if not char.strip(): continue
            if selected_language == "Kannada":
                if char in kannada_chars_to_ignore: continue
            elif selected_language == "Hindi":
                if char in hindi_chars_to_ignore: continue
            
            chars.append(char)
        
        # Calculate grid positions
        cols = 5  # Number of columns in the grid

        script_dir = os.path.dirname(os.path.abspath(__file__))
        for i, char in enumerate(chars):
            try:
                image_path = None
                if selected_language == "Kannada":
                    char_folder = os.path.join(script_dir, 'Kannada Dataset', char)
                    if os.path.isdir(char_folder):
                        images_in_folder = [f for f in os.listdir(char_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                        if images_in_folder:
                            image_path = os.path.join(char_folder, images_in_folder[0])
                elif selected_language == "Hindi":
                    char_folder = os.path.join(script_dir, 'HindiSignImages', char)
                    if os.path.isdir(char_folder):
                        images_in_folder = [f for f in os.listdir(char_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                        if images_in_folder:
                            image_path = os.path.join(char_folder, images_in_folder[0])
                else:
                    image_path = os.path.join(script_dir, f"dataset/{char}.jpeg")

                if image_path and os.path.exists(image_path):
                    found_any = True
                    
                    # Calculate row and column position
                    row = i // cols
                    col = i % cols
                    
                    # Load and process image
                    img = Image.open(image_path)
                    img = img.resize((140, 140), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self.photo_references.append(photo)
                    
                    # Create card for the image
                    card = ImageCard(self.scrollable_frame, photo, char)
                    card.grid(row=row, column=col, padx=10, pady=10)
                else:
                     print(f"Image not found for character '{char}' in language '{selected_language}'")
                    
            except Exception as e:
                print(f"Error loading image for '{char}': {e}")
        
        if not found_any:
            message = ttk.Label(
                self.scrollable_frame,
                text="No sign language images found.\nPlease check your dataset folder.",
                style="Premium.TLabel",
                font=("Segoe UI", 12)
            )
            message.grid(row=0, column=0, columnspan=5, pady=50)

def main(root=None):
    if root:
        app = SignLanguageViewer(root)
    else:
        root = tk.Tk()
        app = SignLanguageViewer(root)
        root.mainloop()

if __name__ == '__main__':
    main()
