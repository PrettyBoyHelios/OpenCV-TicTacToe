import tkinter as tk
import cv2 as cv
import numpy as np
from AppManager import TicTacToeApp
from PIL import Image, ImageTk


webcam = cv.VideoCapture(0)
webcam.release()
# while True:
#     ret, image = webcam.read()
#     image = cv.resize(image, (320, 180), interpolation=cv.INTER_LINEAR_EXACT)
#
#     # OpenCV represents images in BGR order transformation to RGB in PIL is required
#     image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
#
#     normalizedImg = np.zeros((320, 180))
#     normalizedImg = cv.normalize(image, normalizedImg, 0, 255, cv.NORM_MINMAX)
#     image = normalizedImg
#
#     ret, image_bin = cv.threshold(image, 64, 255, cv.THRESH_BINARY)
#     im2, contours, hierarchy = cv.findContours(image_bin, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
#     image = cv.drawContours(image_bin, contours, -1, (0, 255, 0), 5)
#     #image = ImageTk.PhotoImage(image=Image.fromarray(image))
#     cv.imshow('Image', image)