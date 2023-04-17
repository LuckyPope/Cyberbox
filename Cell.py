from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QGraphicsPixmapItem


class Cell(QGraphicsPixmapItem):

    def __init__(self, cellType: int):
        super(Cell, self).__init__()
        self.type = cellType
        self.updateCell()
        self.setScale(2)

    def updateCell(self):
        pixmap = self.getCurrentPixmap()
        self.setPixmap(pixmap)

    def getType(self):
        return self.type

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
