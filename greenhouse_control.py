import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QDial, QSlider, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsRectItem, QGraphicsPolygonItem, QPushButton, QGraphicsProxyWidget
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QPainterPath, QBrush, QPolygonF, QPen
from PyQt5.QtCore import Qt, pyqtSlot, QRectF, QPointF, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QSpacerItem, QSizePolicy


class GreenhouseControl(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Greenhouse Control')
        self.setGeometry(100, 100, 800, 600)

        self.setFixedSize(850, 700)# ekran boyutunu sabitledim.

        main_layout = QVBoxLayout()

        # başlık etiketi
        title = QLabel('Greenhouse Control', self)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Arial', 24))
        main_layout.addWidget(title)

        # sistemler için grid..
        grid_layout = QGridLayout()

        # sistemleri gride ekledim.
        grid_layout.addWidget(self.createTemperatureControl(), 0, 0, 1, 1)
        grid_layout.addWidget(self.createLightingSystem(), 1, 0, 1, 1)
        grid_layout.addWidget(self.createHumidityControl(), 0, 1, 1, 1)
        grid_layout.addWidget(self.createWateringSystem(), 0, 2, 1, 1)
        grid_layout.addWidget(self.createSoilAcidity(), 1, 2, 1, 1)


        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

    def createWateringSystem(self):
        return WateringSystem() #watering sistemi oluşturdum.

    def createHumidityControl(self): #
        humidity_widget = QWidget()
        humidity_layout = QVBoxLayout(humidity_widget)
        humidity_layout.setContentsMargins(0, 0, 50, 0)  
        humidity_layout.setSpacing(0)  #boşlukları kaldırmak için

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

        dial.valueChanged.connect(updateHumidity) #nem değeri değiştitiğinde güncellemek için

        return humidity_widget

    def createLightingSystem(self):
        lighting_widget = LightingSystem() #ligting bileşenini oluştur.
        lighting_layout = QVBoxLayout()
        lighting_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        lighting_layout.setSpacing(0)  # Remove spacing

        title = QLabel('Lighting System', self)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Arial', 16))

        lighting_layout.addWidget(title)
        lighting_layout.addWidget(lighting_widget)

        lighting_container = QWidget()
        lighting_container.setLayout(lighting_layout)

        return lighting_container

    def createSoilAcidity(self):
        soil_acidity_widget = QWidget()
        soil_acidity_layout = QVBoxLayout(soil_acidity_widget)
        soil_acidity_layout.setContentsMargins(0, 50, 0, 0)  # Remove margins
        soil_acidity_layout.setSpacing(0)  # Remove spacing

        title = QLabel('Soil Acidity', self)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Arial', 16))

        soil_acidity_layout.addStretch()

        soil_acidity_layout.addWidget(title)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        soil_acidity_layout.addItem(spacer)

        view = QGraphicsView()
        view.setStyleSheet("background-color: rgb(240, 240, 240);")
        view.setFixedSize(300, 200)
        scene = QGraphicsScene()
        view.setScene(scene)
        soil_acidity_layout.addWidget(view)

        # pH göstergesi
        self.pH_display_text = QGraphicsTextItem('6')
        self.pH_display_text.setDefaultTextColor(Qt.white)
        text_rect = self.pH_display_text.boundingRect()
        self.pH_display_bg = QGraphicsRectItem(text_rect)
        self.pH_display_bg.setBrush(QBrush(Qt.black))
        self.pH_display_bg.setPos(100, 30)
        self.pH_display_text.setPos(100, 30)
        scene.addItem(self.pH_display_bg)
        scene.addItem(self.pH_display_text)

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
            self.pH_display_text.setPlainText(str(value))
            text_rect = self.pH_display_text.boundingRect()
            self.pH_display_bg.setRect(text_rect)
            pos_x = 10 + (value - 1) * (180 / 13)
            pointer.setPos(pos_x, 60)

            self.pH_display_text.setPos(100, 30)
            self.pH_display_bg.setPos(100, 30)

            if value >= 1 and value <= 5:
                self.pH_display_text.setDefaultTextColor(Qt.red)
            elif value >= 6 and value <= 9:
                self.pH_display_text.setDefaultTextColor(Qt.yellow)
            else:
                self.pH_display_text.setDefaultTextColor(Qt.green)

        slider.valueChanged.connect(updateAcidity)

        soil_acidity_widget.adjustSize()
        soil_acidity_widget.setFixedSize(soil_acidity_widget.sizeHint())

        return soil_acidity_widget
    
    def createTemperatureControl(self):
        return Thermometer()

#termometre classı
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

        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

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
        self.title.setFont(QFont('Arial', 16))
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


class LightingSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Lighting System')
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(50, 5, 0, 0)  # Remove margins
        self.layout.setSpacing(0)  # Remove spacing

        self.view = QGraphicsView()
        self.view.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.view.setFixedSize(300, 200)  # Set background color to match GreenhouseControl
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.layout.addWidget(self.view)

        self.createLightingSystem()

        self.setLayout(self.layout)

        # Automatically resize the widget to fit the contents
        self.adjustSize()
        self.setFixedSize(self.sizeHint())

    def createLightingSystem(self):
        
        self.colors = [QColor(255, 0, 0), QColor(255, 165, 0), QColor(255, 255, 0)]
        self.positions = [(50, 50), (50, 100), (50, 150)]

        button_width = 40
        button_height = 30
        button_margin = 10  # Margin between circle and button

        for i, (color, pos) in enumerate(zip(self.colors, self.positions)):
            circle = QGraphicsEllipseItem(QRectF(0, 0, 40, 40))
            circle.setBrush(QBrush(color))
            circle.setPos(*pos)
            self.scene.addItem(circle)

            button = QPushButton('')
            button.setStyleSheet('border: 2px solid black; border-radius: 5px; background: none;')  # Style for the buttons
            button.setFixedSize(button_width, button_height)

            # Create a QGraphicsProxyWidget to embed the QPushButton in the QGraphicsScene
            proxy = QGraphicsProxyWidget()
            proxy.setWidget(button)
            proxy.setPos(pos[0] + 50 + button_margin, pos[1] + 5)  # Adjusted position to place next to circle
            self.scene.addItem(proxy)

            # Connect the button click to the setLighting method
            button.clicked.connect(lambda _, level=i: self.setLighting(level))

        # Position the main control to the right of the buttons and in the empty space
        self.main_control = QGraphicsEllipseItem(QRectF(0, 0, 80, 80))
        self.main_control.setBrush(QBrush(QColor(255, 255, 0)))
        self.main_control.setPos(200, 70)  # Adjust x and y coordinates to position in the right empty space
        self.scene.addItem(self.main_control)

    def setLighting(self, level):
        # Change the brush color of the main control circle
        self.main_control.setBrush(QBrush(self.colors[level]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    control_panel = GreenhouseControl()
    control_panel.show()
    sys.exit(app.exec_())
