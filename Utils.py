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

    def generateTicTacToe(self, img):
        ttt = np.chararray((3, 3))
        ttt[:] = 'a'
        saw_white = False
        #print(img.shape)
        for i in range(0, 3):
            for j in range(0, 3):
                cross = 0
                saw_white = False
                r = 120 * i + 60
                for c in range(213 * j, 213 * (j + 1)):
                    #print(r, c, saw_white)
                    if img[r, c] == 1 and not saw_white:
                        cross += 1
                        saw_white = True
                    elif img[r, c] == 0:
                        saw_white = False

                if cross == 1:
                    ttt[i, j] = b'x'
                elif cross == 2:
                    ttt[i, j] = b'o'
                else:
                    ttt[i, j] = b'a'

        return ttt

    def next_move(self, img):
        cv.imshow("cosa", img)

        tic_tac_toe = self.generateTicTacToe(img)

        print(tic_tac_toe)

        final_q = -1

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


def getColor(color, or_image, ignore_after, open_image, debug=False):
    image = or_image
    h, w, c = image.shape

    colors = {'blue': 0, 'green': 1, 'red': 2}
    eliminating_colors = list()
    for entry in colors:
        if not entry == color:
            eliminating_colors.append(colors[entry])

    eliminating_colors = np.array(eliminating_colors)
    #print(eliminating_colors)
    image = cv.medianBlur(image, 9)
    if debug:
        cv.imshow("getColor::Original", image)
    image_r = image

    for i in range(w):
        for j in range(h):
            n = np.argmax(image_r[j, i])
            if n == colors[color]:
                    image_r[j, i, colors[color]] = 255
            else:
                image_r[j, i, colors[color]] = 0
    image_r[:, :, eliminating_colors] = 0
    cv.imshow("pROCESSED", image_r)
    imgray = cv.cvtColor(image_r, cv.COLOR_BGR2GRAY) # Image to grayscale

    ret, image = cv.threshold(imgray, ignore_after, 255, cv.THRESH_BINARY) # Image binarization

    cv.imshow("Binarized", image)

    if open_image:
        # Structuring Element, cross at 45°
        mask_size = 40
        mask = cv.getStructuringElement(cv.MORPH_CROSS, (mask_size, mask_size)) # Structural element, a cross (+)
        rows, cols = mask.shape
        rot = cv.getRotationMatrix2D((cols/2, rows/2), 45, 1)
        mask = cv.warpAffine(mask, rot, mask.shape)
        # Open Image
        image = cv.morphologyEx(image, cv.MORPH_OPEN, mask)
        cv.imshow("getColor Opening Result", image) if debug else None
    return image


def getTicTacBoard(or_image, mask_size=10, debug=False):
    image = or_image
    image = getColor('red', image, 70, False)
    if debug:
        cv.imshow("getTicTacBoard::Original Image", image)

    # Image opening with a circle to get points
    mask = cv.getStructuringElement(cv.MORPH_ELLIPSE, (mask_size, mask_size))  # Structural element, a cross (+)
    image = cv.morphologyEx(image, cv.MORPH_OPEN, mask)
    if debug:
        cv.imshow("getTicTacBoard::Opened Image", image) if debug else None

    # Labelling of binary image's components
    num_labels, labels = cv.connectedComponents(image)

    if debug:
        cv.imshow("getTicTacBoard::Labelled Image", labels) if debug else None

    points = getPoints(labels)
    print("Points at ", points)
    return points


def getPoints(or_image):
    points = list()
    for i in range(1, 5):
        indexes = np.argwhere(or_image == i)
        points.append(getPoint(indexes))
    points = np.array(points)
    return points


def getPoint(label_index):
    pos = len(label_index)/2
    return label_index[int(pos)]


def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    print("s: ", s)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    print("d: ", diff)
    rect[3] = pts[np.argmin(diff)]
    rect[1] = pts[np.argmax(diff)]

    # For some reason x and y are inverted, this flips the array
    order = np.array([1, 0])
    rect = rect[:, order]
    # return the ordered coordinates
    return rect


def warpTicTacToe(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    print(image.shape)
    cv.imshow("Warp__Image", image)
    rect = order_points(pts)
    print("rect", rect)
    (tl, tr, br, bl) = rect

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # compute the perspective transform matrix and then apply it
    M = cv.getPerspectiveTransform(rect, dst)
    warped = cv.warpPerspective(image, M, (maxWidth, maxHeight))
    # return the warped image
    return warped


