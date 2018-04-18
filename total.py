# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import matplotlib
matplotlib.use("Qt5Agg")
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import numpy as np
import sys
import cv2

class MyCanvas(FigureCanvas):
	
	def __init__(self, parent=None, width=5, height=4, dpi=100):
		
		plt.rcParams['font.family'] = ['SimHei']
		plt.rcParams['axes.unicode_minus'] = False
		
		self.fig = Figure(figsize=(width, height), dpi=dpi)
		
		super().__init__(self.fig)
		self.setParent(parent)
		
		self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.updateGeometry()
	
	def start_static_plot(self, picture, flag='gray'):
		
		if flag == 'gray':
			
			self.fig.suptitle('灰度图像')
			self.fig.figimage(picture, resize=True, cmap='gray')
		
		elif flag == 'D3D':
			
			self.fig.suptitle('3D图像')
			self.axes = self.fig.add_subplot(1, 1, 1, projection='3d')
			self.D3D = picture.copy()
			self.pictureheight3D, self.picturewidth3D = self.D3D.shape[:2]
			self.x3D = np.arange(0, self.picturewidth3D, 1)
			self.y3D = np.arange(0, self.pictureheight3D, 1)
			self.x3D, self.y3D = np.meshgrid(self.x3D, self.y3D)
			self.D3D = cv2.flip(self.D3D, 0)
			self.axes.plot_surface(self.x3D, self.y3D, self.D3D[self.y3D, self.x3D], rstride=2, cstride=2,
			                       cmap='rainbow')
		
		elif flag == 'contour':
			
			self.fig.suptitle('等温线图像')
			self.axes = self.fig.add_subplot(1, 1, 1)
			self.contour = picture.copy()
			self.pictureheight, self.picturewidth = self.contour.shape[:2]
			self.xcontour = np.arange(0, self.picturewidth, 1)
			self.ycontour = np.arange(0, self.pictureheight, 1)
			self.xcontour, self.ycontour = np.meshgrid(self.xcontour, self.ycontour)
			self.contour = cv2.flip(self.contour, 0)
			self.contourline = self.axes.contour(self.xcontour, self.ycontour,
			                                     self.contour[self.ycontour, self.xcontour], 10, colors='black',
			                                     linewidths=1)
			self.axes.clabel(self.contourline, inline=True, inline_spacing=5, fontsize=10, fmt='%.1f')
			self.axes.contourf(self.xcontour, self.ycontour, self.contour[self.ycontour, self.xcontour], 10,
			                   cmap='rainbow')
		
		elif flag == 'original':
			
			self.fig.suptitle('原始图像')
			self.fig.figimage(picture, resize=True)


class MyWidget(QtWidgets.QDialog):
	
	def __init__(self, parent=None, picture=None):
		
		super().__init__(parent)
		self.picture = picture
		self.initUi()
		self.retranslateUi()
		self.setWindowIcon(QtGui.QIcon('红外视频动态识别.ico'))
	
	def initUi(self):
		
		self.layout = QtWidgets.QVBoxLayout(self)
		self.mpl = MyCanvas(self)
		self.layout.addWidget(self.mpl)
		
		self.toolbar = NavigationToolbar(self.mpl, self)
		self.layout.addWidget(self.toolbar)
	
	def retranslateUi(self):
		__translation = QtCore.QCoreApplication.translate
		self.setWindowTitle(__translation(' ', '图像'))
		

class MyD3DCanvas(FigureCanvas):
	
	def __init__(self, parent=None, width=5, height=4, dpi=100):
		
		plt.rcParams['font.family'] = ['SimHei']
		plt.rcParams['axes.unicode_minus'] = False
		
		self.fig = Figure(figsize=(width, height), dpi=dpi)
		
		super().__init__(self.fig)
		self.setParent(parent)
		
		self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.updateGeometry()
	
	def start_static_plot(self, picture, flag='gray'):
		
		if flag == 'gray':
			
			self.fig.suptitle('灰度图像')
			self.fig.figimage(picture, resize=True)
		
		elif flag == 'D3D':
			
			self.fig.suptitle('3D图像')
			self.axes = self.fig.add_subplot(1, 1, 1, projection='3d')
			self.D3D = picture.copy()
			self.axes.set_xticks(np.arange(0, 80, 13))
			self.axes.set_xticklabels(np.arange(0, 601, 100))
			self.axes.set_yticks(np.arange(0, 61, 12))
			self.axes.set_yticklabels(np.arange(0, 501, 100))
			self.pictureheight3D, self.picturewidth3D = self.D3D.shape[:2]
			self.x3D = np.arange(0, self.picturewidth3D, 1)
			self.y3D = np.arange(0, self.pictureheight3D, 1)
			self.x3D, self.y3D = np.meshgrid(self.x3D, self.y3D)
			self.D3D = cv2.flip(self.D3D, 0)
			self.axes.plot_surface(self.x3D, self.y3D, self.D3D[self.y3D, self.x3D], rstride=2, cstride=2,
			                       cmap='rainbow')
		
		elif flag == 'contour':
			
			self.fig.suptitle('等温线图像')
			self.axes = self.fig.add_subplot(1, 1, 1)
			self.contour = picture.copy()
			self.pictureheight, self.picturewidth = self.contour.shape[:2]
			self.xcontour = np.arange(0, self.picturewidth, 1)
			self.ycontour = np.arange(0, self.pictureheight, 1)
			self.xcontour, self.ycontour = np.meshgrid(self.xcontour, self.ycontour)
			self.contour = cv2.flip(self.contour, 0)
			self.contourline = self.axes.contour(self.xcontour, self.ycontour,
			                                     self.contour[self.ycontour, self.xcontour], 10, colors='black',
			                                     linewidths=1)
			self.axes.clabel(self.contourline, inline=True, inline_spacing=5, fontsize=10, fmt='%.1f')
			self.axes.contourf(self.xcontour, self.ycontour, self.contour[self.ycontour, self.xcontour], 10,
			                   cmap='rainbow')
		
		
		elif flag == 'original':
			
			self.fig.suptitle('原始图像')
			self.fig.figimage(picture, resize=True)


