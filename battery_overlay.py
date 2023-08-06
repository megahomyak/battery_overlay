import time

from PyQt5.QtCore import QPoint, Qt, QTimer
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

import psutil


class BatteryIndicator(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowOpacity(0.5)
        self.lastPoint = QPoint()
        self.background = QPixmap("../../website_icon.png")
        QTimer.singleShot(5000, QApplication.quit)
        width = self.background.width()
        height = self.background.height()
        x = 300
        y = 300
        self.setGeometry(x, y, width, height)
        self.setWindowFlags(
            self.windowFlags()
            | Qt.WindowTransparentForInput
            | Qt.X11BypassWindowManagerHint
        )

    def paintEvent(self, _event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background)


app = QApplication([])
window = BatteryIndicator()
window.show()
app.exec()
