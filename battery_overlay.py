from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow

from PIL import ImageQt, Image

import psutil


img = Image.open
PERCENTAGES_TO_IMAGES = {
    i: img("battery.png")
    for i in range(100)
}

def get_percentage() -> int:
    return int(psutil.sensors_battery().percent)

class BatteryIndicator(QMainWindow):
    def show_battery_level(self, percentage):
        image = PERCENTAGES_TO_IMAGES[percentage]
        screen_size = app.primaryScreen().size()
        pixel_ratio = app.devicePixelRatio() ** -1
        width = int(image.width * pixel_ratio)
        height = int(image.height * pixel_ratio)
        x = screen_size.width() - width
        y = screen_size.height() - height
        self.setGeometry(x, y, width, height)

        self.background = QPixmap.fromImage(ImageQt.ImageQt(image))
        self.show()
        QTimer.singleShot(5000, self.hide)

    def check_battery_level(self):
        percentage = get_percentage()
        if (
                percentage < self.last_percentage
                and percentage in PERCENTAGES_TO_IMAGES
        ):
            self.show_battery_level(percentage)
        self.last_percentage = percentage

    def __init__(self):
        super().__init__()

        self.last_percentage = get_percentage()

        self.setWindowOpacity(1)

        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.check_battery_level)
        self.check_timer.start(500)

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
