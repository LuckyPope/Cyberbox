import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMenu, QFileDialog, QVBoxLayout, QPushButton, \
    QGridLayout, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QKeyEvent


def read_level(filename):
    f = open(filename, 'r')
    m = []
    for row in f:
        m.append([int(x) for x in row.strip().split(" ")])
    f.close()
    return m


class Player:

    def __init__(self, pX, pY):
        self.posX = pX
        self.posY = pY


class Cell(QGraphicsPixmapItem):

    def __init__(self, cellType: int):
        super(Cell, self).__init__()
        self.type = cellType
        self.setScale(2)

    def updateCell(self):
        pixmap = self.getCurrentPixmap()
        self.setPixmap(pixmap)

    def setType(self, cellType):
        self.type = cellType
        self.updateCell()

    def getCurrentPixmap(self) -> QPixmap:
        pixmap = None
        if self.type == 6:
            pixmap = QPixmap("images/Player.png")
        if self.type == 5:
            pixmap = QPixmap("images/Win_Cell.png")
        if self.type == 4:
            pixmap = QPixmap("images/Block.png")
        if self.type == 3:
            pixmap = QPixmap("images/All_Side.png")
        if self.type == 2:
            pixmap = QPixmap("images/Left_Right.png")
        if self.type == 1:
            pixmap = QPixmap("images/Up_Down.png")
        if self.type == 0:
            pixmap = QPixmap("images/Cell.png")
        return pixmap

    def isMovableX(self):
        return self.type == 3 or self.type == 2

    def isMovableY(self):
        return self.type == 3 or self.type == 1


class GameField:
    def __init__(self, lev):
        self.win = None
        self.player = None
        self.level = lev
        self.list_of_cells = []

    def initialize_level(self):
        for i, row in enumerate(self.level):
            self.list_of_cells.append([])
            for cellType in row:
                self.list_of_cells[i].append(Cell(cellType))

    def move(self, x, y):
        dp = 2
        step = 1
        length = len(self.level) - 1
        if x < 0:
            step = -1
            length = -1

        if self.list_of_cells[self.player.posY][self.player.posX + x].isMovableX():
            self.list_of_cells[self.player.posY][self.player.posX + x].setType(0)
            for i in range(self.player.posX + 2 * x, length, step):
                if self.list_of_cells[self.player.posY][self.player.posX + dp * x].isMovableX():
                    self.list_of_cells[self.player.posY][self.player.posX + dp * x].setType(2)
                    dp = dp + 1
                else:
                    break

        if self.list_of_cells[self.player.posY + y][self.player.posX].isMovableY():
            self.list_of_cells[self.player.posY + y][self.player.posX + x].setType(0)
            for i in range(self.player.posX + 2 * y, length, step):
                if self.list_of_cells[self.player.posY + dp * y][self.player.posX].isMovableY():
                    self.list_of_cells[self.player.posY + dp * y][self.player.posX].setType(1)
                    dp = dp + 1
                else:
                    break

        self.player.posX = self.player.posX + x
        self.player.posY = self.player.posY + y
        self.list_of_cells[self.player.posY - y][self.player.posX - x].setType(0)

    def keyPressEvent(self, event):
        if event.key == Qt.Key_Right and self.player.posX + 1 < len(self.level) and \
                (self.list_of_cells[self.player.posY][self.player.posX + 1].isMovableX() or
                 self.list_of_cells[self.player.posY][self.player.posX + 1].getType() == 0):
            self.move(1, 0)

        if event.key == Qt.Key_Left and self.player.posX - 1 > -1 and \
                (self.list_of_cells[self.player.posY][self.player.posX - 1].isMovableX() or
                 self.list_of_cells[self.player.posY][self.player.posX - 1].getType() == 0):
            self.move(-1, 0)

        if event.key == Qt.Key_Up and self.player.posY - 1 > - 1 and \
                (self.list_of_cells[self.player.posY - 1][self.player.posX].isMovableY() or
                 self.list_of_cells[self.player.posY - 1][self.player.posX].getType() == 0):
            self.move(0, -1)

        if event.key == Qt.Key_Down and self.player.posY + 1 < len(self.level[0]) and \
                (self.list_of_cells[self.player.posY + 1][self.player.posX].isMovableY() or
                 self.list_of_cells[self.player.posY + 1][self.player.posX].getType() == 0):
            self.move(0, 1)


class MyWindow(QGraphicsScene):

    def __init__(self):
        super().__init__()
        self.item_list = []
        self.selected_item = None
        self.matrix = read_level('levels/01.txt')
        self.initUI()
        self.game = GameField

    def initUI(self):
        # Создаем элементы для графической сцены
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j] == 6:
                    pixmap = QPixmap("images/Player.png")
                    new_pixmap = pixmap.scaled(pixmap.width() * 2, pixmap.height() * 2)
                    item = QGraphicsPixmapItem(new_pixmap)
                    self.selected_item = item
                    item.setPos(j * 64, i * 64)
                    self.selected_item = item
                    self.item_list.append(item)
                    self.addItem(item)
                if self.matrix[i][j] == 5:
                    pixmap = QPixmap("images/Win_Cell.png")
                    new_pixmap = pixmap.scaled(pixmap.width() * 2, pixmap.height() * 2)
                    item = QGraphicsPixmapItem(new_pixmap)
                    item.setPos(j * 64, i * 64)
                    self.item_list.append(item)
                    self.addItem(item)
                if self.matrix[i][j] == 4:
                    pixmap = QPixmap("images/Block.png")
                    new_pixmap = pixmap.scaled(pixmap.width() * 2, pixmap.height() * 2)
                    item = QGraphicsPixmapItem(new_pixmap)
                    item.setPos(j * 64, i * 64)
                    self.item_list.append(item)
                    self.addItem(item)
                if self.matrix[i][j] == 3:
                    pixmap = QPixmap("images/All_Side.png")
                    item = QGraphicsPixmapItem(pixmap)
                    item.setScale(2)
                    item.setPos(j * 64, i * 64)
                    self.item_list.append(item)
                    self.addItem(item)
                if self.matrix[i][j] == 2:
                    pixmap = QPixmap("images/Left_Right.png")
                    new_pixmap = pixmap.scaled(pixmap.width() * 2, pixmap.height() * 2)
                    item = QGraphicsPixmapItem(new_pixmap)
                    item.setPos(j * 64, i * 64)
                    self.item_list.append(item)
                    self.addItem(item)
                if self.matrix[i][j] == 1:
                    pixmap = QPixmap("images/Up_Down.png")
                    new_pixmap = pixmap.scaled(pixmap.width() * 2, pixmap.height() * 2)
                    item = QGraphicsPixmapItem(new_pixmap)
                    item.setPos(j * 64, i * 64)
                    self.item_list.append(item)
                    self.addItem(item)
                if self.matrix[i][j] == 0:
                    pixmap = QPixmap("images/Cell.png")
                    new_pixmap = pixmap.scaled(pixmap.width() * 2, pixmap.height() * 2)
                    item = QGraphicsPixmapItem(new_pixmap)
                    item.setPos(j * 64, i * 64)
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
            new_x = pos.x() + x * 64
            new_y = pos.y() + y * 64
            self.selected_item.setPos(new_x, new_y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = MyWindow()
    view = QGraphicsView(scene)
    view.show()
    sys.exit(app.exec())
