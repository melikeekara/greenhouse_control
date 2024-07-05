import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QDial
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QFont, QPainter, QColor, QPolygon, QPen
from PyQt5.QtCore import QPoint


class HumidityControl(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 400)
        self.setWindowTitle('Humidity Control')

        self.layout = QVBoxLayout()

        self.title = QLabel('Humidity', self)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont('Arial', 16))

        self.dial = QDial(self)
        self.dial.setMinimum(50)
        self.dial.setMaximum(100)
        self.dial.setValue(50)
        self.dial.setNotchesVisible(True)
        self.dial.valueChanged.connect(self.updateHumidity)

        self.humidity_label = QLabel('50.00%', self)
        self.humidity_label.setAlignment(Qt.AlignCenter)
        self.humidity_label.setFont(QFont('Arial', 16))

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.dial)
        self.layout.addWidget(self.humidity_label)

        self.setLayout(self.layout)

    @pyqtSlot()
    def updateHumidity(self):
        value = self.dial.value()
        self.humidity_label.setText(f'{value:.2f}%')
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.dial.geometry()
        value = self.dial.value()

        # Draw the analog display polygon
        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(QColor(0, 128, 255))

        angle = (value - self.dial.minimum()) / (self.dial.maximum() - self.dial.minimum()) * 300 - 150
        radius = min(rect.width(), rect.height()) / 2 * 0.8
        center = QPoint(rect.center().x(), rect.center().y() + 20)
        end_point = center + QPoint(radius * -math.sin(angle * math.pi / 180), radius * -math.cos(angle * math.pi / 180))

        points = QPolygon([center, QPoint(center.x() - 5, center.y()), end_point, QPoint(center.x() + 5, center.y())])
        painter.drawPolygon(points)

        # Draw the tick marks
        painter.setPen(QPen(Qt.black))
        for i in range(self.dial.minimum(), self.dial.maximum() + 1, 10):
            angle = (i - self.dial.minimum()) / (self.dial.maximum() - self.dial.minimum()) * 300 - 150
            tick_start = center + QPoint(radius * -math.sin(angle * math.pi / 180) * 0.8, radius * -math.cos(angle * math.pi / 180) * 0.8)
            tick_end = center + QPoint(radius * -math.sin(angle * math.pi / 180), radius * -math.cos(angle * math.pi / 180))
            painter.drawLine(tick_start, tick_end)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HumidityControl()
    ex.show()
    sys.exit(app.exec_())
