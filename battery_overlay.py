from PyQt6.QtCore import QEasingCurve, Qt, QTimer, QPropertyAnimation, QAbstractAnimation
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QApplication, QGraphicsOpacityEffect, QMainWindow

from PIL import ImageQt, Image

import psutil


img = Image.open
PERCENTAGES_TO_IMAGES = {
    i: img("battery.png")
    for i in range(100)
}


class BatteryIndicator(QMainWindow):

    def __init__(self):
        super().__init__()

        self.painter = QPainter(self)

        self.last_percentage = int(psutil.sensors_battery().percent)

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
        self.setWindowOpacity(0)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def hide_window(self):
        effect = QGraphicsOpacityEffect(self)
        self.anim = QPropertyAnimation(effect, b"opacity")
        self.anim.setStartValue(1)
        self.anim.setDuration(20000)
        self.anim.setEasingCurve(QEasingCurve.Type.Linear)
        self.anim.setEndValue(0)
        self.anim.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    def show_battery_level(self, percentage):
        image = PERCENTAGES_TO_IMAGES[percentage]
        screen_size = app.primaryScreen().size()
        pixel_ratio = app.devicePixelRatio() ** -1
        width = int(image.width * pixel_ratio)
        height = int(image.height * pixel_ratio)
        x = screen_size.width() - width
        y = screen_size.height() - height
        self.setGeometry(x, y, width, height)

        self.anim = QPropertyAnimation(self.painter, b"opacity")
        self.anim.setStartValue(0)
        self.anim.setEasingCurve(QEasingCurve.Type.Linear)
        self.anim.setDuration(20000)
        self.anim.setEndValue(1)
        self.anim.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

        self.background = QPixmap.fromImage(ImageQt.ImageQt(image))
        QTimer.singleShot(25000, self.hide_window)

    def check_battery_level(self):
        percentage = int(psutil.sensors_battery().percent)
        if (
                percentage < self.last_percentage
                and percentage in PERCENTAGES_TO_IMAGES
        ):
            self.show_battery_level(percentage)
        self.last_percentage = percentage

    def paintEvent(self, _event):
        self.painter.begin(self)
        self.painter.drawPixmap(self.rect(), self.background)
        self.painter.end()

app = QApplication([])
window = BatteryIndicator()
window.show_battery_level(98)
app.exec()
