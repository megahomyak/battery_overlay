from PyQt5.QtCore import QPoint, Qt, QTimer
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

from PIL import ImageQt, Image, ImageDraw, ImageFont

import psutil


ACTIVATION_PERCENTAGES = list(range(100))
IMAGE = Image.open("battery.png")
FONT = ImageFont.truetype("font.ttf", 16)


def draw_fn(draw, percentage):
    percentage = str(percentage) + "%"
    _, _, w, h = draw.textbbox((0, 0), percentage, font=FONT)
    x = (IMAGE.width - w) / 2
    y = (IMAGE.height - h) / 2
    draw.text((x, y), percentage, fill='black', font=FONT)


class BatteryIndicator(QMainWindow):
    def check_battery_level(self):
        percentage = int(psutil.sensors_battery().percent)
        print(percentage)
        if percentage < self.last_percentage and percentage in ACTIVATION_PERCENTAGES:
            image = IMAGE.copy()
            draw = ImageDraw.Draw(image)
            draw_fn(draw, percentage)
            self.background = QPixmap.fromImage(ImageQt.ImageQt(image))
            self.show()
            QTimer.singleShot(5000, self.hide)
        self.last_percentage = percentage

    def __init__(self):
        super().__init__()

        self.last_percentage = int(psutil.sensors_battery().percent)

        self.setWindowOpacity(0.5)
        self.lastPoint = QPoint()

        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.check_battery_level)
        self.check_timer.start(500)

        screen_size = app.primaryScreen().size()
        width = IMAGE.width
        height = IMAGE.height
        x = screen_size.width() - IMAGE.width
        y = screen_size.height() - IMAGE.height
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
