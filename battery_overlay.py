from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow

from PIL import ImageFilter, ImageQt, Image, ImageDraw, ImageFont

import psutil


ACTIVATION_PERCENTAGES = list(range(100))
IMAGE = Image.open("battery.png")
FONT = ImageFont.truetype("font.ttf", 70)


def draw_fn(draw, percentage):
    percentage = str(percentage) + "%"
    _, _, w, h = draw.textbbox((0, 0), percentage, font=FONT)
    x = (IMAGE.width - w) / 2
    y = (IMAGE.height - h) / 2
    draw.text((x, y), percentage, fill='blue', font=FONT)


class BatteryIndicator(QMainWindow):
    def check_battery_level(self):
        percentage = int(psutil.sensors_battery().percent)
        if percentage < self.last_percentage and percentage in ACTIVATION_PERCENTAGES:
            image = IMAGE.copy()
            draw = ImageDraw.Draw(image)
            draw_fn(draw, percentage)
            blurred = image.filter(ImageFilter.GaussianBlur(radius = 20))
            blurred.alpha_composite(image, (0, 0))
            image = blurred
            self.background = QPixmap.fromImage(ImageQt.ImageQt(image))
            self.show()
            QTimer.singleShot(5000, self.hide)
        self.last_percentage = percentage

    def __init__(self):
        super().__init__()

        self.last_percentage = int(psutil.sensors_battery().percent)

        self.setWindowOpacity(1)

        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.check_battery_level)
        self.check_timer.start(500)

        screen_size = app.primaryScreen().size()
        pixel_ratio = app.devicePixelRatio() ** -1
        width = int(IMAGE.width * pixel_ratio)
        height = int(IMAGE.height * pixel_ratio)
        x = screen_size.width() - width
        y = screen_size.height() - height
        self.setGeometry(x, y, width, height)

        self.setWindowFlags(
            self.windowFlags()
            | Qt.WindowType.WindowTransparentForInput
            | Qt.WindowType.X11BypassWindowManagerHint
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def paintEvent(self, _event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background)

app = QApplication([])
window = BatteryIndicator()
app.exec()
