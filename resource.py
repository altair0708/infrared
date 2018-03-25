# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
from childwindow import *
from contourWindow import *
from D3DWindow import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,  QMainWindow
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2
import numpy as np
import time
import sys

class Ui_MainWindow(QMainWindow):
	
	playnumberSignal = QtCore.pyqtSignal(object)
	temperatureSignal = QtCore.pyqtSignal(float, float)
	
	def __init__(self):

		super().__init__()
		
		self.play = False
		self.begin = False
		high = 30.0
		low = 10.0
		self.capcheck = None
		self.hcapcheck = 576
		self.wcapcheck = 720
		self.filename = None
		
		self.newthread1 = QtCore.QThread()
		self.newthread2 = QtCore.QThread()
		
		self.playthread = PlayerThread()  # 播放线程
		self.calculatethread = CalculateThread()
		
		self.playthread.moveToThread(self.newthread1)
		self.calculatethread.moveToThread(self.newthread2)
		
		self.newthread1.start()
		self.newthread2.start()
		
	def setupUi(self, MainWindow):
		
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(820, 680)
		MainWindow.setMinimumSize(QtCore.QSize(820, 680))
		MainWindow.setMaximumSize(QtCore.QSize(820, 680))
		
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		
		self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
		self.layoutWidget.setGeometry(QtCore.QRect(2, 3, 816, 667))
		self.layoutWidget.setObjectName("layoutWidget")
		
		self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
		self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		
		self.verticalLayout_3 = QtWidgets.QVBoxLayout()
		self.verticalLayout_3.setObjectName("verticalLayout_3")
		
		self.videoPlayer = QtWidgets.QLabel(self.layoutWidget)
		self.videoPlayer.setMinimumSize(QtCore.QSize(720, 576))
		self.videoPlayer.setMaximumSize(QtCore.QSize(720, 576))
		self.videoPlayer.setAutoFillBackground(True)
		self.videoPlayer.setObjectName("videoPlayer")
		self.verticalLayout_3.addWidget(self.videoPlayer)
		
		self.horizontalSlider = QtWidgets.QSlider(self.layoutWidget)
		self.horizontalSlider.setMinimumSize(QtCore.QSize(720, 22))
		self.horizontalSlider.setMaximumSize(QtCore.QSize(720, 22))
		self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
		self.horizontalSlider.setObjectName("horizontalSlider")
		self.verticalLayout_3.addWidget(self.horizontalSlider)
		
		self.horizontalLayout = QtWidgets.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		
		self.stopVideoPlay = QtWidgets.QPushButton(self.layoutWidget)
		self.stopVideoPlay.setObjectName("stopVideoPlay")
		self.stopVideoPlay.setDisabled(True)
		self.horizontalLayout.addWidget(self.stopVideoPlay)
		
		spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem)
		
		self.playPause = QtWidgets.QPushButton(self.layoutWidget)
		self.playPause.setObjectName("playPause")
		self.horizontalLayout.addWidget(self.playPause)
		
		spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem1)
		
		self.screenShot = QtWidgets.QPushButton(self.layoutWidget)
		self.screenShot.setObjectName("screenShot")
		self.screenShot.setDisabled(True)
		self.horizontalLayout.addWidget(self.screenShot)
		
		self.verticalLayout_3.addLayout(self.horizontalLayout)
		
		self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_3.setObjectName("horizontalLayout_3")
		
		self.minLabel = QtWidgets.QLabel(self.layoutWidget)
		self.minLabel.setObjectName("minLabel")
		self.horizontalLayout_3.addWidget(self.minLabel)
		
		self.minTemperature = QtWidgets.QDoubleSpinBox(self.layoutWidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.minTemperature.sizePolicy().hasHeightForWidth())
		self.minTemperature.setSizePolicy(sizePolicy)
		self.minTemperature.setObjectName("minTemperature")
		self.minTemperature.setValue(10.0)
		self.minTemperature.setSingleStep(0.1)
		self.horizontalLayout_3.addWidget(self.minTemperature)
		
		self.maxLabel = QtWidgets.QLabel(self.layoutWidget)
		self.maxLabel.setObjectName("maxLabel")
		self.horizontalLayout_3.addWidget(self.maxLabel)
		
		self.maxTemperature = QtWidgets.QDoubleSpinBox(self.layoutWidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.maxTemperature.sizePolicy().hasHeightForWidth())
		self.maxTemperature.setSizePolicy(sizePolicy)
		self.maxTemperature.setObjectName("maxTemperature")
		self.maxTemperature.setValue(30.0)
		self.maxTemperature.setSingleStep(0.1)
		self.horizontalLayout_3.addWidget(self.maxTemperature)
		
		self.verticalLayout_3.addLayout(self.horizontalLayout_3)
		
		self.horizontalLayout_2.addLayout(self.verticalLayout_3)
		
		self.verticalLayout_2 = QtWidgets.QVBoxLayout()
		self.verticalLayout_2.setObjectName("verticalLayout_2")
		
		self.showGray = QtWidgets.QPushButton(self.layoutWidget)
		self.showGray.setObjectName("showGray")
		self.showGray.setDisabled(True)
		self.verticalLayout_2.addWidget(self.showGray)
		
		spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.verticalLayout_2.addItem(spacerItem2)
		
		self.show3D = QtWidgets.QPushButton(self.layoutWidget)
		self.show3D.setObjectName("show3D")
		self.show3D.setDisabled(True)
		self.verticalLayout_2.addWidget(self.show3D)
		
		spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.verticalLayout_2.addItem(spacerItem3)
		
		self.showContour = QtWidgets.QPushButton(self.layoutWidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.showContour.sizePolicy().hasHeightForWidth())
		self.showContour.setSizePolicy(sizePolicy)
		self.showContour.setObjectName("showContour")
		self.showContour.setDisabled(True)
		self.verticalLayout_2.addWidget(self.showContour)
		
		spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.verticalLayout_2.addItem(spacerItem4)
		
		# TODO:添加按钮
		self.show1 = QtWidgets.QPushButton(self.layoutWidget)
		self.show1.setObjectName("show3D")
		self.show1.setDisabled(True)
		self.verticalLayout_2.addWidget(self.show1)
		
		self.show2 = QtWidgets.QPushButton(self.layoutWidget)
		self.show2.setObjectName("show3D")
		self.show2.setDisabled(True)
		self.verticalLayout_2.addWidget(self.show2)
		
		self.show3 = QtWidgets.QPushButton(self.layoutWidget)
		self.show3.setObjectName("show3D")
		self.show3.setDisabled(True)
		self.verticalLayout_2.addWidget(self.show3)
		
		self.show4 = QtWidgets.QPushButton(self.layoutWidget)
		self.show4.setObjectName("show3D")
		self.show4.setDisabled(True)
		self.verticalLayout_2.addWidget(self.show4)
		
		self.show5 = QtWidgets.QPushButton(self.layoutWidget)
		self.show5.setObjectName("show3D")
		self.show5.setDisabled(True)
		self.verticalLayout_2.addWidget(self.show5)
		
		self.show6 = QtWidgets.QPushButton(self.layoutWidget)
		self.show6.setObjectName("show3D")
		self.show6.setDisabled(True)
		self.verticalLayout_2.addWidget(self.show6)
		
		self.show7 = QtWidgets.QPushButton(self.layoutWidget)
		self.show7.setObjectName("show3D")
		self.show7.setDisabled(True)
		self.verticalLayout_2.addWidget(self.show7)
		
		self.show8 = QtWidgets.QPushButton(self.layoutWidget)
		self.show8.setObjectName("show3D")
		self.show8.setDisabled(True)
		self.verticalLayout_2.addWidget(self.show8)
		
		self.show9 = QtWidgets.QPushButton(self.layoutWidget)
		self.show9.setObjectName("show3D")
		self.show9.setDisabled(True)
		self.verticalLayout_2.addWidget(self.show9)
		
		self.show10 = QtWidgets.QPushButton(self.layoutWidget)
		self.show10.setObjectName("show3D")
		self.show10.setDisabled(True)
		self.verticalLayout_2.addWidget(self.show10)
		
		
		
		
		self.verticalLayout = QtWidgets.QVBoxLayout()
		self.verticalLayout.setObjectName("verticalLayout")
		
		self.checkBox = QtWidgets.QCheckBox(self.layoutWidget)
		self.checkBox.setEnabled(False)
		self.checkBox.setObjectName("checkBox")
		self.verticalLayout.addWidget(self.checkBox)
		self.checkBox_4 = QtWidgets.QCheckBox(self.layoutWidget)
		self.checkBox_4.setEnabled(False)
		self.checkBox_4.setObjectName("checkBox_4")
		self.verticalLayout.addWidget(self.checkBox_4)
		self.checkBox_3 = QtWidgets.QCheckBox(self.layoutWidget)
		self.checkBox_3.setEnabled(False)
		self.checkBox_3.setObjectName("checkBox_3")
		self.verticalLayout.addWidget(self.checkBox_3)
		self.checkBox_2 = QtWidgets.QCheckBox(self.layoutWidget)
		self.checkBox_2.setEnabled(False)
		self.checkBox_2.setObjectName("checkBox_2")
		self.verticalLayout.addWidget(self.checkBox_2)
		self.checkBox_5 = QtWidgets.QCheckBox(self.layoutWidget)
		self.checkBox_5.setEnabled(False)
		self.checkBox_5.setObjectName("checkBox_5")
		self.verticalLayout.addWidget(self.checkBox_5)
		
		self.verticalLayout_2.addLayout(self.verticalLayout)
		
		spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.verticalLayout_2.addItem(spacerItem5)
		
		self.exitWindow = QtWidgets.QPushButton(self.layoutWidget)
		self.exitWindow.setObjectName("exitWindow")
		self.verticalLayout_2.addWidget(self.exitWindow)
		
		self.horizontalLayout_2.addLayout(self.verticalLayout_2)
		
		MainWindow.setCentralWidget(self.centralwidget)
		
		self.retranslateUi(MainWindow)
		
		'''信号与槽函数链接'''
		'''退出'''
		self.exitWindow.clicked.connect(self.close_all)
		
		'''播放'''
		self.playPause.clicked.connect(self.play_video)
		
		'''进度条'''
		self.horizontalSlider.sliderPressed.connect(self.disconnect_horizontalSlider)
		self.horizontalSlider.sliderReleased.connect(self.connect_horizontalSlider)
		self.horizontalSlider.sliderReleased.connect(self.change_play)
		self.playnumberSignal.connect(self.playthread.change_play)
		
		'''播放器'''
		self.playthread.InitSignal.connect(self.information_process)
		self.playthread.PictureSignal.connect(self.show_video)
		self.playthread.ScrollBarSignal.connect(self.scroll_bar)
		
		'''停止'''
		self.stopVideoPlay.clicked.connect(self.stop_video)
		
		'''截图'''
		self.screenShot.clicked.connect(self.playthread.screen_shot)
		self.calculatethread.originalpictureSignal.connect(self.show_original)
		self.screenShot.clicked.connect(self.set_enabled)

		'''温度条'''
		self.minTemperature.valueChanged.connect(self.set_temperature)
		self.maxTemperature.valueChanged.connect(self.set_temperature)
		
		'''播放线程链接计算线程'''
		self.playthread.TocalculateSignal.connect(self.calculatethread.get_picture)
		self.temperatureSignal.connect(self.calculatethread.receive_temperature)
		
		'''灰度'''
		self.showGray.clicked.connect(self.calculatethread.draw_gray)
		self.calculatethread.graypictureSignal.connect(self.show_gray)
		
		'''3D'''
		self.show3D.clicked.connect(self.calculatethread.draw_3D)
		self.calculatethread.D3DpictureSignal.connect(self.show_D3D)
		
		'''云图'''
		self.showContour.clicked.connect(self.calculatethread.draw_contour)
		self.calculatethread.contourpictureSignal.connect(self.show_contour)
		
		#self.exitWindow.clicked.connect(self.newthread.wait)
		#self.exitWindow.clicked.connect(self.newthread.quit)
		
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
		
	def retranslateUi(self, MainWindow):
		
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "红外视频识别软件"))
		self.stopVideoPlay.setText(_translate("MainWindow", "停止"))
		self.playPause.setText(_translate("MainWindow", "播放/暂停"))
		self.screenShot.setText(_translate("MainWindow", "截图"))
		self.minLabel.setText(_translate("MainWindow", "最低温度"))
		self.maxLabel.setText(_translate("MainWindow", "最高温度"))
		self.showGray.setText(_translate("MainWindow", "灰度"))
		self.show3D.setText(_translate("MainWindow", "3D"))
		self.show1.setText(_translate("MainWindow", "1"))
		self.show2.setText(_translate("MainWindow", "2"))
		self.show3.setText(_translate("MainWindow", "3"))
		self.show4.setText(_translate("MainWindow", "4"))
		self.show5.setText(_translate("MainWindow", "5"))
		self.show6.setText(_translate("MainWindow", "6"))
		self.show7.setText(_translate("MainWindow", "7"))
		self.show8.setText(_translate("MainWindow", "8"))
		self.show9.setText(_translate("MainWindow", "9"))
		self.show10.setText(_translate("MainWindow", "10"))
		self.showContour.setText(_translate("MainWindow", "云图"))
		self.checkBox.setText(_translate("MainWindow", "初始化"))
		self.checkBox_4.setText(_translate("MainWindow", "最低温度"))
		self.checkBox_3.setText(_translate("MainWindow", "最高温度"))
		self.checkBox_2.setText(_translate("MainWindow", "截图"))
		self.checkBox_5.setText(_translate("MainWindow", "输出图像"))
		self.exitWindow.setText(_translate("MainWindow", "退出"))
	
	def play_video(self):
		
		if not self.begin:
			
			self.fileselect = QtWidgets.QFileDialog()
			
			self.fileselect.setFileMode(QtWidgets.QFileDialog.ExistingFile)
			self.fileselect.setWindowTitle('请选择720*576的红外视频')
			self.fileselect.setNameFilter('video files(*.mpg)')
			
			while self.fileselect.exec():
				
				self.filename = self.fileselect.selectedFiles()[0]
				self.capcheck = cv2.VideoCapture(self.filename)
				self.wcapcheck = self.capcheck.get(cv2.CAP_PROP_FRAME_WIDTH)
				self.hcapcheck = self.capcheck.get(cv2.CAP_PROP_FRAME_HEIGHT)
				print(self.wcapcheck, self.hcapcheck)
				print(self.capcheck.get(cv2.CAP_PROP_FRAME_COUNT))
				if (self.hcapcheck == 576 and self.wcapcheck == 720):
					break
			
			else:
				return
			
			self.capcheck.release()
			
			self.playthread.receive_address(self.filename)
			self.begin = True
		
		if not self.playthread.MyTimer.isActive():
			
			self.playthread.MyTimer.start(30)
			self.play = True
			self.screenShot.setDisabled(False)
			self.stopVideoPlay.setDisabled(False)
			
		else:
			
			self.playthread.MyTimer.stop()
			self.play = False
			
	def stop_video(self):
		
		self.playthread.stop_video()
	
	def show_video(self, Qqimage):
		
		self.videoPlayer.setPixmap(QtGui.QPixmap.fromImage(Qqimage))
	
	def information_process(self, VideoFrameNumber):
		self.horizontalSlider.setMaximum(VideoFrameNumber)
		self.horizontalSlider.setMinimum(0)
		
	def change_play(self):
		
		self.playnumberSignal.emit(self.horizontalSlider.value())
		
	def scroll_bar(self, scrollnumber):
		
		self.horizontalSlider.setValue(int(scrollnumber))
		
	def disconnect_horizontalSlider(self):
		
		self.playthread.ScrollBarSignal.disconnect()
	
	def connect_horizontalSlider(self):
		
		self.playthread.ScrollBarSignal.connect(self.scroll_bar)
		
	def set_temperature(self):
		
		high = self.maxTemperature.value()
		low = self.minTemperature.value()
		high = float('%.2f' % high)
		low = float('%.2f' % low)
		self.temperatureSignal.emit(high, low)
		
	def set_enabled(self):
		
		self.show3D.setDisabled(False)
		self.showContour.setDisabled(False)
		self.showGray.setDisabled(False)
	
	def show_gray(self, gray):
		
		self.Mygray = MyWidget()
		self.Mygray.mpl.start_static_plot(gray, flag='gray')
		self.Mygray.exec()
	
	def show_D3D(self, D3D):
		
		self.MyD3D = MyD3DWidget()
		self.MyD3D.mpl.start_static_plot(D3D, flag='D3D')
		self.MyD3D.exec()
	
	def show_contour(self, contour):
		
		self.Mycontour = MyContourWidget()
		self.Mycontour.mpl.start_static_plot(contour, flag='contour')
		self.Mycontour.exec()
	
	def show_original(self, original):
		
		self.Myoriginal = MyWidget()
		self.Myoriginal.mpl.start_static_plot(original, flag='original')
		self.Myoriginal.exec()
	
	def close_all(self):
		
		print(self.newthread1.currentThreadId(), self.newthread2.currentThreadId())
		print(self.thread())
		print(self.newthread1.isFinished())
		self.calculatethread.deleteLater()
		self.playthread.deleteLater()
		print(self.newthread1.isFinished())
		
		self.newthread1.quit()
		self.newthread2.quit()
		print(self.newthread1.isFinished())
		print(self.newthread2.isFinished())
		
		self.newthread1.wait()
		self.newthread2.wait()
		print(self.newthread1.isFinished())
		print(self.newthread2.isFinished())
		self.close()
		
		
