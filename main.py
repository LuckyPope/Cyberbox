import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QMenu, QFileDialog, QVBoxLayout, QPushButton, \
    QGridLayout, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QKeyEvent

from Cell import Cell
from GameField import GameField
from Player import Player


def read_level(filename):
    f = open(filename, 'r')
    m = []
    for row in f:
        m.append([int(x) for x in row.strip().split(" ")])
    f.close()
    return m


class MyWindow(QGraphicsScene):

    def __init__(self):
        super().__init__()
        self.board = []
        self.selected_item = None
        self.player = Player(0, 0)
        self.matrix = read_level('levels/02.txt')
        self.initUI()
        self.game = GameField(self.board, self.player)

    def initUI(self):
        for i in range(len(self.matrix)):
            self.board.append([])
            for j in range(len(self.matrix[0])):
                item = Cell(self.matrix[i][j])
                if item.type == 6:
                    self.player = Player(i, j)
                item.setPos(j * 64, i * 64)
                self.board[i].append(item)
                self.addItem(item)

        self.setFocus()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Left:
            self.move_item(-1, 0)
        elif event.key() == Qt.Key.Key_Right:
            self.move_item(1, 0)
        elif event.key() == Qt.Key.Key_Up:
            self.move_item(0, -1)
        elif event.key() == Qt.Key.Key_Down:
            self.move_item(0, 1)

    def move_item(self, x, y):
        self.game.move(x, y)
            # pos = self.selected_item.pos()
            # new_x = pos.x() + x * 64
            # new_y = pos.y() + y * 64
            # self.selected_item.setPos(new_x, new_y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = MyWindow()
    view = QGraphicsView(scene)
    view.show()
    sys.exit(app.exec())
