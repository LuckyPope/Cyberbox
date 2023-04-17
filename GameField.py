from Cell import Cell
from Player import Player


class GameField:
    def __init__(self, board: list[list[Cell]], player: Player):
        self.win = None
        self.player = player
        self.board = board
        self.list_of_cells = board

    def checkMove(self, x, y):
        if (x >= len(self.board[0]) or x < 0 or
                y >= len(self.board) or y < 0 or self.list_of_cells[y][x].getType() == 4):
            return False
        return True

    def move(self, x, y):
        if not self.checkMove(self.player.posX + x, self.player.posY + y):
            return
        step = 1
        length = len(self.board)
        if x < 0 or y < 0:
            step = -1
            length = 0

        # if (self.player.posX + x >= len(self.board[0]) or self.player.posX + x < 0 or
        #         self.player.posY + y >= len(self.board) or self.player.posY + y < 0):
        #     return False

        # if self.list_of_cells[self.player.posY][self.player.posX + x].isMovableX():
        #     print("fdsfsdf")
        #     self.list_of_cells[self.player.posY][self.player.posX + x].setType(0)
        #     for i in range(self.player.posX + 2 * x, length, step):
        #         if self.list_of_cells[self.player.posY][i].isMovableX():
        #             self.list_of_cells[self.player.posY][i].setType(2)
        #             print("13131231")
        #             dp = dp + 1
        #         else:
        #             break

        if self.list_of_cells[self.player.posY + y][self.player.posX].isMovableY() and self.checkMove(self.player.posX, self.player.posY + y):
            if self.checkMove(self.player.posX, self.player.posY + 2 * y):
                print("111")
                self.list_of_cells[self.player.posY + 2 * y][self.player.posX].setType(self.list_of_cells[self.player.posY + y][self.player.posX].getType())
            else:
                return

        if self.list_of_cells[self.player.posY][self.player.posX + x].isMovableX() and self.checkMove(self.player.posX + x, self.player.posY):
            if self.checkMove(self.player.posX + 2 * x, self.player.posY):
                print("222")
                self.list_of_cells[self.player.posY][self.player.posX + 2 * x].setType(self.list_of_cells[self.player.posY][self.player.posX + x].getType())
            else:
                return

        # if (self.list_of_cells[self.player.posY + y][self.player.posX].isMovableY()
        #         and self.checkMove(self.player.posY + y, self.player.posX)):
        #     for i in range(self.player.posY + y, length, step):
        #         if self.list_of_cells[i][self.player.posX].isMovableY() and self.checkMove(i, self.player.posX):
        #             print(i)
        #             self.list_of_cells[i + step][self.player.posX].setType(1)
        #         else:
        #             break

        # if self.list_of_cells[self.player.posY + y][self.player.posX].isMovableY():
        #     print("123")
        #     self.list_of_cells[self.player.posY + y][self.player.posX].setType(0)
        #     for i in range(self.player.posY + 2 * y, length, step):
        #         if self.list_of_cells[i][self.player.posX].isMovableY():
        #             self.list_of_cells[i][self.player.posX].setType(1)
        #             print("abc")
        #         else:
        #             break

        self.player.posX = self.player.posX + x
        self.player.posY = self.player.posY + y
        self.list_of_cells[self.player.posY][self.player.posX].setType(6)
        self.list_of_cells[self.player.posY - y][self.player.posX - x].setType(0)

    # def keyPressEvent(self, event):
    #     print("gfddfg")
    #     if event.key == Qt.Key.Key_Right and self.player.posX + 1 < len(self.level) and \
    #             (self.list_of_cells[self.player.posY][self.player.posX + 1].isMovableX() or
    #              self.list_of_cells[self.player.posY][self.player.posX + 1].getType() == 0):
    #         self.move(1, 0)
    #
    #     if event.key == Qt.Key.Key_Left and self.player.posX - 1 > -1 and \
    #             (self.list_of_cells[self.player.posY][self.player.posX - 1].isMovableX() or
    #              self.list_of_cells[self.player.posY][self.player.posX - 1].getType() == 0):
    #         self.move(-1, 0)
    #
    #     if event.key == Qt.Key.Key_Up and self.player.posY - 1 > - 1 and \
    #             (self.list_of_cells[self.player.posY - 1][self.player.posX].isMovableY() or
    #              self.list_of_cells[self.player.posY - 1][self.player.posX].getType() == 0):
    #         self.move(0, -1)
    #
    #     if event.key == Qt.Key.Key_Down and self.player.posY + 1 < len(self.level[0]) and \
    #             (self.list_of_cells[self.player.posY + 1][self.player.posX].isMovableY() or
    #              self.list_of_cells[self.player.posY + 1][self.player.posX].getType() == 0):
    #         self.move(0, 1)
