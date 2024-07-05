import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QDial, QSlider, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsRectItem, QGraphicsPolygonItem
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QPainterPath, QBrush, QPolygonF, QPen
from PyQt5.QtCore import Qt, pyqtSlot, QRectF, QPointF, QPoint


class GreenhouseControl(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Greenhouse Control')
        self.setGeometry(100, 100, 800, 600)
        
        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel('Greenhouse Control', self)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Arial', 24))
        main_layout.addWidget(title)
        
        # Create a grid layout for the systems
        grid_layout = QHBoxLayout()
        
        # Left Column (Temperature, Watering System)
        left_col = QVBoxLayout()
        left_col.addWidget(self.createTemperatureControl())
        left_col.addWidget(self.createWateringSystem())
        
        # Center Column (Lighting System)
        center_col = QVBoxLayout()
        center_col.addWidget(self.createLightingSystem())
        
        # Right Column (Humidity, Soil Acidity)
        right_col = QVBoxLayout()
        right_col.addWidget(self.createHumidityControl())
        right_col.addWidget(self.createSoilAcidity())
        
        grid_layout.addLayout(left_col)
        grid_layout.addLayout(center_col)
        grid_layout.addLayout(right_col)
        
        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)
    
    def createWateringSystem(self):
        watering_widget = QWidget()
        watering_layout = QVBoxLayout(watering_widget)
        
        # Step 1: Title
        title = QLabel('Watering System', self)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Arial', 16))
        watering_layout.addWidget(title)
        
        # Step 2: Dial and Water Drops Layout
        dial_layout = QVBoxLayout()
        dial = QDial(self)
        dial.setRange(0, 3)
        dial.setNotchesVisible(True)
        dial_layout.addWidget(dial, alignment=Qt.AlignCenter)

        # Step 3: Water drops
        drop_layout = QHBoxLayout()
        water_drops = []
        for i in range(3):
            drop = QLabel(self)
            pixmap = QPixmap(30, 30)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            path = QPainterPath()
            path.moveTo(15, 0)
            path.quadTo(30, 15, 15, 30)
            path.quadTo(0, 15, 15, 0)
            painter.setBrush(QColor('blue'))
            painter.drawPath(path)
            painter.end()
            drop.setPixmap(pixmap)
            drop.setVisible(False)
            water_drops.append(drop)
            drop_layout.addWidget(drop)
        
        dial_layout.addLayout(drop_layout)
        watering_layout.addLayout(dial_layout)
        
        # Step 4: Text indicators
        text_indicators = []
        for i in range(4):
            text = QLabel(str(i), self)
            text.setAlignment(Qt.AlignCenter)
            text.setFont(QFont('Arial', 18))
            text_indicators.append(text)
            watering_layout.addWidget(text)
        
        watering_widget.water_drops = water_drops
        watering_widget.text_indicators = text_indicators
        
        def updateWateringLevel(value):
            for i, drop in enumerate(watering_widget.water_drops):
                drop.setVisible(i < value)
            for i, text in enumerate(watering_widget.text_indicators):
                text.setVisible(i == value)
        
        dial.valueChanged.connect(updateWateringLevel)
        updateWateringLevel(0)
        
        return watering_widget

    def createHumidityControl(self):
        humidity_widget = QWidget()
        humidity_layout = QVBoxLayout(humidity_widget)

        title = QLabel('Humidity', self)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Arial', 16))

        dial = QDial(self)
        dial.setMinimum(50)
        dial.setMaximum(100)
        dial.setValue(50)
        dial.setNotchesVisible(True)

        humidity_label = QLabel('50.00%', self)
        humidity_label.setAlignment(Qt.AlignCenter)
        humidity_label.setFont(QFont('Arial', 16))

        humidity_layout.addWidget(title)
        humidity_layout.addWidget(dial)
        humidity_layout.addWidget(humidity_label)

        def updateHumidity():
            value = dial.value()
            humidity_label.setText(f'{value:.2f}%')
            humidity_widget.update()

        dial.valueChanged.connect(updateHumidity)

        return humidity_widget

    def createLightingSystem(self):
        lighting_widget = QWidget()
        lighting_layout = QVBoxLayout(lighting_widget)

        view = QGraphicsView()
        scene = QGraphicsScene()
        view.setScene(scene)
        lighting_layout.addWidget(view)

        title = QGraphicsTextItem('Lighting System')
        title.setDefaultTextColor(Qt.white)
        title.setPos(50, 10)
        scene.addItem(title)

        colors = [QColor(255, 0, 0), QColor(255, 165, 0), QColor(255, 255, 0)]
        positions = [(50, 50), (50, 100), (50, 150)]
        
        button_width = 60
        button_height = 40
        button_margin = 10

        main_control = QGraphicsEllipseItem(QRectF(0, 0, 80, 80))
        main_control.setBrush(QBrush(QColor(255, 255, 0)))
        main_control.setPos(150, 100)
        scene.addItem(main_control)

        def setLighting(level):
            main_control.setBrush(QBrush(colors[level]))

        for i, (color, pos) in enumerate(zip(colors, positions)):
            circle = QGraphicsEllipseItem(QRectF(0, 0, 40, 40))
            circle.setBrush(QBrush(color))
            circle.setPos(*pos)
            scene.addItem(circle)
            
        return lighting_widget

    def createSoilAcidity(self):
        soil_acidity_widget = QWidget()
        soil_acidity_layout = QVBoxLayout(soil_acidity_widget)

        view = QGraphicsView()
        scene = QGraphicsScene()
        view.setScene(scene)
        soil_acidity_layout.addWidget(view)

        title = QGraphicsTextItem('Soil Acidity')
        title.setDefaultTextColor(Qt.white)
        title.setPos(50, 10)
        scene.addItem(title)

        pH_display = QGraphicsTextItem('6')
        pH_display.setDefaultTextColor(Qt.black)
        pH_display.setPos(100, 30)
        scene.addItem(pH_display)
        
        red_zone = QGraphicsRectItem(QRectF(10, 70, 60, 20))
        red_zone.setBrush(QBrush(QColor(255, 0, 0)))
        scene.addItem(red_zone)
        
        yellow_zone = QGraphicsRectItem(QRectF(70, 70, 60, 20))
        yellow_zone.setBrush(QBrush(QColor(255, 255, 0)))
        scene.addItem(yellow_zone)
        
        green_zone = QGraphicsRectItem(QRectF(130, 70, 60, 20))
        green_zone.setBrush(QBrush(QColor(0, 255, 0)))
        scene.addItem(green_zone)
        
        pointer = QGraphicsPolygonItem(QPolygonF([QPointF(-5, -10), QPointF(5, -10), QPointF(0, 0)]))
        pointer.setBrush(QBrush(Qt.black))
        pointer.setPos(10 + (6 - 1) * (180 / 13), 60)
        scene.addItem(pointer)
        
        slider = QSlider(Qt.Horizontal)
        slider.setRange(1, 14)
        slider.setValue(6)
        soil_acidity_layout.addWidget(slider)

        def updateAcidity(value):
            pH_display.setPlainText(str(value))
            pos_x = 10 + (value - 1) * (180 / 13)
            pointer.setPos(pos_x, 60)
            
            if value >= 1 and value <= 5:
                pH_display.setDefaultTextColor(Qt.red)
            elif value >= 6 and value <= 9:
                pH_display.setDefaultTextColor(Qt.yellow)
            else:
                pH_display.setDefaultTextColor(Qt.green)

        slider.valueChanged.connect(updateAcidity)

        return soil_acidity_widget

    def createTemperatureControl(self):
        return Thermometer()


