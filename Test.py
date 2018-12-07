import tkinter as tk
import cv2 as cv
import numpy as np
from AppManager import TicTacToeApp
from PIL import Image, ImageTk
from Utils import getColor
np.set_printoptions(threshold=np.inf)


image = cv.imread("data/test_grid.jpg", cv.IMREAD_COLOR)
image = cv.resize(image, (640, 360), interpolation=cv.INTER_LINEAR_EXACT)
image = getColor('red', image, 70, True)
cv.imshow("Result", image)
cv.waitKey(0)
cv.destroyAllWindows()