class PlayerThread(QtCore.QObject):
	
	InitSignal = QtCore.pyqtSignal(object)
	PictureSignal = QtCore.pyqtSignal(object)
	ScrollBarSignal = QtCore.pyqtSignal(object)
	TocalculateSignal = QtCore.pyqtSignal(object)
	
	def __init__(self, parant = None):
		
		super().__init__(parant)
		
		self.address = None
		self.ret = False
		self.image = np.ones((576, 720, 3), np.uint8) * 255
		self.ischanged = False
		self.playnumber = 1
		self.stopchanged = False
		self.begin = False
		self.MyTimer = QtCore.QTimer()
		self.MyTimer.timeout.connect(self.video_play)
		self.printscreen = None
	
	def receive_address(self, address):
	
		self.address = address
		self.cap = cv2.VideoCapture(self.address)
		self.VideoFrameNumber = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
	
	def video_play(self):
		
		if not self.begin:
			
			self.InitSignal.emit(self.VideoFrameNumber)
			self.begin = True
		
		if self.ischanged:
			self.cap.set(cv2.CAP_PROP_POS_FRAMES, int(self.playnumber))
			self.ischanged = False
			
		if self.stopchanged or self.cap.get(cv2.CAP_PROP_POS_FRAMES) == self.cap.get(cv2.CAP_PROP_FRAME_COUNT):
			self.cap.release()
			self.cap = cv2.VideoCapture(self.address)
			self.stopchanged = False
			
		self.ret, self.image = self.cap.read()
		self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
		self.Qqimage = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0],
							   QtGui.QImage.Format_RGB888)
		self.PictureSignal.emit(self.Qqimage)
		self.ScrollBarSignal.emit(self.cap.get(cv2.CAP_PROP_POS_FRAMES))

	def continue_pause(self):
		
		if not self.__pause:
			self.__pause = True
		
		else:
			self.__pause = False
			
	def stop_video(self):
		
		self.MyTimer.stop()
		self.stopchanged = True
		
		self.image = np.ones((576, 720, 3), np.uint8) * 255
		self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
		self.Stopimage = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0],
								 QtGui.QImage.Format_RGB888)
		self.PictureSignal.emit(self.Stopimage)
		self.ScrollBarSignal.emit(0)
		
	def change_play(self, playnumber):
		
		self.ischanged = True
		self.playnumber = playnumber
		
	def screen_shot(self):
		
		self.printscreen = self.image
		self.TocalculateSignal.emit(self.printscreen)
		