class Thermometer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 400)
        self.setWindowTitle('Temperature Control')
        
        self.layout = QVBoxLayout()

        self.title = QLabel('Temperature', self)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont('Arial', 16))
        

        self.slider = QSlider(Qt.Vertical, self)
        self.slider.setMinimum(20)
        self.slider.setMaximum(35)
        self.slider.setValue(20)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.updateTemperature)

        self.temperature_label = QLabel('20°C', self)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.temperature_label.setFont(QFont('Arial', 16))

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.temperature_label)
        
        self.setLayout(self.layout)

    @pyqtSlot()
    def updateTemperature(self):
        value = self.slider.value()
        self.temperature_label.setText(f'{value}°C')
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.slider.geometry()
        value = self.slider.value()

        # Calculate the height of the red indicator based on the slider value
        percentage = (value - self.slider.minimum()) / (self.slider.maximum() - self.slider.minimum())
        indicator_height = rect.height() * percentage

        # Draw the red indicator
        painter.setBrush(QColor(255, 0, 0))
        painter.drawRect(rect.left() + 150, rect.bottom() - indicator_height, rect.width(), indicator_height)

        # Draw the tick marks and labels
        painter.setPen(QColor(0, 0, 0))
        font = QFont('Arial', 10)
        painter.setFont(font)
        for i in range(self.slider.minimum(), self.slider.maximum() + 1, 5):
            tick_y = rect.bottom() - rect.height() * ((i - self.slider.minimum()) / (self.slider.maximum() - self.slider.minimum()))
            painter.drawLine(rect.left() + 140, tick_y, rect.left() + 150, tick_y)
            painter.drawText(rect.left() + 100, tick_y + 5, f'{i}°C')

        # Draw shorter tick marks
        for j in range(self.slider.minimum(), self.slider.maximum() + 1, 1):
            tick_y = rect.bottom() - rect.height() * ((j - self.slider.minimum()) / (self.slider.maximum() - self.slider.minimum()))
            painter.drawLine(rect.left() + 145, tick_y, rect.left() + 150, tick_y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    control_panel = GreenhouseControl()
    control_panel.show()
    sys.exit(app.exec_())
