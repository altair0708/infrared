import sys
from PyQt5.QtWidgets import QApplication,  QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from resource import *


class MyMainWindow(Ui_MainWindow):
	def __init__(self, parent=None):
		super().__init__()
		self.setupUi(self)


app = QApplication(sys.argv)

mainWindow = MyMainWindow()

'''
newthread = QtCore.QThread()

calculatethread = CalculateThread()

calculatethread.moveToThread(newthread)

mainWindow.playthread.TocalculateSignal.connect(calculatethread.get_picture)
mainWindow.temperatureSignal.connect(calculatethread.receive_temperature)

mainWindow.showGray.clicked.connect(calculatethread.draw_gray)
mainWindow.show3D.clicked.connect(calculatethread.draw_3D)
mainWindow.showContour.clicked.connect(calculatethread.draw_contour)

mainWindow.exitWindow.clicked.connect(newthread.wait)
mainWindow.exitWindow.clicked.connect(newthread.quit)

newthread.start()
'''

mainWindow.show()

sys.exit(app.exec())