class MyD3DWidget(QtWidgets.QDialog):
	
	def __init__(self, parent=None, picture=None):
		
		super().__init__(parent)
		self.picture = picture
		self.initUi()
		self.retranslateUi()
		self.setWindowIcon(QtGui.QIcon('红外视频动态识别.ico'))
	
	def initUi(self):
		
		self.layout = QtWidgets.QVBoxLayout(self)
		self.mpl = MyD3DCanvas(self)
		self.mpl.resize(QtCore.QSize(720, 576))
		self.mpl.setMinimumSize(QtCore.QSize(720, 576))
		self.mpl.setMaximumSize(QtCore.QSize(720, 576))
		
		self.layout.addWidget(self.mpl)
		self.toolbar = NavigationToolbar(self.mpl, self)
		self.layout.addWidget(self.toolbar)
	
	def retranslateUi(self):
		
		__translation = QtCore.QCoreApplication.translate
		self.setWindowTitle(__translation(' ', '3D图像'))


class MyContourCanvas(FigureCanvas):
	
	def __init__(self, parent=None, width=5, height=4, dpi=100):
		
		plt.rcParams['font.family'] = ['SimHei']
		plt.rcParams['axes.unicode_minus'] = False
		
		self.fig = plt.figure(figsize=(width, height), dpi=dpi)
		
		super().__init__(self.fig)
		self.setParent(parent)
		
		self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.updateGeometry()
		self.slider_number = 10
	
	def start_static_plot(self, picture, flag='gray'):
		
		if flag == 'gray':
			
			self.fig.suptitle('灰度图像')
			self.fig.figimage(picture, resize=True)
		
		elif flag == 'D3D':
			
			self.fig.suptitle('3D图像')
			self.axes = self.fig.add_subplot(1, 1, 1, projection='3d')
			self.D3D = picture.copy()
			self.pictureheight3D, self.picturewidth3D = self.D3D.shape[:2]
			self.x3D = np.arange(0, self.picturewidth3D, 1)
			self.y3D = np.arange(0, self.pictureheight3D, 1)
			self.x3D, self.y3D = np.meshgrid(self.x3D, self.y3D)
			self.D3D = cv2.flip(self.D3D, 0)
			self.axes.plot_surface(self.x3D, self.y3D, self.D3D[self.y3D, self.x3D], rstride=2, cstride=2,
			                       cmap='rainbow')
		
		elif flag == 'contour':
			
			self.fig.suptitle('等温线图像')
			self.axes = self.fig.add_subplot(1, 1, 1)
			self.axes.axis('equal')
			self.contour = picture.copy()
			self.pictureheight, self.picturewidth = self.contour.shape[:2]
			self.xcontour = np.arange(0, self.picturewidth, 1)
			self.ycontour = np.arange(0, self.pictureheight, 1)
			self.xcontour, self.ycontour = np.meshgrid(self.xcontour, self.ycontour)
			self.contour = cv2.flip(self.contour, 0)
			self.contourline = self.axes.contour(self.xcontour, self.ycontour,
			                                     self.contour[self.ycontour, self.xcontour], self.slider_number,
			                                     colors='black', linewidths=1)
			self.axes.clabel(self.contourline, inline=True, inline_spacing=5, fontsize=10, fmt='%.1f')
			self.axes.contourf(self.xcontour, self.ycontour, self.contour[self.ycontour, self.xcontour],
			                   self.slider_number, cmap='rainbow')
		
		elif flag == 'original':
			
			self.fig.suptitle('原始图像')
			self.fig.figimage(picture, resize=True)
	
	def show_contour(self):
		
		self.fig.clear()
		self.axes = self.fig.add_subplot(1, 1, 1)
		self.contourline = self.axes.contour(self.xcontour, self.ycontour, self.contour[self.ycontour, self.xcontour],
		                                     self.slider_number, cmap='rainbow', linewidths=2)
		self.axes.clabel(self.contourline, inline=True, inline_spacing=5, fontsize=10, fmt='%.1f')
		self.fig.draw(renderer=self.renderer)
		self.blit(self.fig.bbox)
	
	def show_contourf(self):
		
		self.fig.clear()
		self.axes = self.fig.add_subplot(1, 1, 1)
		self.axes.contourf(self.xcontour, self.ycontour, self.contour[self.ycontour, self.xcontour], self.slider_number,
		                   cmap='rainbow')
		self.fig.draw(renderer=self.renderer)
		self.blit(self.fig.bbox)
	
	def show_all(self):
		
		self.fig.clear()
		self.axes = self.fig.add_subplot(1, 1, 1)
		self.contourline = self.axes.contour(self.xcontour, self.ycontour, self.contour[self.ycontour, self.xcontour],
		                                     self.slider_number, colors='black', linewidths=1)
		self.axes.clabel(self.contourline, inline=True, inline_spacing=5, fontsize=10, fmt='%.1f')
		self.axes.contourf(self.xcontour, self.ycontour, self.contour[self.ycontour, self.xcontour], self.slider_number,
		                   cmap='rainbow')
		self.fig.draw(renderer=self.renderer)
		self.blit(self.fig.bbox)


