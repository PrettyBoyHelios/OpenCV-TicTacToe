import tkinter as tk
import cv2 as cv
import numpy as np
from PIL import Image, ImageTk


def getColor(color, image, ignore_after, open_image):
    h, w, c = image.shape
    #print(h, w)
    colors = {'blue': 0, 'green': 1, 'red': 2}
    eliminating_colors = list()
    for entry in colors:
        if not entry == color:
            eliminating_colors.append(colors[entry])

    eliminating_colors = np.array(eliminating_colors)
    #print(eliminating_colors)
    image = cv.medianBlur(image, 9)
    cv.imshow("Original", image)
    image_r = image
    for i in range(w):
        for j in range(h):
            n = np.argmax(image_r[j, i])
            if n == colors[color]:
                    image_r[j, i, colors[color]] = 255
            else:
                image_r[j, i, colors[color]] = 0
    image_r[:, :, eliminating_colors] = 0
    #cv.imshow("pROCESSED", image_r)
    imgray = cv.cvtColor(image_r, cv.COLOR_BGR2GRAY) # Image to grayscale

    ret, image = cv.threshold(imgray, ignore_after, 255, cv.THRESH_BINARY) # Image binarization

    if open_image:
        # Structuring Element, cross at 45°
        mask_size = 40
        mask = cv.getStructuringElement(cv.MORPH_CROSS, (mask_size, mask_size))
        print(mask)
        rows, cols = mask.shape
        rot = cv.getRotationMatrix2D((cols/2, rows/2), 45, 1)

        dst = cv.warpAffine(mask, rot, mask.shape)
        print(dst)
        # Open Image
        image = cv.morphologyEx(image, cv.MORPH_OPEN, mask)
        #cv.imshow("Opening Result", image)

    return image

