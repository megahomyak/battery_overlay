from PyQt5.QtCore import QPoint, Qt, QTimer
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

import psutil


ACTIVATION_PERCENTAGES = list(range(100))


class BatteryIndicator(QMainWindow):
    def check_battery_level(self):
        percentage = int(psutil.sensors_battery().percent)
        print(percentage)
        if percentage < self.last_percentage and percentage in ACTIVATION_PERCENTAGES:
            print("in")
            self.show()
            QTimer.singleShot(5000, self.hide)
        self.last_percentage = percentage

    def __init__(self):
        super().__init__()

        self.last_percentage = int(psutil.sensors_battery().percent)

        self.setWindowOpacity(0.5)
        self.lastPoint = QPoint()
        self.background = QPixmap("../../website_icon.png")
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.check_battery_level)
        self.check_timer.start(500)
        width = self.background.width()
        height = self.background.height()
        x = 300
        y = 300
        self.setGeometry(x, y, width, height)
        self.setWindowFlags(
            self.windowFlags()
            | Qt.WindowTransparentForInput
            | Qt.X11BypassWindowManagerHint
            | Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
        )

    def paintEvent(self, _event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background)


app = QApplication([])
window = BatteryIndicator()
app.exec()
