import tkinter as tk
import cv2 as cv
import numpy as np
from AppManager import TicTacToeApp
from PIL import Image, ImageTk
import Utils
import traceback


# Image To grid representation Test
image = cv.imread("data/test_ttt1.png", cv.IMREAD_GRAYSCALE)
# image = cv.resize(image, (360, 360), interpolation=cv.INTER_LINEAR_EXACT)
# image = Utils.getColor('red', image, 70, False)
#print(image)
# cv.imshow("cosa", image)
# cv.imwrite("images/test_grid.png", image)
player = Utils.Player()

print(player.next_move(image))


# getColor Testing

#np.set_printoptions(threshold=np.inf)

# debug = True
# try:
#     image = cv.imread("data/testTicTacToeAux.jpg", cv.IMREAD_COLOR)
#     image = cv.resize(image, (640, 360), interpolation=cv.INTER_LINEAR_EXACT)
#     cv.imshow("Test::Original", image)
#     points = Utils.getTicTacBoard(image, (140, 250), debug=debug)
#     print("Debug, points ", points)
#     image = Utils.warpTicTacToe(image, points)
#     cv.imshow("Test::Result", image)
#     ## Opening of Second Image
#     image = cv.imread("data/testTicTacToeII.jpg", cv.IMREAD_COLOR)
#     image = cv.resize(image, (640, 360), interpolation=cv.INTER_LINEAR_EXACT)
#     image = Utils.warpTicTacToe(image, points)
#     cv.imshow("WarpedSecondTurn::Result", image)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
#
# except Exception as e:
#     print("[INFO] caught a RuntimeError")
#     print(e)
#     traceback.print_exc()


