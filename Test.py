import tkinter as tk
import cv2 as cv
import numpy as np
from AppManager import TicTacToeApp
from PIL import Image, ImageTk
import Utils


# Image To grid representation Test
image = cv.imread("data/test_grid.jpg", cv.IMREAD_COLOR)
image = cv.resize(image, (640, 360), interpolation=cv.INTER_LINEAR_EXACT)
image = Utils.getColor('red', image, 70, False)
#print(image)
cv.imshow("cosa", image)
cv.imwrite("images/test_grid.png", image)
Utils.generateTicTacToe(image)


# getColor Testing

np.set_printoptions(threshold=np.inf)


image = cv.imread("data/test_grid.jpg", cv.IMREAD_COLOR)
image = cv.resize(image, (640, 360), interpolation=cv.INTER_LINEAR_EXACT)
image = getColor('red', image, 70, True)
cv.imshow("Result", image)
cv.waitKey(0)
cv.destroyAllWindows()