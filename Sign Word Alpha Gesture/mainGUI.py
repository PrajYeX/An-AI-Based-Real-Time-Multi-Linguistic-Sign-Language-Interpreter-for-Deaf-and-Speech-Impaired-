import sys
import os.path
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import WebCam
from WordToSign import main as WordToSign_main
from gesture.GestureCamera import detect as GestureCameraDetector
from VoiceToSign import main as VoiceToSign_main

class ModernDashboardUI:
    def __init__(self, top=None):
        self.root = top
        # Modern color scheme with gradients
        self.colors = {
            'primary': '#4834d4',
            'secondary': '#686de0',
            'accent': '#be2edd',
            'background': '#f1f2f6',
            'card_bg': '#ffffff',
            'text_dark': '#2d3436',
            'text_light': '#ffffff',
            'success': '#6ab04c',
            'sidebar': '#30336b'
        }

        # Configure window
        w, h = 1200, 750
        ws = top.winfo_screenwidth()
        hs = top.winfo_screenheight()
        x, y = (ws/2)-(w/2), (hs/2)-(h/2)
        top.geometry(f'{w}x{h}+{int(x)}+{int(y)}')
        top.title("Sign Language Recognition Dashboard")
        top.configure(background=self.colors['background'])

        # Custom fonts
        self.title_font = tkfont.Font(family="Helvetica", size=32, weight="bold")
        self.heading_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
        self.subtitle_font = tkfont.Font(family="Helvetica", size=14)
        self.label_font = tkfont.Font(family="Helvetica", size=12)

        # Create main layout
        self.create_layout()

    def create_layout(self):
        # Create sidebar
        self.sidebar = tk.Frame(self.root, bg=self.colors['sidebar'], width=250)
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)
        
        # Create main content area
        self.main_content = tk.Frame(self.root, bg=self.colors['background'])
        self.main_content.pack(side='right', fill='both', expand=True)

        # Add sidebar content
        self.create_sidebar_content()
        
        # Add main content
        self.create_main_content()

    def create_sidebar_content(self):
        # Logo/Brand section
        logo_frame = tk.Frame(self.sidebar, bg=self.colors['sidebar'])
        logo_frame.pack(pady=30)
        
        logo_label = tk.Label(logo_frame, bg=self.colors['sidebar'])
        photo_location = os.path.join(sys.path[0], "Images/icon.png")
        self.logo_image = tk.PhotoImage(file=photo_location)
        logo_label.configure(image=self.logo_image)
        logo_label.pack()

        # Navigation menu
        menu_items = ['Dashboard']
        for item in menu_items:
            self.create_menu_item(item)

    def create_menu_item(self, text):
        menu_frame = tk.Frame(self.sidebar, bg=self.colors['sidebar'])
        menu_frame.pack(fill='x', pady=5)
        menu_frame.bind('<Enter>', lambda e: self.on_menu_hover(menu_frame, True))
        menu_frame.bind('<Leave>', lambda e: self.on_menu_hover(menu_frame, False))

        menu_label = tk.Label(
            menu_frame,
            text=text,
            font=self.subtitle_font,
            fg=self.colors['text_light'],
            bg=self.colors['sidebar'],
            padx=20,
            pady=10
        )
        menu_label.pack(fill='x')

    def create_main_content(self):
        # Header section
        header = tk.Frame(self.main_content, bg=self.colors['background'])
        header.pack(fill='x', padx=30, pady=30)

        title = tk.Label(
            header,
            text="Sign Language Recognition",
            font=self.title_font,
            fg=self.colors['primary'],
            bg=self.colors['background']
        )
        title.pack(anchor='w')

        subtitle = tk.Label(
            header,
            text="Select a recognition mode to begin",
            font=self.subtitle_font,
            fg=self.colors['text_dark'],
            bg=self.colors['background']
        )
        subtitle.pack(anchor='w', pady=(5, 0))

        # Create feature cards container
        self.create_feature_cards()

        # Create status section
        self.create_status_section()

    def create_feature_cards(self):
        cards_frame = tk.Frame(self.main_content, bg=self.colors['background'])
        cards_frame.pack(fill='x', padx=30)
        
        # Configure grid
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        cards_frame.grid_columnconfigure(2, weight=1)
        cards_frame.grid_columnconfigure(3, weight=1)

        # Create feature cards with gradients
        features = [
            {
                'title': 'Gesture Detection',
                'description': 'Recognize hand gestures in real-time',
                'image': 'Images/images icon.png',
                'gradient': ['#6c5ce7', '#a55eea'],
                'command': self.handle_gesture_detection
            },
            {
                'title': 'Alphabet Recognition',
                'description': 'Detect and translate sign language alphabet',
                'image': 'Images/webcam icon.png',
                'gradient': ['#00b894', '#00cec9'],
                'command': self.handle_webcam
            },
            {
                'title': 'Text To Gesture',
                'description': 'Convert Word to Sign',
                'image': 'Images/3 ICON.png',
                'gradient': ['#fd79a8', '#e84393'],
                'command': self.handle_text_to_sign
            },
            {
                'title': 'Voice to Sign',
                'description': 'Speak a word to see the sign translation',
                'image': 'Images/4 ICON.png',
                'gradient': ['#ff7675', '#d63031'],
                'command': self.handle_voice_to_sign
            }
        ]

        for idx, feature in enumerate(features):
            self.create_gradient_card(cards_frame, feature, idx)

    def create_gradient_card(self, parent, feature, column):
        # Create card with gradient effect
        card = tk.Frame(
            parent,
            bg=self.colors['card_bg'],
            highlightbackground=feature['gradient'][0],
            highlightthickness=2,
        )
        card.grid(row=0, column=column, padx=15, pady=15, sticky='nsew')
        
        # Gradient header
        header = tk.Canvas(card, height=100, bg=feature['gradient'][0], highlightthickness=0)
        header.pack(fill='x')

        # Image
        img_label = tk.Label(card, bg=self.colors['card_bg'])
        photo_location = os.path.join(sys.path[0], feature['image'])
        image = tk.PhotoImage(file=photo_location)
        img_label.image = image
        img_label.configure(image=image)
        img_label.pack(pady=(20, 10))

        # Title
        title_label = tk.Label(
            card,
            text=feature['title'],
            font=self.heading_font,
            fg=self.colors['text_dark'],
            bg=self.colors['card_bg']
        )
        title_label.pack(pady=(0, 10))

        # Description
        desc_label = tk.Label(
            card,
            text=feature['description'],
            font=self.label_font,
            fg=self.colors['text_dark'],
            bg=self.colors['card_bg'],
            wraplength=250
        )
        desc_label.pack(pady=(0, 20))

        # Button
        btn = tk.Button(
            card,
            text="Launch",
            font=self.label_font,
            bg=feature['gradient'][0],
            fg='#000000',
            relief='solid',
            borderwidth=2,
            activebackground=feature['gradient'][1],
            activeforeground='#000000',
            padx=20,
            pady=10,
            command=feature['command']
        )
        btn.pack(pady=(0, 20))

        # Add hover effects
        card.bind('<Enter>', lambda e: self.on_card_hover(card, btn, feature['gradient'][0], True))
        card.bind('<Leave>', lambda e: self.on_card_hover(card, btn, feature['gradient'][0], False))

    def create_status_section(self):
        status_frame = tk.Frame(self.main_content, bg=self.colors['card_bg'])
        status_frame.pack(fill='x', padx=30, pady=30)

        status_label = tk.Label(
            status_frame,
            text="System Status: Ready",
            font=self.subtitle_font,
            fg=self.colors['success'],
            bg=self.colors['card_bg'],
            pady=15
        )
        status_label.pack(side='left', padx=20)

    def on_menu_hover(self, frame, is_hover):
        frame.configure(bg=self.colors['secondary'] if is_hover else self.colors['sidebar'])
        for child in frame.winfo_children():
            child.configure(bg=self.colors['secondary'] if is_hover else self.colors['sidebar'])

    def on_card_hover(self, card, btn, gradient_color, is_hover):
        if is_hover:
            card.configure(highlightbackground=gradient_color)
            btn.configure(bg=self.colors['secondary'])
        else:
            card.configure(highlightbackground=gradient_color)
            btn.configure(bg=gradient_color)

    # Event handlers
    def handle_gesture_detection(self):
        threading.Thread(target=GestureCameraDetector, args=(0,)).start()

    def handle_webcam(self):
        webcam_window = tk.Toplevel(self.root)
        app = WebCam.ModernApplication(webcam_window)

    def handle_text_to_sign(self):
        numbers_window = tk.Toplevel(self.root)
        WordToSign_main(numbers_window)

    def handle_voice_to_sign(self):
        voice_window = tk.Toplevel(self.root)
        VoiceToSign_main(voice_window)

def vp_start_gui():
    root = tk.Tk()
    app = ModernDashboardUI(root)
    root.mainloop()

if __name__ == '__main__':
    vp_start_gui()