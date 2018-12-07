from __future__ import print_function
import numpy as np
import cv2 as cv
import tkinter as tk
import threading
from PIL import Image, ImageTk
import traceback
import datetime
import Utils


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
        self.process_image()

    def setConfig(self, config):
        self.usePattern = config['pattern']


    def videoLoop(self):
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                ret, self.frame = self.vs.read()
                self.frame = cv.resize(self.frame, (640, 360), interpolation=cv.INTER_LINEAR_EXACT)
                self.frame = cv.cvtColor(self.frame, cv.COLOR_BGR2RGB)
                # OpenCV represents images in BGR order transformation to RGB in PIL is required

                image = ImageTk.PhotoImage(image=Image.fromarray(self.frame))

                if self.panel is None:
                    self.panel = tk.Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=10, pady=10)
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

        except Exception as e:
            print("[INFO] caught a RuntimeError")
            print(e)
            traceback.print_exc()

    def onClose(self):
        print("[INFO] closing...")
        self.stopEvent.set()
        self.vs.release()
        cv.destroyAllWindows()
        self.root.destroy()

    def process_image(self):
        image = self.frame
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        image = Utils.getColor('blue', image, 70, False)
        cv.imwrite("images/lol" + str(datetime.datetime.now())+".png", image)

    def preprocessimage(self, image):

        return image