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
    def __init__(self, vs, w, h, debug=False):
        self.vs = vs
        self.h = h
        self.w = w
        self.dbg = debug
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.isSetUp = False
        self.coordinates = None

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
        if self.isSetUp:
            self.img = cv.resize(self.frame, (640, 360), interpolation=cv.INTER_LINEAR_EXACT)
            self.img = cv.cvtColor(self.frame, cv.COLOR_BGR2RGB)
            print("Coordinates", self.coordinates)
            player = Utils.Player()
            #image = self.process_image()
            image = self.img
            image = self.process_image(image)
            cv.imshow("TicTacToe::After ProcessImage", image)
            image = Utils.warpTicTacToe(image, self.coordinates, True)
            r, c = player.next_move(image)
            print("Put a O at: ", r, c)
        else:
            self.img = cv.resize(self.img, (640, 360), interpolation=cv.INTER_LINEAR_EXACT)
            #self.img = cv.cvtColor(self.img, cv.COLOR_BGR2RGB)
            cv.imshow("Original", self.img)
            self.coordinates = Utils.getTicTacBoard(self.img, (140, 250), debug=True)
            self.isSetUp = True

    def setConfig(self, config):
        self.usePattern = config['pattern']


    def videoLoop(self):
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                ret, self.frame = self.vs.read()
                self.frame = cv.resize(self.frame, (640, 360), interpolation=cv.INTER_LINEAR_EXACT)
                self.img = self.frame
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

    def process_image(self, image):
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        image = Utils.getColor('red', image, 70, False, self.dbg)
        cv.imwrite("images/lol" + str(datetime.datetime.now())+".png", image)
        return image

    def preprocessimage(self, image):
        return image
