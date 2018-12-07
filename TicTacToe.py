import tkinter as tk
import cv2 as cv
import numpy as np
#from AppManager import TicTacToeApp
from AppManager import TicTacToeApp
from imutils.video import VideoStream


webcam = cv.VideoCapture(0)
# webcam = VideoStream(0)
app = TicTacToeApp(webcam, 640, 360)

app.root.mainloop()

