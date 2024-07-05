import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QDial
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QPainterPath, QPen
from PyQt5.QtCore import Qt, QRectF, QPoint

class CustomDial(QDial):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setNotchesVisible(True)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        rect = self.rect()
        center = rect.center()
        radius = min(rect.width(), rect.height()) / 2 - 10

        # Draw additional custom graphics or modifications if needed
        # For example, you could draw lines, shapes, etc.

class WateringSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Watering System')
        self.setGeometry(100, 100, 300, 400)

        main_layout = QVBoxLayout()

        # Step 1: Title
        self.title = QLabel('Watering System', self)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont('Arial', 20))
        main_layout.addWidget(self.title)

        # Step 2: Dial and Water Drops Layout
        dial_layout = QVBoxLayout()
        self.dial = CustomDial(self)
        self.dial.setRange(0, 3)
        self.dial.valueChanged.connect(self.updateWateringLevel)
        dial_layout.addWidget(self.dial, alignment=Qt.AlignCenter)

        # Step 3: Water drops
        self.drop_layout = QHBoxLayout()
        self.water_drops = []
        for i in range(3):
            drop = QLabel(self)
            pixmap = QPixmap(30, 50)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            path = QPainterPath()
            path.moveTo(15, 40)
            path.cubicTo(30, 35, 25, 10, 15, 0)
            path.cubicTo(5, 10, 0, 35, 15, 40)
            painter.setBrush(QColor('blue'))
            painter.drawPath(path)
            painter.end()
            drop.setPixmap(pixmap)
            drop.setVisible(False)  # Start with drops hidden
            self.water_drops.append(drop)
            self.drop_layout.addWidget(drop)

        dial_layout.addLayout(self.drop_layout)
        main_layout.addLayout(dial_layout)

        # Step 4: Text indicators
        self.text_indicators = []
        for i in range(4):
            text = QLabel(str(i), self)
            text.setAlignment(Qt.AlignCenter)
            text.setFont(QFont('Arial', 18))
            self.text_indicators.append(text)
            main_layout.addWidget(text)

        self.setLayout(main_layout)
        self.updateWateringLevel(0)

    def updateWateringLevel(self, value):
        for i, drop in enumerate(self.water_drops):
            drop.setVisible(i < value)
        for i, text in enumerate(self.text_indicators):
            text.setVisible(i == value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WateringSystem()
    ex.show()
    sys.exit(app.exec_())
