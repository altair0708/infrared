import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backend_bases import FigureManagerBase as FigureManger
from matplotlib.backend_bases import RendererBase as Renderer
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.image as mpimg
from PyQt5 import QtCore, QtWidgets
import numpy as np
import sys
import cv2


class MyContourCanvas(FigureCanvas):
	def __init__(self, parent=None, width=5, height=4, dpi=100):
		
		plt.rcParams['font.family'] = ['SimHei']
		plt.rcParams['axes.unicode_minus'] = False
		
		self.fig = plt.figure(figsize=(width, height), dpi=dpi)
		
		#self.axes = self.fig.add_subplot(111)
		
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
			print(self.pictureheight3D, self.picturewidth3D)
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
			self.contourline = self.axes.contour(self.xcontour, self.ycontour, self.contour[self.ycontour, self.xcontour],
			                                     self.slider_number, colors='black', linewidths=1)
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
		self.axes.contourf(self.xcontour, self.ycontour, self.contour[self.ycontour, self.xcontour],
		                   self.slider_number, cmap='rainbow')
		self.fig.draw(renderer=self.renderer)
		self.blit(self.fig.bbox)
		
	def show_all(self):
		
		self.fig.clear()
		self.axes = self.fig.add_subplot(1, 1, 1)
		self.contourline = self.axes.contour(self.xcontour, self.ycontour, self.contour[self.ycontour, self.xcontour],
		                                     self.slider_number, colors='black', linewidths=1)
		self.axes.clabel(self.contourline, inline=True, inline_spacing=5, fontsize=10, fmt='%.1f')
		self.axes.contourf(self.xcontour, self.ycontour, self.contour[self.ycontour, self.xcontour],
		                   self.slider_number, cmap='rainbow')
		self.fig.draw(renderer=self.renderer)
		self.blit(self.fig.bbox)
		
class MyContourWidget(QtWidgets.QDialog):
	
	def __init__(self, parent=None, picture=None):
		super().__init__(parent)
		self.picture = picture
		self.initUi()
		self.connectEmit()
		self.retranslateUi()
		
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
		
if __name__ == '__main__':
	
	app = QtWidgets.QApplication(sys.argv)
	image = mpimg.imread('mask.png')
	ui = MyContourWidget(picture=image)
	ui.show()
	sys.exit(app.exec())
