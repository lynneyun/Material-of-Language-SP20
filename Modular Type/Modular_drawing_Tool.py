import sys
from PyQt5.QtCore import Qt, QPoint, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QLabel
from PyQt5.QtGui import QPixmap, QImage,QPainter, QPen, QPainterPath,QColor

import bezmerizing
from bezmerizing import Polyline, Bezier
import numpy as np

class Window(QMainWindow):

	def __init__(self):
		super().__init__()
		self.title ="Drawing a Writing System"
		self.drawing = False
		self.setGeometry(100, 100, 1080, 720)
		self.sketch = QImage(self.size(), QImage.Format_ARGB32)
		self.sketch.fill(Qt.black)
		self.design = QImage(self.size(), QImage.Format_ARGB32)
		self.design.fill(QColor(0,0,0,0))
		self.thickStemValue = str("20, 1, 20, 1, 20")
		self.roundStemValue = str("10, 3, 30, 2, 10")
		self.thinStemValue = str("10, 3, 2, 1")
		self.diagnalStemValue = str("2, 2, 10, 2, 2")
		self.buttons()
		self.brushThickStem()
		self.brushState = self.brushThickStem
		self.thickStemLines = []
		self.roundStemLines = []
		self.thinStemLines = []
		self.diagnalStemLines = []



	def buttons(self):
		btn_quit = QPushButton('quit', self)
		btn_quit.clicked.connect(self.close_application)
		btn_quit.setFixedWidth(120)
		btn_quit.move(0,680)

		btn_clear_lines = QPushButton('clear lines', self)
		btn_clear_lines.clicked.connect(self.clear_lines)
		btn_clear_lines.setFixedWidth(120)
		btn_clear_lines.move(0,650)

		btn_clear_sketch = QPushButton('clear sketch', self)
		btn_clear_sketch.clicked.connect(self.clear_sketch)
		btn_clear_sketch.setFixedWidth(120)
		btn_clear_sketch.move(0,620)

		btn_clear_design = QPushButton('clear design', self)
		btn_clear_design.clicked.connect(self.clear_design)
		btn_clear_design.setFixedWidth(120)
		btn_clear_design.move(0,590)

		btn_update_design = QPushButton('update design', self)
		btn_update_design.clicked.connect(self.update_design)
		btn_update_design.setFixedWidth(120)
		btn_update_design.move(0,560)

		# straight stem label
		# btn_thickStem_mod = QPushButton('modify', self)
		# btn_thickStem_mod.clicked.connect(self.brushThickStem)


		label = QLabel(self)
		label.setStyleSheet('color: white')
		label.setText("** Modules **")
		label.move(10,0)
		# straight stem
		btn_thickStem = QPushButton('Straight', self)
		btn_thickStem.clicked.connect(self.brushThickStem)
		btn_thickStem.setStyleSheet('QPushButton {color: black;background-color:cyan;border-radius:5px}'
			'QPushButton:pressed {color: cyan;background-color:black;border-radius:5px}')
		btn_thickStem.setFixedWidth(100)
		btn_thickStem.move(10, 30)

		self.thickStemLabelLineEdit = QLineEdit(self)
		self.thickStemLabelLineEdit.setStyleSheet('background-color:black; color:white; border: 0px')
		self.thickStemLabelLineEdit.setText(str(self.thickStemValue))
		self.thickStemLabelLineEdit.setFixedWidth(150)
		self.thickStemLabelLineEdit.move(10, 60)
		self.thickStemLabelLineEdit.returnPressed.connect(self.brushThickStem)
		

		# round stem
		btn_roundStem = QPushButton('Round', self)
		btn_roundStem.clicked.connect(self.brushRoundStem)
		btn_roundStem.setStyleSheet('QPushButton {color: black;background-color:magenta;border-radius:5px}'
			'QPushButton:pressed {color: magenta;background-color:black;border-radius:5px}')
		btn_roundStem.setFixedWidth(100)
		btn_roundStem.move(10, 90)

		self.roundStemLabelLineEdit = QLineEdit(self)
		self.roundStemLabelLineEdit.setStyleSheet('background-color:black; color:white; border: 0px')
		self.roundStemLabelLineEdit.setText(str(self.roundStemValue))
		self.roundStemLabelLineEdit.setFixedWidth(150)
		self.roundStemLabelLineEdit.move(10, 120)
		self.roundStemLabelLineEdit.returnPressed.connect(self.brushRoundStem)

		# thins
		btn_thinStem = QPushButton('Thin', self)
		btn_thinStem.clicked.connect(self.brushThinStem)
		btn_thinStem.setStyleSheet('QPushButton {color: black;background-color:yellow;border-radius:5px}'
			'QPushButton:pressed {color: yellow;background-color:black;border-radius:5px}')
		btn_thinStem.setFixedWidth(100)
		btn_thinStem.move(10, 150)

		self.thinStemLabelLineEdit = QLineEdit(self)
		self.thinStemLabelLineEdit.setStyleSheet('background-color:black; color:white; border: 0px')
		self.thinStemLabelLineEdit.setText(str(self.roundStemValue))
		self.thinStemLabelLineEdit.setFixedWidth(150)
		self.thinStemLabelLineEdit.move(10, 180)
		self.thinStemLabelLineEdit.returnPressed.connect(self.brushThinStem)

		# diagnals
		btn_diagnalStem = QPushButton('Diagnal Stem', self)
		btn_diagnalStem.clicked.connect(self.brushDiagnalStem)
		btn_diagnalStem.setStyleSheet('QPushButton {color: black;background-color:green;border-radius:5px}'
			'QPushButton:pressed {color: green;background-color:black;border-radius:5px}')
		btn_diagnalStem.setFixedWidth(100)
		btn_diagnalStem.move(10, 210)

		self.diagnalStemLabelLineEdit = QLineEdit(self)
		self.diagnalStemLabelLineEdit.setStyleSheet('background-color:black; color:white; border: 0px')
		self.diagnalStemLabelLineEdit.setText(str(self.diagnalStemValue))
		self.diagnalStemLabelLineEdit.setFixedWidth(150)
		self.diagnalStemLabelLineEdit.move(10, 240)
		self.diagnalStemLabelLineEdit.returnPressed.connect(self.brushDiagnalStem)


		self.show()



	def brushThickStem(self):
		text=self.thickStemLabelLineEdit.text().split(',')
		text = list(map(int,text))
		self.brushParameters = text
		self.brushState = self.brushThickStem 


	def brushRoundStem(self):
		text=self.roundStemLabelLineEdit.text().split(',')
		text = list(map(int,text))
		self.brushParameters = text
		self.brushState = self.brushRoundStem

	def brushThinStem(self):
		text=self.thinStemLabelLineEdit.text().split(',')
		text = list(map(int,text))
		self.brushParameters = text
		self.brushState = self.brushThinStem

	def brushDiagnalStem(self):
		text=self.diagnalStemLabelLineEdit.text().split(',')
		text = list(map(int,text))
		self.brushParameters = text
		self.brushState = self.brushDiagnalStem

	def paintEvent(self, event):
		canvasPainter = QPainter(self)
		canvasPainter.drawImage(self.rect(),self.sketch)
		canvasPainter.drawImage(self.rect(),self.design)
		self.update()

		# print('lines # ' + str(len(lines)))


	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.drawing = True
			self.lastPoint = event.pos()
			# print('left click!')
			line = QPainterPath()
			line.moveTo(event.pos().x(),event.pos().y())
			self.returnList().append(line)
			# self.update()


	def mouseMoveEvent(self, event):
		if (event.buttons() == Qt.LeftButton) == self.drawing:
			line = self.returnList()[-1]
			line.lineTo(event.pos().x(),event.pos().y())
			painter = QPainter(self.sketch)
			if self.brushState == self.brushThickStem: 
				painter.setPen(QPen(Qt.cyan, 1, Qt.SolidLine))
			if self.brushState == self.brushRoundStem: 
				painter.setPen(QPen(Qt.magenta, 1, Qt.SolidLine))
			if self.brushState == self.brushThinStem: 
				painter.setPen(QPen(Qt.yellow, 1, Qt.SolidLine))
			if self.brushState == self.brushDiagnalStem: 
				painter.setPen(QPen(Qt.green, 1, Qt.SolidLine))
			painter.drawPath(self.returnList()[-1])
			self.update()

	def mouseReleaseEvent(self,event):

		self.drawFancyPath(self.returnList()[-1])
		self.update()

	def fancyPath(self,pline,thickness):
		fancyLine = pline.fancy_curve(samples_per=24, thicknesses=thickness)
		fancyPath = QPainterPath()
		fancyPath.setFillRule(1) # 
		fancyPath.moveTo(float(fancyLine.vertices[0][0]), float(fancyLine.vertices[0][1]))
		for i in fancyLine.vertices[1:]:
			fancyPath.lineTo(float(i[0]),float(i[1]))
		return fancyPath

	def drawFancyPath(self, linegroup):
			if linegroup.elementCount() > 3: ## Polyline needs at least 3 vertices
			#making Polyline
				plinePoints =[]
				for i in range(linegroup.elementCount()):
					plinePoints.append([linegroup.elementAt(i).x,linegroup.elementAt(i).y])
				pline = Polyline(plinePoints)
				thickness = self.brushParameters
				fancyPline = self.fancyPath(pline,thickness)
				painter = QPainter(self.design)
				painter.setPen(QPen(Qt.white))
				painter.setBrush(QColor(255,255,255))
				painter.drawPath(fancyPline)


	def returnList(self): 
		## Keeps track of which list lines should be stored in
			if self.brushState == self.brushThickStem: 
				return self.thickStemLines
			if self.brushState == self.brushRoundStem: 
				return self.roundStemLines
			if self.brushState == self.brushThinStem: 
				return self.thinStemLines
			if self.brushState == self.brushDiagnalStem: 
				return self.diagnalStemLines

	def close_application(self):
		print('Exit!')
		sys.exit()

	def clear_design(self):
		self.design.fill(QColor(0,0,0,0))
		self.update()

	def clear_sketch(self):
		self.sketch.fill(Qt.black)
		self.update()

	def update_design(self):
		currBrushParameters = self.brushParameters
		currBrushState = self.brushState
		for item in self.thickStemLines:
			self.brushThickStem()
			self.drawFancyPath(item)
		for item in self.roundStemLines:
			self.brushRoundStem()
			self.drawFancyPath(item)
		for item in self.thinStemLines:
			self.brushThinStem()
			self.drawFancyPath(item)
		for item in self.diagnalStemLines:
			self.brushDiagnalStem()
			self.drawFancyPath(item)

		self.brushParameters = currBrushParameters
		self.brushState = currBrushState
		self.update()

	def clear_lines(self):
		self.thickStemLines = []
		self.roundStemLines = []
		self.thinStemLines = []
		self.diagnalStemLines = []


def run():
	if __name__ == '__main__':
		app = QApplication(sys.argv)
		window = Window()
		window.show()
		sys.exit(app.exec_())

run()