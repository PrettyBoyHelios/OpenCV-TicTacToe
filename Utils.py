import tkinter as tk
import cv2 as cv
import numpy as np
from AppManager import TicTacToeApp
from PIL import Image, ImageTk


def getColor(color, image, ignore_after):
    colors = {'blue':0, 'green': 1, 'red': 2 }
    eliminating_colors = 
    image = cv.medianBlur(image, 9)
    cv.imshow("Original", image)
    image_r = image
    print(image_r.shape)
    for i in range(640):
        for j in range(360):
            n = np.argmax(image_r[j, i])
            if n == 2:
                    image_r[j, i, 2] = 255
            else:
                image_r[j, i, 2] = 0
    image_r[:, :, 0:2] = 0
    cv.imshow("pROCESSED", image_r)
    imgray = cv.cvtColor(image_r, cv.COLOR_BGR2GRAY)
    print(imgray.shape, "imgray")
    cv.imshow("Gray", imgray)
    ret, th2 = cv.threshold(imgray, ignore_after, 255, cv.THRESH_BINARY)
    #th2 = cv.adaptiveThreshold(imgray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 11, 2)
    print(th2.shape)
    cv.imshow("TH2", th2)
    print(image_r)
    cv.imshow("RedFilter", image)
    mask_size = 110
    img = cv.getStructuringElement(cv.MORPH_CROSS, (mask_size, mask_size))
    rows, cols = img.shape
    rot = cv.getRotationMatrix2D((cols/2, rows/10), 45, 1)
    print(img)
    dst = None
    dst = cv.warpAffine(img, rot, img.shape)
    opening = cv.morphologyEx(image, cv.MORPH_OPEN, img)
    print(opening.size)
    cv.imshow("Opening Result", opening)
    return opening