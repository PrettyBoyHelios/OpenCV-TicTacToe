import cv2 as cv
from AppManager import TicTacToeApp


webcam = cv.VideoCapture(0)
app = TicTacToeApp(webcam, (640, 360), debug=False)
app.set_red_calibration(200, 250)
app.root.mainloop()

