# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(833, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(40, 40, 711, 461))
        self.frame.setStyleSheet("background-color: lightgray;")
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(290, 10, 171, 41))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(70, 80, 101, 16))
        self.label_2.setObjectName("label_2")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(60, 140, 181, 221))
        self.frame_2.setStyleSheet("background-color: lightgray;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        self.verticalSlider_2 = QtWidgets.QSlider(self.frame_2)
        self.verticalSlider_2.setGeometry(QtCore.QRect(60, 20, 22, 180))  # 35-20 arası konumlandırıldı
        self.verticalSlider_2.setStyleSheet("QSlider::groove:vertical {\n"
"    background: white;\n"
"    border: 1px solid black;\n"
"    width: 20px; /* Genişliği isteğe göre ayarlayın */\n"
"}\n"
"\n"
"QSlider::handle:vertical {\n"
"    background: red;\n"
"    border: 1px solid black;\n"
"    height: 20px;\n"
"    margin: -5px 0;\n"
"}\n"
"")
        self.verticalSlider_2.setMinimum(20)
        self.verticalSlider_2.setMaximum(35)
        self.verticalSlider_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_2.setTickInterval(5)
        self.verticalSlider_2.setObjectName("verticalSlider_2")

        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setGeometry(QtCore.QRect(100, 20, 41, 180))  # Slider ile aynı yükseklikte
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")

        self.scaleWidget = TemperatureScaleWidget(self.frame_3)
        self.scaleWidget.setGeometry(0, 0, 41, 180)  # Ölçek widget'ı için konum ve boyut ayarlandı

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 833, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Greenhouse Control"))
        self.label_2.setText(_translate("MainWindow", "Temperature"))

class TemperatureScaleWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(180)  # Widget yüksekliği

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        width = self.width()
        height = self.height()
        margin = 5
        num_intervals = 3  # 35, 30, 25, 20 arası 3 interval
        interval_height = (height - 2 * margin) / num_intervals / 5  # Her aralık 5 çizgi olacak şekilde ayarlandı

        pen = QtGui.QPen(QtCore.Qt.black)  # Siyah kalem
        pen.setWidth(2)  # Kalem kalınlığı 2 piksel olarak ayarlandı
        painter.setPen(pen)

        # Slider'ın geometrisini kullanarak çizgilerin uzunluğunu ayarlama
        slider_width = 22  # Slider genişliği
        long_line_length = width - margin - slider_width - 10
        short_line_length = long_line_length - 10

        for i in range((num_intervals + 1) * 5):
            y = margin + i * interval_height
            if i % 5 == 0:
                painter.drawLine(margin, y, margin + long_line_length, y)
                painter.drawText(margin + long_line_length + 5, y + 5, f"{35 - (i//5)*5}")
            else:
                painter.drawLine(margin, y, margin + long_line_length, y)
        painter.end()

        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
