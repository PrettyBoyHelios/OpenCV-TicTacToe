from __future__ import print_function
import numpy as np
import cv2 as cv
import tkinter as tk
import threading
from PIL import Image, ImageTk


class TicTacToeApp:
    def __init__(self, vs, w, h):
        self.vs = vs
        self.h = h
        self.w = w
        self.frame = None
        self.thread = None
        self.stopEvent = None

        self.root = tk.Tk()
        self.panel = None
        btn = tk.Button(self.root, text="PC Turn!", command=self.computer_turn)
        btn.pack(side="bottom", fill="both", expand="no", padx=10, pady=10)

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        self.root.wm_title("TicTacToe OpenCV")
        self.root.protocol("WM_DELETE_WINDOW", self.onClose)
        self.edge_detection = False

    def computer_turn(self):
        self.edge_detection = ~self.edge_detection

    def videoLoop(self):
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                ret, self.frame = self.vs.read()
                self.frame = cv.resize(self.frame, (640, 360), interpolation=cv.INTER_LINEAR)

                # OpenCV represents images in BGR order transformation to RGB in PIL is required
                image = cv.cvtColor(self.frame, cv.COLOR_BGR2RGB)
                image = cv.cvtColor(self.frame, cv.COLOR_BGR2RGB)
                if self.edge_detection:
                    image = cv.Canny(image, 100, 200)
                image = ImageTk.PhotoImage(image=Image.fromarray(image))

                if self.panel is None:
                    self.panel = tk.Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=10, pady=10)
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

        except Exception as e:
            print("[INFO] caught a RuntimeError")
            print(e.with_traceback())

    def onClose(self):
        print("[INFO] closing...")
        self.stopEvent.set()
        self.vs.release()
        self.root.destroy()