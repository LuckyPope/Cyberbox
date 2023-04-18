import sys
from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView,QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent

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


class MyScene(QGraphicsScene):

    def __init__(self):
        super().__init__()
        self.board = []
        self.player = Player(0, 0)
        self.matrix = []
        self.button_level1 = QPushButton("level 1")
        self.button_level1.clicked.connect(self.initLevel1)
        self.button_level2 = QPushButton("level 2")
        self.button_level2.clicked.connect(self.initLevel2)
        self.initializeButton()
        self.setSceneRect(0, 0, 960, 700)
        self.initUI()
        self.game = GameField(self.board, self.player)

    def initializeButton(self):
        self.button_level1.move(0, 645)
        self.button_level2.move(0, 670)
        self.addWidget(self.button_level1)
        self.addWidget(self.button_level2)

    def initLevel1(self):
        self.matrix = read_level("levels/01.txt")
        self.board.clear()
        self.initUI()
        self.game = GameField(self.board, self.player)

    def initLevel2(self):
        self.matrix = read_level("levels/02.txt")
        self.board.clear()
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

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Left:
            self.move_item(-1, 0)
            if self.game.win:
                self.win()
        elif event.key() == Qt.Key.Key_Right:
            self.move_item(1, 0)
            if self.game.win:
                self.win()
        elif event.key() == Qt.Key.Key_Up:
            self.move_item(0, -1)
            if self.game.win:
                self.win()
        elif event.key() == Qt.Key.Key_Down:
            self.move_item(0, 1)
            if self.game.win:
                self.win()
        if event.key() == Qt.Key.Key_R:
            self.board.clear()
            self.initUI()
            self.game = GameField(self.board, self.player)

    def move_item(self, x, y):
        self.game.move(x, y)

    @staticmethod
    def win():
        dlg = QMessageBox()
        dlg.setWindowTitle("Победа")
        dlg.setText("Уровень пройден!")
        dlg.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = MyScene()
    view = QGraphicsView(scene)
    view.setMinimumSize(990, 705)
    view.setMaximumSize(990, 705)
    view.show()
    sys.exit(app.exec())
