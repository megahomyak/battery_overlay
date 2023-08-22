#include <QApplication>
#include <QCoreApplication>
#include <QDesktopWidget>
#include <QMainWindow>
#include <QPainter>
#include <QPixmap>
#include <QRect>
#include <QScreen>
#include <QTimer>

#include <fstream>
#include <iostream>
#include <stdio.h>

void die(const char *text) {
  perror(text);
  exit(-1);
}

int get_percentage() {
  int percentage;
  FILE *batteryFile = fopen("/sys/class/power_supply/BAT1/capacity", "r");
  if (batteryFile == NULL) {
    die("no battery file found");
  }
  if (fscanf(batteryFile, "%d", &percentage) != 1) {
    die("can't read the percentage from the battery file");
  }
  fclose(batteryFile);
  return percentage;
}

class BatteryIndicator : public QMainWindow {
  Q_OBJECT;

public:
  BatteryIndicator() : QMainWindow() {
    last_percentage = get_percentage();

    setWindowOpacity(1);

    check_timer = new QTimer(this);
    connect(check_timer, &QTimer::timeout, this,
            &BatteryIndicator::check_battery_level);
    check_timer->start(500);

    setWindowFlags(windowFlags() | Qt::WindowTransparentForInput |
                   Qt::X11BypassWindowManagerHint | Qt::FramelessWindowHint |
                   Qt::WindowStaysOnTopHint);
    setAttribute(Qt::WA_TranslucentBackground);
    setAttribute(Qt::WA_TransparentForMouseEvents);
    setAttribute(Qt::WA_TransparentForMouseEvents);
  }

protected:
  void paintEvent(QPaintEvent *_event) override {
    QPainter painter(this);
    painter.drawPixmap(rect(), background);
  }

private slots:
  void check_battery_level() {
    int percentage = get_percentage();
    if (percentage < last_percentage &&
        PERCENTAGES_TO_IMAGES.contains(percentage)) {
      show_battery_level(percentage);
    }
    last_percentage = percentage;
  }

  void show_battery_level(int percentage) {
    background = PERCENTAGES_TO_IMAGES[percentage];
    QScreen *primaryScreen = QGuiApplication::primaryScreen();
    qreal pixel_ratio = 1.0 / primaryScreen->devicePixelRatio();
    int width = static_cast<int>(background.width() * pixel_ratio);
    int height = static_cast<int>(background.height() * pixel_ratio);
    int x = primaryScreen->size().width() - width;
    int y = primaryScreen->size().height() - height;
    setGeometry(x, y, width, height);

    show();
    QTimer::singleShot(5000, this, &QWidget::hide);
  }

private:
  QPixmap background;
  int last_percentage;
  QTimer *check_timer;
};

int main(int argc, char **argv) {
  QApplication app(argc, argv);

  QMap<int, QPixmap> PERCENTAGES_TO_IMAGES;
  for (int i = 0; i < 100; ++i) {
    PERCENTAGES_TO_IMAGES[i] = QPixmap("battery.png");
  }

  BatteryIndicator window;
  return app.exec();
}