class CalculateThread(QtCore.QObject):
	
	graypictureSignal = QtCore.pyqtSignal(object)
	D3DpictureSignal = QtCore.pyqtSignal(object)
	contourpictureSignal = QtCore.pyqtSignal(object)
	originalpictureSignal = QtCore.pyqtSignal(object)
	
	
	def __init__(self, parent = None):
		super().__init__(parent)
		self.image = np.ones((576, 720, 3), np.uint8) *255
		self.gray = np.ones((576, 720, 3), np.uint8) *255
		self.mask = cv2.imread('mask.png', cv2.IMREAD_GRAYSCALE)
		
		self.high = 30.0
		self.low = 10.0
		
		self.barheight = 1
		self.barwidth = 1
		
		self.pictureheight = 1
		self.picturewidth = 1
		self.pictureheight3D = 1
		self.picturewidth3D = 1
		
		self.color = None
		self.temperature = []
		self.temperaturedict = {}
		self.k = 1
		
		self.renovation3D = False
		self.renovationcontour = False
		
		self.D3D = None
		self.contour = None
		
	
	def get_picture(self, picture):
		self.image = picture.copy()
		
		self.rot = self.image[184:432, 652:668].copy()
		self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
		self.gray = cv2.inpaint(self.gray, self.mask, 3, cv2.INPAINT_TELEA)
		self.rot = cv2.cvtColor(self.rot, cv2.COLOR_BGR2GRAY)
		self.barheight, self.barwidth = self.rot.shape[:2]
		self.color = self.rot.sum(axis = 1)
		self.color = self.color / self.barwidth
		self.color = [max(self.color), min(self.color)]
		self.temperature = [self.high, self.low]
		self.temperaturedict = dict(zip(self.temperature, self.color))
		print(self.temperaturedict)
		
		self.gray = cv2.GaussianBlur(self.gray, (0, 0), 5)
		if self.temperaturedict[self.high] - self.temperaturedict[self.low]:
			self.k = (self.high - self.low) / (self.temperaturedict[self.high] - self.temperaturedict[self.low])
		
		self.renovation3D = True
		self.renovationcontour = True
		
		self.originalpictureSignal.emit(self.image)
		
		# plt.close()
		# plt.imshow(self.image)
		# plt.show()
		# plt.close()
		# plt.clf()
	
	def receive_temperature(self, high, low):
		self.high = high
		self.low = low
		print(self.high, self.low)
		
	def draw_gray(self):
		
		self.graypictureSignal.emit(self.gray)
		
	def draw_3D(self):
		if self.renovation3D:
			self.D3D = self.gray.copy()
			for i in range(3):
				self.D3D = cv2.pyrDown(self.D3D)
			self.D3D = self.D3D[6:66, 5:83]
			
			self.D3D1 = np.zeros(self.D3D.shape, np.float_)
			self.pictureheight3D, self.picturewidth3D = self.D3D.shape[:2]
			for col3d in range(self.pictureheight3D):
				for row3d in range(self.picturewidth3D):
					self.temp3D = self.D3D[col3d][row3d]
					self.D3D1[col3d][row3d] = self.low + (self.temp3D - self.temperaturedict[self.low]) * self.k
			self.renovation3D = False
		self.D3DpictureSignal.emit(self.D3D1)
		
		# self.x3D = np.arange(0, self.picturewidth3D, 1)
		# self.y3D = np.arange(0, self.pictureheight3D, 1)
		# self.x3D, self.y3D = np.meshgrid(self.x3D, self.y3D)
		# self.D3D1 = cv2.flip(self.D3D1, 0)
		# self.fig3d = plt.figure()
		# self.ax = Axes3D(self.fig3d)
		# self.ax.plot_surface(self.x3D, self.y3D, self.D3D1[self.y3D, self.x3D], rstride=2, cstride=2, cmap='rainbow')
		# plt.show()
		# plt.close()
		# plt.clf()
	
	def draw_contour(self):
		plt.close()
		if self.renovationcontour:
			
			self.contour = self.gray.copy()
			self.contour = self.contour[40:530,30:670]
			
			self.pictureheight, self.picturewidth = self.contour.shape[:2]
			self.contour1 = np.zeros(self.contour.shape, np.float_)
			for col in range(self.pictureheight):
				for row in range(self.picturewidth):
					self.temp = self.contour[col][row]
					self.contour1[col][row] = self.low + (self.temp - self.temperaturedict[self.low]) * self.k
					self.renovationcontour = False
		self.contourpictureSignal.emit(self.contour1)
		
		# self.xcontour = np.arange(0, self.picturewidth, 1)
		# self.ycontour = np.arange(0, self.pictureheight, 1)
		# self.xcontour, self.ycontour = np.meshgrid(self.xcontour, self.ycontour)
		# print(self.contour1.max())
		# self.contour1 = cv2.flip(self.contour1, 0)
		# print(self.contour1.max())
		#
		# self.contourline = plt.contour(self.xcontour, self.ycontour, self.contour1[self.ycontour, self.xcontour], 10,
		#                         colors = 'black', linewidths = 1)
		# plt.clabel(self.contourline, inline = True, inline_spacing = 5, fontsize = 10, fmt = '%.1f')
		# plt.contourf(self.xcontour, self.ycontour, self.contour1[self.ycontour, self.xcontour], 10, cmap='rainbow')
		# plt.show()
		# plt.close()
		# plt.clf()

