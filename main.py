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

    def getType(self):
        return self.type

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
        # self.row = len(self.level)
        # self.col = len(self.level[0])
        self.list_of_cells = []
        # self.list_of_left_right_cells = []
        # self.list_of_up_down_cells = []
        # self.list_of_movable_cells = []
        # self.list_of_unmovable_cells = []

    def initialize_level(self):
        for i, row in enumerate(self.level):
            self.list_of_cells.append([])
            for cellType in row:
                self.list_of_cells[i].append(Cell(cellType))
                # if self.level[i][j] == 0:
                #     self.list_of_cells.append((i, j))
                # if self.level[i][j] == 1:
                #     self.list_of_up_down_cells.append((i, j))
                # if self.level[i][j] == 2:
                #     self.list_of_left_right_cells.append((i, j))
                # if self.level[i][j] == 3:
                #     self.list_of_movable_cells.append((i, j))
                # if self.level[i][j] == 4:
                #     self.list_of_unmovable_cells.append((i, j))
                # if self.level[i][j] == 5:
                #     self.win = (i, j)
                # if self.level[i][j] == 6:
                #     self.player = Player(i, j)

    def move(self, x, y):
        self.player.posX = self.player.posX + x # Переделать перемещение, так как оно сделано только в положительную сторону
        self.player.posY = self.player.posY + y
        if (self.player.posX + x, self.player.posY + y) in self.list_of_left_right_cells \
                and (self.player.posX + 2 * x < len(self.level) or self.player.posY + 2 * y < len(self.player[0])):
            self.list_of_left_right_cells.append((self.player.posX + 2 * x, self.player.posY + y))
            self.list_of_left_right_cells.remove((self.player.posX + x, self.player.posY + y))
        if (self.player.posX + x, self.player.posY + y) in self.list_of_movable_cells \
                and (self.player.posX + 2 * x < len(self.level) or self.player.posY + 2 * y < len(self.player[0])):
            self.list_of_movable_cells.append((self.player.posX + 2 * x, self.player.posY + 2 * y))
            self.list_of_movable_cells.remove((self.player.posX + x, self.player.posY + y))

    def keyPressEvent(self, event):
        if event.key == Qt.Key_Right and self.player.posX + 1 < len(self.level) \
                and (self.player.posX + 1, self.player.posY) not in self.list_of_unmovable_cells \
                and (self.player.posX + 1, self.player.posY) not in self.list_of_up_down_cells:
            self.move(1, 0)
        if event.key == Qt.Key_Left and self.player.posX - 1 > -1 \
                and (self.player.posX - 1, self.player.posY) not in self.list_of_unmovable_cells:
            self.move(-1, 0)
        if event.key == Qt.Key_Up and self.player.posY - 1 > - 1 \
                and (self.player.posX, self.player.posY - 1) not in self.list_of_unmovable_cells:
            self.move(0, -1)
        if event.key == Qt.Key_Down and self.player.posY + 1 < len(self.level[0]) \
                and (self.player.posX, self.player.posY + 1) not in self.list_of_unmovable_cells:
            self.move(0, 1)


class MyWindow(QGraphicsScene):

    def __init__(self):
        super().__init__()
        self.item_list = []
        self.selected_item = None
        # screen_geometry = QApplication.desktop().availableGeometry()
        # window_width = 1200
        # window_height = 1000
        # window_x = (screen_geometry.width() - window_width) // 2
        # window_y = (screen_geometry.height() - window_height) // 2
        # self.setGeometry(window_x, window_y, window_width, window_height)
        self.matrix = read_level('levels/01.txt')
        self.initUI()
        self.game = GameField

        # main_layout = QGridLayout(self)
        #
        # # Создание виджета для игрового поля
        # self.game_board = QWidget(self)
        # main_layout.addWidget(self.game_board, 0, Qt.AlignHCenter)
        #
        # buttons_container = QWidget(self)
        # buttons_layout = QVBoxLayout(buttons_container)
        # buttons_layout.setContentsMargins(0, 10, 0, 0)
        # buttons_layout.setSpacing(10)
        #
        # self.load_button = QPushButton("Load", self)
        # self.load_button.setMaximumSize(150, 70)  # Увеличение размеров кнопки
        # self.load_button.clicked.connect(self.load_matrix)
        # buttons_layout.addWidget(self.load_button)

    def initUI(self):
        # Создаем элементы для графической сцены
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j] == 6:
                    pixmap = QPixmap("images/Player.png")
                    new_pixmap = pixmap.scaled(pixmap.width()*2, pixmap.height()*2)
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
    #
    # def mousePressEvent(self, event):
    #     # Обрабатываем клик мыши для выбора элемента
    #     pos = event.scenePos()
    #     items = self.items(pos)
    #     for item in items:
    #         if isinstance(item, QGraphicsPixmapItem):
    #             self.selected_item = item
    #             break


if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = MyWindow()
    view = QGraphicsView(scene)
    view.show()
    sys.exit(app.exec())
