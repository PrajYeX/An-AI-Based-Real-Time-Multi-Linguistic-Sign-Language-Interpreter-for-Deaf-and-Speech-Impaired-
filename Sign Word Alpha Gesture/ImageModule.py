

import sys
import cv2

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

import numpy as np
import cv2

from PIL import ImageTk,Image
from tkinter import filedialog,messagebox

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import os.path

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    global prog_location
    prog_call = sys.argv[0]
    prog_location = os.path.split(prog_call)[0]
    root = tk.Tk()
    top = ImageModule (root)
    root.mainloop()

w = None
def create_ImageModule(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    global prog_location
    prog_call = sys.argv[0]
    prog_location = os.path.split(prog_call)[0]
    rt = root
    w = tk.Toplevel (root)
    top = ImageModule (w)
    return (w, top)

def destroy_ImageModule():
    global w
    w.destroy()
    w = None

class ImageModule:
    def __init__(self, top=None):
        self.directory = "model/"


        minValue = 70

        def function(path,flip):    
            frame = cv2.imread(path)
            frame = cv2.flip(frame, flip)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray,(5,5),2)

            th3 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
            ret, res = cv2.threshold(th3, minValue, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
            return res


        global ImageFileName
        ImageFileName = None
        def chooseImage(event):
            global ImageFileName
            ##Get File directory from user
            ImageFileName =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("all files","*.*"),("jpeg files","*.jpg"),("png files","*.png")))
            ###Identify the name of file
            image = Image.open(ImageFileName)
            image = image.resize((800, 600), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            self.lblImage.configure(image=photo)
            self.lblImage.image = photo


        def btnExit(event):
            top.destroy()
            import mainGUI
            mainGUI.vp_start_gui()



        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font10 = "-family {Segoe UI} -size 24 -weight bold -slant "  \
            "roman -underline 0 -overstrike 0"
        font11 = "-family {Segoe UI} -size 18 -weight bold -slant "  \
            "roman -underline 0 -overstrike 0"

        top.geometry("1324x817+310+102")
        top.title("New Toplevel")
        top.state('zoomed')
        top.configure(background="#ffffff")

        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.385, rely=0.037, height=60, width=715)
        self.Label1.configure(background="#ffffff")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font=font10)
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''Sign Language Detection System''')

        self.Label2 = tk.Label(top)
        self.Label2.place(relx=0.083, rely=0.049, height=154, width=250)
        self.Label2.configure(background="#ffffff")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="#000000")
        photo_location = os.path.join(prog_location,"images/icon.png")
        self._img0 = tk.PhotoImage(file=photo_location)
        self.Label2.configure(image=self._img0)
        self.Label2.configure(text='''Label''')

        self.lblImage = tk.Label(top)
        self.lblImage.place(relx=0.317, rely=0.196, height=606, width=852)
        self.lblImage.configure(background="#ffffff")
        self.lblImage.configure(disabledforeground="#a3a3a3")
        self.lblImage.configure(foreground="#000000")
        self.lblImage.configure(relief="ridge")
        self.lblImage.configure(text='''Image''')
        self.lblImage.configure(width=852)

        self.btnChooseImage = tk.Button(top)
        self.btnChooseImage.place(relx=0.068, rely=0.33, height=70, width=225)
        self.btnChooseImage.configure(activebackground="#d63031")
        self.btnChooseImage.configure(activeforeground="#000000")
        self.btnChooseImage.configure(background="#ff1212")
        self.btnChooseImage.configure(disabledforeground="#a3a3a3")
        self.btnChooseImage.configure(font=("Helvetica", 12, "bold"))
        self.btnChooseImage.configure(foreground="#000000")
        self.btnChooseImage.configure(highlightbackground="#d9d9d9")
        self.btnChooseImage.configure(highlightcolor="black")
        self.btnChooseImage.configure(pady="0")
        self.btnChooseImage.configure(text='''Choose Image''')
        self.btnChooseImage.bind('<Button-1>',chooseImage)

        self.btnAlgorithm1 = tk.Button(top)
        self.btnAlgorithm1.place(relx=0.068, rely=0.49, height=70, width=225)
        self.btnAlgorithm1.configure(activebackground="#ccbb00")
        self.btnAlgorithm1.configure(activeforeground="#000000")
        self.btnAlgorithm1.configure(background="#f7ff0f")
        self.btnAlgorithm1.configure(disabledforeground="#a3a3a3")
        self.btnAlgorithm1.configure(font=("Helvetica", 12, "bold"))
        self.btnAlgorithm1.configure(foreground="#000000")
        self.btnAlgorithm1.configure(highlightbackground="#d9d9d9")
        self.btnAlgorithm1.configure(highlightcolor="black")
        self.btnAlgorithm1.configure(pady="0")
        self.btnAlgorithm1.configure(text='''Predict''')


        self.btnAlgorithm2 = tk.Button(top)
        self.btnAlgorithm2.place(relx=0.068, rely=0.636, height=70, width=225)
        self.btnAlgorithm2.configure(activebackground="#ccbb00")
        self.btnAlgorithm2.configure(activeforeground="#000000")
        self.btnAlgorithm2.configure(background="#f7ff0f")
        self.btnAlgorithm2.configure(disabledforeground="#a3a3a3")
        self.btnAlgorithm2.configure(font=("Helvetica", 12, "bold"))
        self.btnAlgorithm2.configure(foreground="#000000")
        self.btnAlgorithm2.configure(highlightbackground="#d9d9d9")
        self.btnAlgorithm2.configure(highlightcolor="black")
        self.btnAlgorithm2.configure(pady="0")
        self.btnAlgorithm2.configure(text='''Flip & Predict''')


        self.btnExit = tk.Button(top)
        self.btnExit.place(relx=0.068, rely=0.808, height=70, width=225)
        self.btnExit.configure(activebackground="#1e6d06")
        self.btnExit.configure(activeforeground="#000000")
        self.btnExit.configure(background="#287a0a")
        self.btnExit.configure(disabledforeground="#a3a3a3")
        self.btnExit.configure(font=("Helvetica", 12, "bold"))
        self.btnExit.configure(foreground="#000000")
        self.btnExit.configure(highlightbackground="#d9d9d9")
        self.btnExit.configure(highlightcolor="black")
        self.btnExit.configure(pady="0")
        self.btnExit.configure(text='''EXIT''')
        self.btnExit.bind('<Button-1>',btnExit)

        

