from Cell import Cell
from Player import Player


class GameField:
    def __init__(self, board: list[list[Cell]], player: Player):
        self.win = None
        self.player = player
        self.board = board
        self.list_of_cells = board
        self.win = False

    def checkMove(self, x, y):
        if (x >= len(self.board[0]) or x < 0 or
                y >= len(self.board) or y < 0 or self.list_of_cells[y][x].getType() == 4):
            return False
        return True

    def checkMoveY(self, dx, dy):
        if self.list_of_cells[dy][dx].isMovableY() and self.checkMove(dx, dy):
            return True
        return False

    def checkMoveX(self, dx, dy):
        if self.list_of_cells[dy][dx].isMovableX() and self.checkMove(dx, dy):
            return True
        return False

    def move(self, x, y):
        if (not self.checkMove(self.player.posX + x, self.player.posY + y)
                or self.list_of_cells[self.player.posY][self.player.posX + x].getType() == 1
                or self.list_of_cells[self.player.posY + y][self.player.posX].getType() == 2
                or self.win):
            return

        step = 1
        length_y = len(self.board)
        length_x = len(self.board[0])
        if x < 0 or y < 0:
            step = -1
            length_y = -1
            length_x = -1
        cells = []

        if self.checkMoveY(self.player.posX + x, self.player.posY + y):
            for i in range(self.player.posY + y, length_y, step):
                if self.checkMoveY(self.player.posX, i):
                    cells.append(i)
                else:
                    break

            for i in range(len(cells) - 1, -1, -1):
                if (self.checkMove(self.player.posX, cells[i] + step)
                        and self.list_of_cells[cells[i] + step][self.player.posX].getType() != 2):
                    self.list_of_cells[cells[i] + step][self.player.posX].setType(self.list_of_cells[cells[i]][self.player.posX].getType())
                else:
                    cells.clear()
                    return

        cells.clear()

        if self.checkMoveX(self.player.posX + x, self.player.posY + y):
            for i in range(self.player.posX + x, length_x, step):
                if self.checkMoveX(i, self.player.posY):
                    cells.append(i)
                else:
                    break

            for i in range(len(cells) - 1, -1, -1):
                if (self.checkMove(cells[i] + step, self.player.posY)
                        and self.list_of_cells[self.player.posY][cells[i] + step].getType() != 1):
                    self.list_of_cells[self.player.posY][cells[i] + step].setType(self.list_of_cells[self.player.posY][cells[i]].getType())
                else:
                    cells.clear()
                    return

            cells.clear()

        self.player.posX = self.player.posX + x
        self.player.posY = self.player.posY + y
        if self.list_of_cells[self.player.posY][self.player.posX].getType() == 5:
            self.win = True
        self.list_of_cells[self.player.posY][self.player.posX].setType(6)
        self.list_of_cells[self.player.posY - y][self.player.posX - x].setType(0)


