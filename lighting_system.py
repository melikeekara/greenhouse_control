import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem, QPushButton, QGraphicsProxyWidget
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QBrush, QColor

class LightingSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Lighting System')
        self.layout = QVBoxLayout()
        
        self.view = QGraphicsView()
        self.scene = QGraphicsScene(0, 0, 400, 300)  # Define the scene size
        self.view.setScene(self.scene)
        self.layout.addWidget(self.view)
        
        self.createLightingSystem()
        
        self.setLayout(self.layout)
        
    def createLightingSystem(self):
        title = QGraphicsTextItem('Lighting System')
        title.setDefaultTextColor(Qt.black)
        title.setPos(10, 10)
        self.scene.addItem(title)

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
    lighting_system = LightingSystem()
    lighting_system.show()
    sys.exit(app.exec_())
