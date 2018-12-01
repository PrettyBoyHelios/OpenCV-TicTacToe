import tkinter as tk
import cv2 as cv
import numpy as np


# root = tk.Tk()
# root.bind('<Escape>', lambda e: root.quit())
# lmain = tk.Label(root, text="Hola!")
# lmain.pack()
while(True):
    webcam = cv.VideoCapture(0)
    ret, frame = webcam.read()
    frame = cv.resize(frame,(640, 360), interpolation=cv.INTER_LINEAR)
    gray_image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    filter = cv.Canny(frame, 180, 230)
    cv.imshow('frame', filter)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# root.mainloop()