class MyContourWidget(QtWidgets.QDialog):
	
	def __init__(self, parent=None, picture=None):
		
		super().__init__(parent)
		self.picture = picture
		self.initUi()
		self.connectEmit()
		self.retranslateUi()
		self.setWindowIcon(QtGui.QIcon('红外视频动态识别.ico'))
	
	def initUi(self):
		
		self.layout = QtWidgets.QVBoxLayout(self)
		self.mpl = MyContourCanvas(self)
		self.layout.addWidget(self.mpl)
		self.toolbar = NavigationToolbar(self.mpl, self)
		self.mpl.resize(QtCore.QSize(720, 576))
		self.mpl.setMinimumSize(QtCore.QSize(720, 576))
		self.mpl.setMaximumSize(QtCore.QSize(720, 576))
		self.layout.addWidget(self.toolbar)
		
		self.contour_number = QtWidgets.QSlider(self)
		self.contour_number.setOrientation(QtCore.Qt.Horizontal)
		self.contour_number.setObjectName('contour_number')
		self.contour_number.setRange(6, 14)
		self.contour_number.setValue(10)
		self.contour_number.setTickInterval(2)
		self.contour_number.setSingleStep(2)
		self.contour_number.setTickPosition(QtWidgets.QSlider.TicksBelow)
		self.layout.addWidget(self.contour_number)
		
		self.horizontalLayout = QtWidgets.QHBoxLayout(self)
		
		self.show_contour = QtWidgets.QPushButton(self)
		self.show_contour.setObjectName("contour")
		self.horizontalLayout.addWidget(self.show_contour)
		
		self.show_contourf = QtWidgets.QPushButton(self)
		self.show_contourf.setObjectName("enlarge")
		self.horizontalLayout.addWidget(self.show_contourf)
		
		self.show_all = QtWidgets.QPushButton(self)
		self.show_all.setObjectName("pull")
		self.horizontalLayout.addWidget(self.show_all)
		self.layout.addLayout(self.horizontalLayout)
	
	def connectEmit(self):
		
		self.show_contour.clicked.connect(self.mpl.show_contour)
		self.show_contourf.clicked.connect(self.mpl.show_contourf)
		self.show_all.clicked.connect(self.mpl.show_all)
		self.contour_number.sliderReleased.connect(self.change_contour_number)
	
	def retranslateUi(self):
		
		__translation = QtCore.QCoreApplication.translate
		self.setWindowTitle(__translation(' ', '等温线图像'))
		self.show_contour.setText(__translation(' ', '等温线'))
		self.show_contourf.setText(__translation(' ', '等温云图'))
		self.show_all.setText(__translation(' ', '全部'))
	
	def change_contour_number(self):
		
		self.mpl.fig.clear()
		self.mpl.slider_number = self.contour_number.value()
		self.mpl.show_all()


