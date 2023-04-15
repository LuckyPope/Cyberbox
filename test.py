import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QKeyEvent
from PyQt5.QtCore import Qt


class MyScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.item_list = []
        self.selected_item = None
        self.field = [[1, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]
        self.initUI()

    def initUI(self):
        # Создаем элементы для графической сцены
        for i in range(4):
            for j in range(4):
                if self.field[i][j] == 1:
                    pixmap = QPixmap("images/Player.png")
                    item = QGraphicsPixmapItem(pixmap)
                    item.setPos(j*100, i*100)
                    self.item_list.append(item)
                    self.addItem(item)

        # Устанавливаем фокус на графическую сцену
        self.setFocus()

    def keyPressEvent(self, event: QKeyEvent):
        # Обрабатываем нажатие клавиш
        if event.key() == Qt.Key_Left:
            self.move_item(-1, 0)
        elif event.key() == Qt.Key_Right:
            self.move_item(1, 0)
        elif event.key() == Qt.Key_Up:
            self.move_item(0, -1)
        elif event.key() == Qt.Key_Down:
            self.move_item(0, 1)

    def move_item(self, x, y):
        # Перемещаем выбранный элемент
        if self.selected_item is not None:
            pos = self.selected_item.pos()
            new_x = pos.x() + x*100
            new_y = pos.y() + y*100
            if new_x >= 0 and new_x <= 300 and new_y >= 0 and new_y <= 300:
                self.selected_item.setPos(new_x, new_y)

    def mousePressEvent(self, event):
        # Обрабатываем клик мыши для выбора элемента
        pos = event.scenePos()
        items = self.items(pos)
        for item in items:
            if isinstance(item, QGraphicsPixmapItem):
                self.selected_item = item
                break


if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = MyScene()
    view = QGraphicsView(scene)
    view.show()
    sys.exit(app.exec())