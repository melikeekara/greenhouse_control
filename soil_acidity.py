from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QGraphicsPolygonItem
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QBrush, QColor, QPolygonF
import sys

class SoilAcidity(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Soil Acidity')
        self.layout = QVBoxLayout()
        
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.layout.addWidget(self.view)
        
        self.createSoilAcidity()
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 14)
        self.slider.setValue(6)
        self.slider.valueChanged.connect(self.updateAcidity)
        self.layout.addWidget(self.slider)
        
        self.setLayout(self.layout)
        
    def createSoilAcidity(self):
        title = QGraphicsTextItem('Soil Acidity')
        title.setDefaultTextColor(Qt.white)
        title.setPos(50, 10)
        self.scene.addItem(title)

        self.pH_display = QGraphicsTextItem('6')
        self.pH_display.setDefaultTextColor(Qt.black)
        self.pH_display.setPos(100, 30)
        self.scene.addItem(self.pH_display)
        
        # Colors for the pH zones
        self.red_zone = QGraphicsRectItem(QRectF(10, 70, 60, 20))
        self.red_zone.setBrush(QBrush(QColor(255, 0, 0)))
        self.scene.addItem(self.red_zone)
        
        self.yellow_zone = QGraphicsRectItem(QRectF(70, 70, 60, 20))
        self.yellow_zone.setBrush(QBrush(QColor(255, 255, 0)))
        self.scene.addItem(self.yellow_zone)
        
        self.green_zone = QGraphicsRectItem(QRectF(130, 70, 60, 20))
        self.green_zone.setBrush(QBrush(QColor(0, 255, 0)))
        self.scene.addItem(self.green_zone)
        
        self.pointer = QGraphicsPolygonItem(QPolygonF([QPointF(-5, -10), QPointF(5, -10), QPointF(0, 0)]))
        self.pointer.setBrush(QBrush(Qt.black))
        self.pointer.setPos(10 + (6 - 1) * (180 / 13), 60)
        self.scene.addItem(self.pointer)
        
    def updateAcidity(self, value):
        self.pH_display.setPlainText(str(value))
        pos_x = 10 + (value - 1) * (180 / 13)
        self.pointer.setPos(pos_x, 60)
        
        if value >= 1 and value <= 5:
            self.pH_display.setDefaultTextColor(Qt.red)
        elif value >= 6 and value <= 9:
            self.pH_display.setDefaultTextColor(Qt.yellow)
        else:
            self.pH_display.setDefaultTextColor(Qt.green)

app = QApplication(sys.argv)
soil_acidity = SoilAcidity()
soil_acidity.show()
sys.exit(app.exec_())
