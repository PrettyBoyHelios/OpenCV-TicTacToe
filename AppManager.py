from __future__ import print_function
import numpy as np
import cv2 as cv
import tkinter as tk
import threading
from PIL import Image, ImageTk
import traceback
import datetime
import Utils
from tkinter import StringVar


class TicTacToeApp:
    #def __init__(self, vs, w, h, debug=False):
    def __init__(self, vs, dimensions, debug=False):
        self.vs = vs
        self.h = dimensions[1]
        self.w = dimensions[0]
        self.dbg = debug
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.isSetUp = False
        self.coordinates = None
        self.redMin = 50
        self.redMax = 254
        self.current_state = 0


        self.isFirstTurn = False

        self.root = tk.Tk()
        self.current_message = StringVar()
        self.panel = None
        btn = tk.Button(self.root, text="PC Turn!", command=self.computer_turn)
        btn.pack(side="bottom", fill="both", expand="no", padx=10, pady=10)
        msg_label = tk.Label(self.root, textvariable=self.current_message)
        msg_label.pack(side="bottom", fill="both", expand="no", padx=10, pady=10)

        self.current_message.set("Please, press the \"PC Turn!\" button when the board is blank to calibrate the board.")

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        self.root.wm_title("TicTacToe OpenCV")
        self.root.protocol("WM_DELETE_WINDOW", self.onClose)
        self.edge_detection = False

    def computer_turn(self):
        if self.isSetUp:
            self.img = cv.resize(self.img, (self.w, self.h), interpolation=cv.INTER_LINEAR_EXACT)

            if self.dbg:
                cv.imshow("TicTacToe::Image", self.img)
                print("Coordinates", self.coordinates)

            player = Utils.Player()
            image = self.img
            image = self.process_image(image)

            if self.dbg:
                cv.imshow("TicTacToe::After ProcessImage", image)
            image = Utils.warpTicTacToe(image, self.coordinates, True, debug=self.dbg)

            if self.dbg:
                cv.imshow("TicTacToe::After ProcessImage", image)
                cv.imwrite("images/" + str(datetime.datetime.now()) + ".png", image)

            r, c, ev = player.next_move(image)
            self.set_label_text(ev, r, c)
        else:
            self.img = cv.resize(self.img, (self.w, self.h), interpolation=cv.INTER_LINEAR_EXACT)

            if self.dbg:
                cv.imshow("Original", self.img)

            self.coordinates = Utils.getTicTacBoard(self.img, (self.redMin, self.redMax), debug=self.dbg)
            self.isSetUp = True
            self.current_message.set("Put your 'X' in the board and press to play!")

    def setConfig(self, config):
        self.usePattern = config['pattern']

    def videoLoop(self):
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                ret, self.frame = self.vs.read()
                self.frame = cv.resize(self.frame, (self.w, self.h), interpolation=cv.INTER_LINEAR_EXACT)
                self.img = self.frame.copy()
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

    def set_red_calibration(self, minRed, maxRed):
        self.redMin = minRed
        self.redMax = maxRed

    def set_label_text(self, ev, r, c):
        if ev == 0:
            string = "Please, put an 'O' at (r, c) (" + str(r + 1) + ", " + str(
                c + 1) + "), make your move, and then click the button again!"
            self.current_message.set(string)
        elif ev == 1:
            string = "Please, put an 'O' at (r, c) (" + str(r + 1) + ", " + str(c + 1) + "). I won! :)"
            self.current_message.set(string)
        elif ev == -1:
            self.current_message.set("You won! Good game!")

    def process_image(self, image):
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        image = Utils.getColor('red', image, self.redMin, self.redMax, False, flip=True, debug=self.dbg)
        return image
