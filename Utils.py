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
    colors = {'blue': 0, 'green': 1, 'red': 2}
    eliminating_colors = list()
    for entry in colors:
        if not entry == color:
            eliminating_colors.append(colors[entry])

    eliminating_colors = np.array(eliminating_colors)
    #print(eliminating_colors)
    image = cv.medianBlur(image, 9)
    #cv.imshow("Original", image)
    image_r = image
    for i in range(640):
        for j in range(360):
            n = np.argmax(image_r[j, i])
            if n == 2:
                    image_r[j, i, colors[color]] = 255
            else:
                image_r[j, i, colors[color]] = 0
    image_r[:, :, eliminating_colors] = 0
    #cv.imshow("pROCESSED", image_r)
    imgray = cv.cvtColor(image_r, cv.COLOR_BGR2GRAY)
    # print(imgray.shape, "imgray")
    #cv.imshow("Gray", imgray)
    ret, image = cv.threshold(imgray, ignore_after, 255, cv.THRESH_BINARY)
    #th2 = cv.adaptiveThreshold(imgray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 11, 2)
    # print(th2.shape)
    #cv.imshow("TH2", th2)
    # print(image_r)
    #cv.imshow("RedFilter", image)

    if open_image:
        # Structuring Element, cross at 45°
        mask_size = 110
        mask = cv.getStructuringElement(cv.MORPH_CROSS, (mask_size, mask_size))
        rows, cols = mask.shape
        rot = cv.getRotationMatrix2D((cols/2, rows/10), 45, 1)

        dst = cv.warpAffine(mask, rot, mask.shape)
        #print(dst)
        # Open Image
        opening = cv.morphologyEx(image, cv.MORPH_OPEN, mask)
        cv.imshow("Opening Result", opening)
        return opening
    else:
        return image


def generateTicTacToe(img):
    ttt = np.chararray((3, 3))
    ttt[:] = 'a'
    for i in range(0, 3):
        for j in range(0, 3):
            cross = 0
            saw_white = False
            r = 120 * i + 60
            for c in range(213 * j, 213 * (j + 1)):
                if img[r, c] == 255 and not saw_white:
                    cross += 1
                    saw_white = True
                elif img[r, c] == 0:
                    saw_white = False

            if cross == 1:
                ttt[i, j] = 'x'
            elif cross == 2:
                ttt[i, j] = 'o'

    return ttt

