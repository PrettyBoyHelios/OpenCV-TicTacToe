import tkinter as tk
import cv2 as cv
import numpy as np
from PIL import Image, ImageTk


class Player:
    INF = 99999999999999

    def evaluate_position(self, t):
        vd1 = 0
        vd2 = 0

        for x in range(0, 3):
            vr = vc = 0
            for y in range(0, 3):
                if t[x, y] == b'o':
                    vr += 1
                elif t[x, y] == b'x':
                    vr -= 1

                if t[y, x] == b'o':
                    vc += 1
                elif t[y, x] == b'x':
                    vc -= 1

            if t[x, x] == b'o':
                vd1 += 1
            if t[x, x] == b'x':
                vd1 -= 1

            if t[x, 2 - x] == b'o':
                vd2 += 1
            if t[x, 2 - x] == b'x':
                vd2 -= 1

            if vr == 3 or vc == 3:
                return 1
            if vr == -3 or vc == -3:
                return -1

        if vd1 == 3 or vd2 == 3:
            return 1

        if vd1 == -3 or vd2 == -3:
            return -1

        return 0

    def dfs(self, ttt, level, move):

        if level == 4:
            return 0

        ev = self.evaluate_position(ttt)

        if ev == 1:
            if level == 1:
                return self.INF
            return 1
        elif ev == -1:
            if level == 2:
                return -self.INF
            return -1

        total = 0
        for a in range(0, 3):
            for b in range(0, 3):
                if ttt[a, b] == b'a':
                    ttt[a, b] = move

                    total += self.dfs(ttt, level + 1, b'o' if move == b'x' else b'x')
                    ttt[a, b] = b'a'

        return total

    def next_move(self, tic_tac_toe):
        final_q = -1

        r = int(input())
        c = int(input())

        tic_tac_toe[r, c] = b'x'

        r = -1
        c = -1

        for i in range(0, 3):
            for j in range(0, 3):
                if tic_tac_toe[i, j] == b'a':
                    tic_tac_toe[i, j] = b'o'
                    q = self.dfs(tic_tac_toe, 1, b'x')
                    if q > final_q:
                        r = i
                        c = j
                        final_q = q

                    tic_tac_toe[i, j] = b'a'
        return r, c



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
        mask = cv.getStructuringElement(cv.MORPH_CROSS, (mask_size, mask_size)) # Structural element, a cross (+)
        rows, cols = mask.shape
        rot = cv.getRotationMatrix2D((cols/2, rows/2), 45, 1)
        mask = cv.warpAffine(mask, rot, mask.shape)
        # Open Image
        image = cv.morphologyEx(image, cv.MORPH_OPEN, mask)
        #cv.imshow("Opening Result", image)

    return image

