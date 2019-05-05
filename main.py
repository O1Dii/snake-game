import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random
from copy import deepcopy


class Snake:
    def __init__(self):
        self.current_pos = [100, 100]
        self.poses: list = [[90, 100]]
        self.__direction = 2

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, direct: int):
        if 0 > direct > 3:
            raise ValueError
        else:
            self.__direction = direct


class MyWindow(QMainWindow):
    window_height = 600
    window_width = 600

    def __init__(self):
        super(QWidget, self).__init__()
        self.setGeometry(100, 100, self.window_height, self.window_width)

        # oImage = QImage("background.png")
        # sImage = oImage.scaled(QSize(self.window_height, self.window_width))
        # palette = QPalette()
        # palette.setBrush(QPalette.Window, QBrush(sImage))
        # self.setPalette(palette)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def draw(self, qp):
        global snake
        pen = QPen(QColor(255, 100, 0, 255), 10, Qt.SolidLine)
        qp.setPen(pen)
        for i in apples:
            qp.drawPoint(*i)
        if len(snake.poses) != 1:
            for i in range(len(snake.poses) - 1):
                if not (0 in snake.poses[i] or 600 in snake.poses[i]):
                    qp.drawLine(*snake.poses[i], *snake.poses[i + 1])
        else:
            qp.drawLine(*snake.current_pos, *snake.poses[0])

    def keyPressEvent(self, event):
        global snake, apples
        key = event.key()
        if key == QtCore.Qt.Key_Left:
            snake.direction = 0 if snake.direction != 2 else 2
            self.change_direction()
        elif key == QtCore.Qt.Key_Up:
            snake.direction = 1 if snake.direction != 3 else 3
            self.change_direction()
        elif key == QtCore.Qt.Key_Right:
            snake.direction = 2 if snake.direction != 0 else 0
            self.change_direction()
        elif key == QtCore.Qt.Key_Down:
            snake.direction = 3 if snake.direction != 1 else 1
            self.change_direction()
        elif key == QtCore.Qt.Key_R:
            apples = []
            snake = Snake()

    def change_direction(self):
        global snake
        # snake.poses.append((snake.current_pos.copy(), snake.direction))


def update_values():
    global snake, speed
    snake.poses.append(snake.current_pos.copy())
    if snake.direction == 0:
        if snake.current_pos[0] > 0:
            snake.current_pos[0] -= speed
        else:
            snake.current_pos[0] -= speed - 600
    elif snake.direction == 1:
        if snake.current_pos[1] > 0:
            snake.current_pos[1] -= speed
        else:
            snake.current_pos[1] -= speed - 600
    elif snake.direction == 2:
        if snake.current_pos[0] < 600:
            snake.current_pos[0] += speed
        else:
            snake.current_pos[0] += speed - 600
    else:
        if snake.current_pos[1] < 600:
            snake.current_pos[1] += speed
        else:
            snake.current_pos[1] += speed - 600

    if tuple(snake.current_pos) in apples:
        apples.remove(tuple(snake.current_pos))
    else:
        snake.poses.pop(0)

    if snake.current_pos in snake.poses:
        snake.poses = snake.poses[snake.poses.index(snake.current_pos)::2]
    mw.update()


if __name__ == '__main__':
    speed = 10
    apples = []
    snake = Snake()
    timer_speed = 0
    while True:
        try:
            timer_speed = int(input("Выберите уровень сложности:\n1. Очень сложно" +
                                    "\n2. Сложно\n3. Средне\n4. Легко\n5. Очень легко\n")) * 8
            if timer_speed < 0 or timer_speed > 50:
                print('Введено неверное значение')
                continue
        except ValueError:
            print('Введено неверное значение')
        else:
            break

    app = QApplication(sys.argv)

    mw = MyWindow()
    mw.setWindowTitle('Snake')
    mw.setWindowIcon(QIcon("icon.jpg"))

    timer = QTimer()
    timer.timeout.connect(update_values)
    timer.start(timer_speed)

    timer_apples = QTimer()
    timer_apples.timeout.connect(
        lambda: apples.append((random.randint(0, 60) * speed,
                               random.randint(0, 60) * speed
                               )))
    timer_apples.start(timer_speed * 50)

    mw.show()
    sys.exit(app.exec_())
