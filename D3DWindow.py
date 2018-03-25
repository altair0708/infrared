import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.image as mpimg
from PyQt5 import QtCore, QtWidgets
import numpy as np
import sys
import cv2


class MyD3DCanvas(FigureCanvas):
	def __init__(self, parent=None, width=5, height=4, dpi=100):
		
		plt.rcParams['font.family'] = ['SimHei']
		plt.rcParams['axes.unicode_minus'] = False
		
		self.fig = Figure(figsize=(width, height), dpi=dpi)
		
		#self.axes = self.fig.add_subplot(111)
		
		FigureCanvas.__init__(self, self.fig)
		self.setParent(parent)
		
		FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)
		
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
			print(self.pictureheight3D, self.picturewidth3D)
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
			self.contourline = self.axes.contour(self.xcontour, self.ycontour, self.contour[self.ycontour, self.xcontour],
			                               10, colors='black', linewidths=1)
			self.axes.clabel(self.contourline, inline=True, inline_spacing=5, fontsize=10, fmt='%.1f')
			self.axes.contourf(self.xcontour, self.ycontour, self.contour[self.ycontour, self.xcontour], 10, cmap='rainbow')
		
		elif flag == 'original':
			print(1)
			self.fig.suptitle('原始图像')
			self.fig.figimage(picture, resize=True)
		
class MyD3DWidget(QtWidgets.QDialog):
	
	def __init__(self, parent=None, picture=None):
		super().__init__(parent)
		self.picture = picture
		self.initUi()
		self.connectEmit()
		self.retranslateUi()
		
	def initUi(self):

		self.layout = QtWidgets.QVBoxLayout(self)
		self.mpl = MyD3DCanvas(self)
		self.layout.addWidget(self.mpl)
		
		self.horizontalLayout = QtWidgets.QHBoxLayout(self)
		self.save_button = QtWidgets.QPushButton(self)
		self.save_button.setObjectName("save")
		self.horizontalLayout.addWidget(self.save_button)
		self.enlarge_button = QtWidgets.QPushButton(self)
		self.enlarge_button.setObjectName("enlarge")
		self.horizontalLayout.addWidget(self.enlarge_button)
		self.return_button = QtWidgets.QPushButton(self)
		self.return_button.setObjectName("pull")
		self.horizontalLayout.addWidget(self.return_button)
		self.layout.addLayout(self.horizontalLayout)
	
	def connectEmit(self):
		self.save_button.clicked.connect(self.save_figure)
		
	def retranslateUi(self):
		
		__translation = QtCore.QCoreApplication.translate
		self.setWindowTitle(__translation(' ', '图像'))
		self.save_button.setText(__translation(' ', '保存'))
		self.enlarge_button.setText(__translation(' ', '放大'))
		self.return_button.setText(__translation(' ', '还原'))
	
	def save_figure( self ):
		
		self.save_widget = QtWidgets.QFileDialog()
		self.save_widget.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
		self.save_widget.setWindowTitle('请选择保存路径')
		self.save_widget.setNameFilter('image files(*.png)')
		
		if self.save_widget.exec():
			self.save_name = self.save_widget.selectedFiles()[0]
			self.save_url = self.save_widget.selectedUrls()
			print(self.save_url, self.save_name)
			self.mpl.fig.savefig(self.save_name)
		else:
			return
		
if __name__ == '__main__':
	
	app = QApplication(sys.argv)
	image = mpimg.imread('mask.png')
	ui = MyD3DWidget(picture=image)
	ui.show()
	sys.exit(app.exec())