class Ui_MainWindow(QMainWindow):
	playnumberSignal = QtCore.pyqtSignal(object)
	temperatureSignal = QtCore.pyqtSignal(float, float)
	
	def __init__(self):
		
		super().__init__()
		self.setWindowIcon(QtGui.QIcon('红外视频动态识别.ico'))
		
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
		
		self.playthread = PlayerThread()
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
		self.Blankimage = np.ones((576, 720, 3), np.uint8) * 255
		self.Blankimage = QtGui.QImage(self.Blankimage.data, self.Blankimage.shape[1], self.Blankimage.shape[0],
		                               QtGui.QImage.Format_RGB888)
		self.videoPlayer.setPixmap(QtGui.QPixmap.fromImage(self.Blankimage))
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
		self.exitWindow.clicked.connect(self.close)
		
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
		
		
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
	
	def retranslateUi(self, MainWindow):
		
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "红外视频温度动态监测成像与分析软件"))
		self.stopVideoPlay.setText(_translate("MainWindow", "停止"))
		self.playPause.setText(_translate("MainWindow", "播放/暂停"))
		self.screenShot.setText(_translate("MainWindow", "截图"))
		self.minLabel.setText(_translate("MainWindow", "最低温度"))
		self.maxLabel.setText(_translate("MainWindow", "最高温度"))
		self.showGray.setText(_translate("MainWindow", "灰度"))
		self.show3D.setText(_translate("MainWindow", "3D"))
		self.showContour.setText(_translate("MainWindow", "云图"))
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
		self.begin = False
	
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
		
		self.playthread.MyTimer.stop()
		self.play = False
		self.Mygray = MyWidget()
		self.Mygray.mpl.start_static_plot(gray, flag='gray')
		self.Mygray.exec()
	
	def show_D3D(self, D3D):
		
		self.playthread.MyTimer.stop()
		self.play = False
		self.MyD3D = MyD3DWidget()
		self.MyD3D.mpl.start_static_plot(D3D, flag='D3D')
		self.MyD3D.exec()
	
	def show_contour(self, contour):
		
		self.playthread.MyTimer.stop()
		self.play = False
		self.Mycontour = MyContourWidget()
		self.Mycontour.mpl.start_static_plot(contour, flag='contour')
		self.Mycontour.exec()
	
	def show_original(self, original):
		
		self.playthread.MyTimer.stop()
		self.play = False
		self.Myoriginal = MyWidget()
		self.Myoriginal.mpl.start_static_plot(original, flag='original')
		self.Myoriginal.exec()
	
	def closeEvent(self, event):
		
		reply = QMessageBox.question(self, '提示', '您确定要退出么？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		
		if reply == QMessageBox.Yes:
			self.calculatethread.deleteLater()
			self.playthread.deleteLater()
			
			self.newthread1.quit()
			self.newthread2.quit()
			
			self.newthread1.wait()
			self.newthread2.wait()
			event.accept()
			
		else:
			event.ignore()


class PlayerThread(QtCore.QObject):
	InitSignal = QtCore.pyqtSignal(object)
	PictureSignal = QtCore.pyqtSignal(object)
	ScrollBarSignal = QtCore.pyqtSignal(object)
	TocalculateSignal = QtCore.pyqtSignal(object)
	
	def __init__(self, parant=None):
		
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
	
	def __init__(self, parent=None):
		
		super().__init__(parent)
		self.image = np.ones((576, 720, 3), np.uint8) * 255
		self.gray = np.ones((576, 720, 3), np.uint8) * 255
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
		self.color = self.rot.sum(axis=1)
		self.color = self.color / self.barwidth
		self.color = [max(self.color), min(self.color)]
		self.temperature = [self.high, self.low]
		self.temperaturedict = dict(zip(self.temperature, self.color))
		
		self.gray = cv2.GaussianBlur(self.gray, (0, 0), 15)
		if self.temperaturedict[self.high] - self.temperaturedict[self.low]:
			self.k = (self.high - self.low) / (self.temperaturedict[self.high] - self.temperaturedict[self.low])
		
		self.renovation3D = True
		self.renovationcontour = True
		
		self.originalpictureSignal.emit(self.image)
	
	def receive_temperature(self, high, low):
		
		self.high = high
		self.low = low
	
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
	
	def draw_contour(self):
		
		if self.renovationcontour:
			
			self.contour = self.gray.copy()
			self.contour = self.contour[40:530, 30:670]
			
			self.pictureheight, self.picturewidth = self.contour.shape[:2]
			self.contour1 = np.zeros(self.contour.shape, np.float_)
			for col in range(self.pictureheight):
				for row in range(self.picturewidth):
					self.temp = self.contour[col][row]
					self.contour1[col][row] = self.low + (self.temp - self.temperaturedict[self.low]) * self.k
					self.renovationcontour = False
		self.contourpictureSignal.emit(self.contour1)


if __name__ == '__main__':
	
	class MyMainWindow(Ui_MainWindow):
		def __init__(self, parent=None):
			super().__init__()
			self.setupUi(self)
	
	
	app = QApplication(sys.argv)
	
	mainWindow = MyMainWindow()
	
	mainWindow.show()
	
	sys.exit(app.exec())