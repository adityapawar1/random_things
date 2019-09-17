import arcade as game


# Define Constants
PIECE_SCALE = 0.48
OFFSET = 39
HEIGHT = 600
WIDTH = 600
rows = 8
count = 0
draw = ""
turn = "white"
mode = "piece"
win = ""
locations = []
pieces = []
debug = True
c = 0


# Colors
class Colors:
    black = (0, 0, 0)
    gray = (130, 130, 130)
    white = (250, 250, 250, 50)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

    colors = [gray, white, red, green, blue]


""" PIECE CLASSES """


class Piece:
    def __init__(self, x, y, color):
        self.color = color
        self.x = x
        self.y = y
        pieces.append(self)
        self.index = len(locations)
        locations.append((self.x, self.y))

    def show(self):
        pass

    def possibleLocations(self):
        pass

    def move(self, x, y):
        global turn, mode
        move = False
        for l in self.possible:
            if l == (x * (WIDTH // rows) - OFFSET, y * (WIDTH // rows) - OFFSET):
                move = True

        if move:
            try:
                pieces[locations.index((x, y))].death = True
            except:
                pass
            self.piece.center_x = x * (WIDTH // rows) - OFFSET
            self.piece.center_y = y * (WIDTH // rows) - OFFSET
            self.x = x
            self.y = y
            locations.pop(index)
            locations.insert(index, (self.x, self.y))
            turn = "white" if turn == "black" else "black"
            print("It is {}'s turn\n\n\n".format(turn))
            if mode == "mov":
                mode = "move"
            else:
                mode = "piece"
        else:
            if mode == "mov":
                mode = "piece"


class Pawn(Piece):
    def __init__(self, x, y, color):
        super(Pawn, self).__init__(x, y, color)
        self.death = False
        self.sprite = "images/{}/pawn{}.png".format(color, color)
        self.piece = game.Sprite(self.sprite, PIECE_SCALE)
        self.piece.center_x = self.x * (WIDTH // rows) - OFFSET
        self.piece.center_y = self.y * (WIDTH // rows) - OFFSET

    def possibleLocations(self):
        global draw
        self.possible = []
        if self.color == "white":
            offset = 1
            offset2 = 2
        else:
            offset = -1
            offset2 = -2

        try:
            if pieces[locations.index((self.x, self.y + offset))].death:
                draw += "game.draw_circle_filled({}, {}, {}, {})\n".format(self.x * (WIDTH // rows) - OFFSET, (self.y + offset) * (WIDTH // rows) - OFFSET, 10, Colors.green)
                self.possible.append((self.x * (WIDTH // rows) - OFFSET, (self.y + offset) * (WIDTH // rows) - OFFSET))
        except:
            draw += "game.draw_circle_filled({}, {}, {}, {})\n".format(self.x * (WIDTH // rows) - OFFSET, (self.y + offset) * (WIDTH // rows) - OFFSET, 10, Colors.green)
            self.possible.append((self.x * (WIDTH // rows) - OFFSET, (self.y + offset) * (WIDTH // rows) - OFFSET))

        if (self.color == "white" and self.y == 2) or (self.color == "black" and self.y == 7):
            draw += "game.draw_circle_filled({}, {}, {}, {})\n".format(self.x * (WIDTH // rows) - OFFSET, (self.y + offset2) * (WIDTH // rows) - OFFSET, 10, Colors.green)
            self.possible.append((self.x * (WIDTH // rows) - OFFSET, (self.y + offset2) * (WIDTH // rows) - OFFSET))

        try:
            if pieces[locations.index((self.x + offset, self.y + offset))].color != self.color and not pieces[locations.index((self.x + offset, self.y + offset))].death:
                draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x + offset) * (WIDTH // rows) - OFFSET, (self.y + offset) * (WIDTH // rows) - OFFSET, 10, Colors.green)
                self.possible.append(((self.x + offset) * (WIDTH // rows) - OFFSET, (self.y + offset) * (WIDTH // rows) - OFFSET))
        except:
            pass

        try:
            if pieces[locations.index((self.x - offset, self.y + offset))].color != self.color and not pieces[locations.index((self.x - offset, self.y + offset))].death:
                draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x - offset) * (WIDTH // rows) - OFFSET, (self.y + offset) * (WIDTH // rows) - OFFSET, 10, Colors.green)
                self.possible.append(((self.x - offset) * (WIDTH // rows) - OFFSET, (self.y + offset) * (WIDTH // rows) - OFFSET))
        except:
            pass

    def show(self):
        if not self.death:
            self.piece.draw()


class Rook(Piece):
    def __init__(self, x, y, color):
        super(Rook, self).__init__(x, y, color)
        self.death = False
        self.sprite = "images/{}/rook{}.png".format(color, color)
        self.piece = game.Sprite(self.sprite, PIECE_SCALE)
        self.piece.center_x = self.x * (WIDTH // rows) - OFFSET
        self.piece.center_y = self.y * (WIDTH // rows) - OFFSET

    def show(self):
        if not self.death:
            self.piece.draw()

    def possibleLocations(self):
        global draw
        self.possible = []

        xArray = [1, 2, 3, 4, 5, 6, 7, 8]
        yArray = [1, 2, 3, 4, 5, 6, 7, 8]

        topB = True
        bottomB = True
        rightB = True
        leftB = True

        left = xArray[:xArray.index(self.x)]
        right = xArray[xArray.index(self.x) + 1:]
        left.reverse()
        xArray.pop(xArray.index(self.x))

        bottom = yArray[:yArray.index(self.y)]
        bottom.reverse()
        top = yArray[yArray.index(self.y) + 1:]
        yArray.pop(yArray.index(self.y))

        for i in range(7):
            try:
                if (pieces[locations.index((right[i], self.y))].color != self.color and rightB):
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format(right[i] * (WIDTH // rows) - OFFSET, self.y * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append((right[i] * (WIDTH // rows) - OFFSET, self.y * (WIDTH // rows) - OFFSET))
                if not pieces[locations.index((right[i], self.y))].death:
                    rightB = False
            except:
                pass
            try:
                if rightB:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format(right[i] * (WIDTH // rows) - OFFSET, self.y * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append((right[i] * (WIDTH // rows) - OFFSET, self.y * (WIDTH // rows) - OFFSET))
            except:
                pass

            try:
                if pieces[locations.index((left[i], self.y))].color != self.color and leftB:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format(left[i] * (WIDTH // rows) - OFFSET, self.y * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append((left[i] * (WIDTH // rows) - OFFSET, self.y * (WIDTH // rows) - OFFSET))
                if not pieces[locations.index((left[i], self.y))].death:
                    leftB = False
            except:
                pass
            try:
                if leftB:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format(left[i] * (WIDTH // rows) - OFFSET, self.y * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append((left[i] * (WIDTH // rows) - OFFSET, self.y * (WIDTH // rows) - OFFSET))
            except:
                pass

            try:
                if pieces[locations.index((self.x, top[i]))].color != self.color and topB:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format(self.x * (WIDTH // rows) - OFFSET, top[i] * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append((self.x * (WIDTH // rows) - OFFSET, top[i] * (WIDTH // rows) - OFFSET))
                if not pieces[locations.index((self.x, top[i]))].death:
                    topB = False
            except:
                pass
            try:
                if topB:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format(self.x * (WIDTH // rows) - OFFSET, top[i] * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append((self.x * (WIDTH // rows) - OFFSET, top[i] * (WIDTH // rows) - OFFSET))
            except:
                pass

            try:
                if pieces[locations.index((self.x, bottom[i]))].color != self.color and bottomB:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format(self.x * (WIDTH // rows) - OFFSET, bottom[i] * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append((self.x * (WIDTH // rows) - OFFSET, bottom[i] * (WIDTH // rows) - OFFSET))
                if not pieces[locations.index((self.x, bottom[i]))].death:
                    bottomB = False
            except:
                pass
            try:
                if bottomB:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format(self.x * (WIDTH // rows) - OFFSET, bottom[i] * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append((self.x * (WIDTH // rows) - OFFSET, bottom[i] * (WIDTH // rows) - OFFSET))
            except:
                pass


class Knight(Piece):
    def __init__(self, x, y, color):
        super(Knight, self).__init__(x, y, color)
        self.death = False
        self.sprite = "images/{}/knight{}.png".format(color, color)
        self.piece = game.Sprite(self.sprite, PIECE_SCALE)
        self.piece.center_x = self.x * (WIDTH // rows) - OFFSET
        self.piece.center_y = self.y * (WIDTH // rows) - OFFSET

    def show(self):
        if not self.death:
            self.piece.draw()

    def possibleLocations(self):
        global draw
        self.possible = []

        pos1pos2 = True
        pos1neg2 = True
        pos2neg1 = True
        pos2pos1 = True
        neg1pos2 = True
        neg2neg1 = True
        neg2pos1 = True
        neg1neg2 = True


        try:
            if pieces[locations.index((self.x + 1, self.y + 2))].color == self.color:
                pos1pos2 = False
        except:
            pass
        if pos1pos2:
            draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x + 1) * (WIDTH // rows) - OFFSET, (self.y + 2) * (WIDTH // rows) - OFFSET, 10, Colors.green)
            self.possible.append(((self.x + 1) * (WIDTH // rows) - OFFSET, (self.y + 2) * (WIDTH // rows) - OFFSET))

        try:
            if pieces[locations.index((self.x + 2, self.y + 1))].color == self.color:
                pos2pos1 = False
        except:
            pass
        if pos2pos1:
            draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x + 2) * (WIDTH // rows) - OFFSET, (self.y + 1) * (WIDTH // rows) - OFFSET, 10, Colors.green)
            self.possible.append(((self.x + 2) * (WIDTH // rows) - OFFSET, (self.y + 1) * (WIDTH // rows) - OFFSET))

        try:
            if pieces[locations.index((self.x - 1, self.y - 2))].color == self.color:
                neg1neg2 = False
        except:
            pass
        if neg1neg2:
            draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x - 1) * (WIDTH // rows) - OFFSET, (self.y - 2) * (WIDTH // rows) - OFFSET, 10, Colors.green)
            self.possible.append(((self.x - 1) * (WIDTH // rows) - OFFSET, (self.y - 2) * (WIDTH // rows) - OFFSET))

        try:
            if pieces[locations.index((self.x + 2, self.y - 1))].color == self.color:
                pos2neg1 = False
        except:
            pass
        if pos2neg1:
            draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x + 2) * (WIDTH // rows) - OFFSET, (self.y - 1) * (WIDTH // rows) - OFFSET, 10, Colors.green)
            self.possible.append(((self.x + 2) * (WIDTH // rows) - OFFSET, (self.y - 1) * (WIDTH // rows) - OFFSET))

        try:
            if pieces[locations.index((self.x + 1, self.y - 2))].color == self.color:
                pos1neg2 = False
        except:
            pass
        if pos1neg2:
            draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x + 1) * (WIDTH // rows) - OFFSET, (self.y - 2) * (WIDTH // rows) - OFFSET, 10, Colors.green)
            self.possible.append(((self.x + 1) * (WIDTH // rows) - OFFSET, (self.y - 2) * (WIDTH // rows) - OFFSET))

        try:
            if pieces[locations.index((self.x - 2, self.y - 1))].color == self.color:
                neg2neg1 = False
        except:
            pass
        if neg2neg1:
            draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x - 2) * (WIDTH // rows) - OFFSET, (self.y - 1) * (WIDTH // rows) - OFFSET, 10, Colors.green)
            self.possible.append(((self.x - 2) * (WIDTH // rows) - OFFSET, (self.y - 1) * (WIDTH // rows) - OFFSET))

        try:
            if pieces[locations.index((self.x - 1, self.y + 2))].color == self.color:
                neg1pos2 = False
        except:
            pass
        if neg1pos2:
            draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x - 1) * (WIDTH // rows) - OFFSET, (self.y + 2) * (WIDTH // rows) - OFFSET, 10, Colors.green)
            self.possible.append(((self.x - 1) * (WIDTH // rows) - OFFSET, (self.y + 2) * (WIDTH // rows) - OFFSET))

        try:
            if pieces[locations.index((self.x - 2, self.y + 1))].color == self.color:
                neg2pos1 = False
        except:
            pass
        if neg2pos1:
            draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x - 2) * (WIDTH // rows) - OFFSET, (self.y + 1) * (WIDTH // rows) - OFFSET, 10, Colors.green)
            self.possible.append(((self.x - 2) * (WIDTH // rows) - OFFSET, (self.y + 1) * (WIDTH // rows) - OFFSET))


class Bishop(Piece):
    def __init__(self, x, y, color):
        super(Bishop, self).__init__(x, y, color)
        self.death = False
        self.sprite = "images/{}/bishop{}.png".format(color, color)
        self.piece = game.Sprite(self.sprite, PIECE_SCALE)
        self.piece.center_x = self.x * (WIDTH // rows) - OFFSET
        self.piece.center_y = self.y * (WIDTH // rows) - OFFSET

    def show(self):
        if not self.death:
            self.piece.draw()

    def possibleLocations(self):
        global draw
        self.possible = []

        pospos = True
        negpos = True
        posneg = True
        negneg = True

        for i in range(1, 8):
            try:
                if pieces[locations.index((self.x + i, self.y + i))].color != self.color and pospos:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x + i) * (WIDTH // rows) - OFFSET, (self.y + i) * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append(((self.x + i) * (WIDTH // rows) - OFFSET, (self.y + i) * (WIDTH // rows) - OFFSET))
                if not pieces[locations.index((self.x + i, self.y + i))].death:
                    pospos = False
            except:
                if pospos:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x + i) * (WIDTH // rows) - OFFSET, (self.y + i) * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append(((self.x + i) * (WIDTH // rows) - OFFSET, (self.y + i) * (WIDTH // rows) - OFFSET))

            try:
                if pieces[locations.index((self.x - i, self.y + i))].color != self.color and negpos:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x - i) * (WIDTH // rows) - OFFSET, (self.y + i) * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append(((self.x - i) * (WIDTH // rows) - OFFSET, (self.y + i) * (WIDTH // rows) - OFFSET))
                if not pieces[locations.index((self.x - i, self.y + i))].death:
                    negpos = False
            except:
                if negpos:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x - i) * (WIDTH // rows) - OFFSET, (self.y + i) * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append(((self.x - i) * (WIDTH // rows) - OFFSET, (self.y + i) * (WIDTH // rows) - OFFSET))

            try:
                if pieces[locations.index((self.x + i, self.y - i))].color != self.color and posneg:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x + i) * (WIDTH // rows) - OFFSET, (self.y - i) * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append(((self.x + i) * (WIDTH // rows) - OFFSET, (self.y - i) * (WIDTH // rows) - OFFSET))
                if not pieces[locations.index((self.x + i, self.y - i))].death:
                    posneg = False
            except:
                if posneg:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x + i) * (WIDTH // rows) - OFFSET, (self.y - i) * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append(((self.x + i) * (WIDTH // rows) - OFFSET, (self.y - i) * (WIDTH // rows) - OFFSET))
            try:
                if pieces[locations.index((self.x - i, self.y - i))].color != self.color and negneg:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x - i) * (WIDTH // rows) - OFFSET, (self.y - i) * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append(((self.x - i) * (WIDTH // rows) - OFFSET, (self.y - i) * (WIDTH // rows) - OFFSET))
                if not pieces[locations.index((self.x - i, self.y - i))].death:
                    negneg = False
            except:
                if negneg:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x - i) * (WIDTH // rows) - OFFSET, (self.y - i) * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append(((self.x - i) * (WIDTH // rows) - OFFSET, (self.y - i) * (WIDTH // rows) - OFFSET))


class Queen(Piece):
    def __init__(self, x, y, color):
        super(Queen, self).__init__(x, y, color)
        self.death = False
        self.sprite = "images/{}/queen{}.png".format(color, color)
        self.piece = game.Sprite(self.sprite, PIECE_SCALE)
        self.piece.center_x = self.x * (WIDTH // rows) - OFFSET
        self.piece.center_y = self.y * (WIDTH // rows) - OFFSET

    def show(self):
        if not self.death:
            self.piece.draw()

    def possibleLocations(self):
        global draw
        """ROOK MOVEMENT"""
        self.possible = []

        xArray = [1, 2, 3, 4, 5, 6, 7, 8]
        yArray = [1, 2, 3, 4, 5, 6, 7, 8]

        topB = True
        bottomB = True
        rightB = True
        leftB = True

        left = xArray[:xArray.index(self.x)]
        right = xArray[xArray.index(self.x) + 1:]
        left.reverse()
        xArray.pop(xArray.index(self.x))

        bottom = yArray[:yArray.index(self.y)]
        bottom.reverse()
        top = yArray[yArray.index(self.y) + 1:]
        yArray.pop(yArray.index(self.y))

        for i in range(7):
            try:
                if (pieces[locations.index((right[i], self.y))].color != self.color and rightB):
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format(right[i] * (WIDTH // rows) - OFFSET, self.y * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append((right[i] * (WIDTH // rows) - OFFSET, self.y * (WIDTH // rows) - OFFSET))
                if not pieces[locations.index((right[i], self.y))].death:
                    rightB = False
            except:
                pass
            try:
                if rightB:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format(right[i] * (WIDTH // rows) - OFFSET, self.y * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append((right[i] * (WIDTH // rows) - OFFSET, self.y * (WIDTH // rows) - OFFSET))
            except:
                pass

            try:
                if pieces[locations.index((left[i], self.y))].color != self.color and leftB:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format(left[i] * (WIDTH // rows) - OFFSET, self.y * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append((left[i] * (WIDTH // rows) - OFFSET, self.y * (WIDTH // rows) - OFFSET))
                if not pieces[locations.index((left[i], self.y))].death:
                    leftB = False
            except:
                pass
            try:
                if leftB:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format(left[i] * (WIDTH // rows) - OFFSET, self.y * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append((left[i] * (WIDTH // rows) - OFFSET, self.y * (WIDTH // rows) - OFFSET))
            except:
                pass

            try:
                if pieces[locations.index((self.x, top[i]))].color != self.color and topB:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format(self.x * (WIDTH // rows) - OFFSET, top[i] * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append((self.x * (WIDTH // rows) - OFFSET, top[i] * (WIDTH // rows) - OFFSET))
                if not pieces[locations.index((self.x, top[i]))].death:
                    topB = False
            except:
                pass
            try:
                if topB:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format(self.x * (WIDTH // rows) - OFFSET, top[i] * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append((self.x * (WIDTH // rows) - OFFSET, top[i] * (WIDTH // rows) - OFFSET))
            except:
                pass

            try:
                if pieces[locations.index((self.x, bottom[i]))].color != self.color and bottomB:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format(self.x * (WIDTH // rows) - OFFSET, bottom[i] * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append((self.x * (WIDTH // rows) - OFFSET, bottom[i] * (WIDTH // rows) - OFFSET))
                if not pieces[locations.index((self.x, bottom[i]))].death:
                    bottomB = False
            except:
                pass
            try:
                if bottomB:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format(self.x * (WIDTH // rows) - OFFSET, bottom[i] * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append((self.x * (WIDTH // rows) - OFFSET, bottom[i] * (WIDTH // rows) - OFFSET))
            except:
                pass

        """BISHOP MOVEMENT"""
        pospos = True
        negpos = True
        posneg = True
        negneg = True

        for i in range(1, 8):
            try:
                if pieces[locations.index((self.x + i, self.y + i))].color != self.color and pospos:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x + i) * (WIDTH // rows) - OFFSET, (self.y + i) * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append(((self.x + i) * (WIDTH // rows) - OFFSET, (self.y + i) * (WIDTH // rows) - OFFSET))
                if not pieces[locations.index((self.x + i, self.y + i))].death:
                    pospos = False
            except:
                if pospos:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x + i) * (WIDTH // rows) - OFFSET, (self.y + i) * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append(((self.x + i) * (WIDTH // rows) - OFFSET, (self.y + i) * (WIDTH // rows) - OFFSET))

            try:
                if pieces[locations.index((self.x - i, self.y + i))].color != self.color and negpos:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x - i) * (WIDTH // rows) - OFFSET, (self.y + i) * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append(((self.x - i) * (WIDTH // rows) - OFFSET, (self.y + i) * (WIDTH // rows) - OFFSET))
                if not pieces[locations.index((self.x - i, self.y + i))].death:
                    negpos = False
            except:
                if negpos:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x - i) * (WIDTH // rows) - OFFSET, (self.y + i) * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append(((self.x - i) * (WIDTH // rows) - OFFSET, (self.y + i) * (WIDTH // rows) - OFFSET))

            try:
                if pieces[locations.index((self.x + i, self.y - i))].color != self.color and posneg:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x + i) * (WIDTH // rows) - OFFSET, (self.y - i) * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append(((self.x + i) * (WIDTH // rows) - OFFSET, (self.y - i) * (WIDTH // rows) - OFFSET))
                if not pieces[locations.index((self.x + i, self.y - i))].death:
                    posneg = False
            except:
                if posneg:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x + i) * (WIDTH // rows) - OFFSET, (self.y - i) * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append(((self.x + i) * (WIDTH // rows) - OFFSET, (self.y - i) * (WIDTH // rows) - OFFSET))
            try:
                if pieces[locations.index((self.x - i, self.y - i))].color != self.color and negneg:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x - i) * (WIDTH // rows) - OFFSET, (self.y - i) * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append(((self.x - i) * (WIDTH // rows) - OFFSET, (self.y - i) * (WIDTH // rows) - OFFSET))
                if not pieces[locations.index((self.x - i, self.y - i))].death:
                    negneg = False
            except:
                if negneg:
                    draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x - i) * (WIDTH // rows) - OFFSET, (self.y - i) * (WIDTH // rows) - OFFSET, 10, Colors.green)
                    self.possible.append(((self.x - i) * (WIDTH // rows) - OFFSET, (self.y - i) * (WIDTH // rows) - OFFSET))


class King(Piece):
    def __init__(self, x, y, color):
        super(King, self).__init__(x, y, color)
        self.death = False
        self.sprite = "images/{}/king{}.png".format(color, color)
        self.piece = game.Sprite(self.sprite, PIECE_SCALE)
        self.piece.center_x = self.x * (WIDTH // rows) - OFFSET
        self.piece.center_y = self.y * (WIDTH // rows) - OFFSET

    def show(self):
        if not self.death:
            self.piece.draw()

    def possibleLocations(self):
        global draw
        self.possible = []

        draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x + 1) * (WIDTH // rows) - OFFSET, self.y * (WIDTH // rows) - OFFSET, 10, Colors.green)
        self.possible.append(((self.x + 1) * (WIDTH // rows) - OFFSET, self.y * (WIDTH // rows) - OFFSET))
        draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x + 1) * (WIDTH // rows) - OFFSET, (self.y + 1) * (WIDTH // rows) - OFFSET, 10, Colors.green)
        self.possible.append(((self.x + 1) * (WIDTH // rows) - OFFSET, (self.y + 1) * (WIDTH // rows) - OFFSET))
        draw += "game.draw_circle_filled({}, {}, {}, {})\n".format(self.x * (WIDTH // rows) - OFFSET, (self.y + 1) * (WIDTH // rows) - OFFSET, 10, Colors.green)
        self.possible.append((self.x * (WIDTH // rows) - OFFSET, (self.y + 1) * (WIDTH // rows) - OFFSET))
        draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x - 1) * (WIDTH // rows) - OFFSET, self.y * (WIDTH // rows) - OFFSET, 10, Colors.green)
        self.possible.append(((self.x - 1) * (WIDTH // rows) - OFFSET, self.y * (WIDTH // rows) - OFFSET))
        draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x - 1) * (WIDTH // rows) - OFFSET, (self.y - 1) * (WIDTH // rows) - OFFSET, 10, Colors.green)
        self.possible.append(((self.x - 1) * (WIDTH // rows) - OFFSET, (self.y - 1) * (WIDTH // rows) - OFFSET))
        draw += "game.draw_circle_filled({}, {}, {}, {})\n".format(self.x * (WIDTH // rows) - OFFSET, (self.y - 1) * (WIDTH // rows) - OFFSET, 10, Colors.green)
        self.possible.append((self.x * (WIDTH // rows) - OFFSET, (self.y - 1) * (WIDTH // rows) - OFFSET))
        draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x - 1) * (WIDTH // rows) - OFFSET, (self.y + 1) * (WIDTH // rows) - OFFSET, 10, Colors.green)
        self.possible.append(((self.x - 1) * (WIDTH // rows) - OFFSET, (self.y + 1) * (WIDTH // rows) - OFFSET))
        draw += "game.draw_circle_filled({}, {}, {}, {})\n".format((self.x + 1) * (WIDTH // rows) - OFFSET, (self.y - 1) * (WIDTH // rows) - OFFSET, 10, Colors.green)
        self.possible.append(((self.x + 1) * (WIDTH // rows) - OFFSET, (self.y - 1) * (WIDTH // rows) - OFFSET))


""" PIECE DEFINITIONS """


# White Pieces


wpawn1 = Pawn(1, 2, "white")
wpawn2 = Pawn(2, 2, "white")
wpawn3 = Pawn(3, 2, "white")
wpawn4 = Pawn(4, 2, "white")
wpawn5 = Pawn(5, 2, "white")
wpawn6 = Pawn(6, 2, "white")
wpawn7 = Pawn(7, 2, "white")
wpawn8 = Pawn(8, 2, "white")

wrook1 = Rook(1, 1, "white")
wrook2 = Rook(8, 1, "white")

wknight1 = Knight(2, 1, "white")
wknight2 = Knight(7, 1, "white")

wbishop1 = Bishop(3, 1, "white")
wbishop2 = Bishop(6, 1, "white")

wqueen = Queen(4, 1, "white")
wking = King(5, 1, "white")

# Black Pieces

bpawn1 = Pawn(1, 7, "black")
bpawn2 = Pawn(2, 7, "black")
bpawn3 = Pawn(3, 7, "black")
bpawn4 = Pawn(4, 7, "black")
bpawn5 = Pawn(5, 7, "black")
bpawn6 = Pawn(6, 7, "black")
bpawn7 = Pawn(7, 7, "black")
bpawn8 = Pawn(8, 7, "black")

brook1 = Rook(1, 8, "black")
brook2 = Rook(8, 8, "black")

bknight1 = Knight(2, 8, "black")
bknight2 = Knight(7, 8, "black")

bbishop1 = Bishop(3, 8, "black")
bbishop2 = Bishop(6, 8, "black")

bqueen = Queen(5, 8, "black")
bking = King(4, 8, "black")


# Draws all pieces
def showAll():

    # White

    wpawn1.show()
    wpawn2.show()
    wpawn3.show()
    wpawn4.show()
    wpawn5.show()
    wpawn6.show()
    wpawn7.show()
    wpawn8.show()

    wrook1.show()
    wrook2.show()

    wknight1.show()
    wknight2.show()

    wbishop1.show()
    wbishop2.show()

    wqueen.show()
    wking.show()

    # Black

    bpawn1.show()
    bpawn2.show()
    bpawn3.show()
    bpawn4.show()
    bpawn5.show()
    bpawn6.show()
    bpawn7.show()
    bpawn8.show()

    brook1.show()
    brook2.show()

    bknight1.show()
    bknight2.show()

    bbishop1.show()
    bbishop2.show()

    bqueen.show()
    bking.show()


class Game(game.Window):

    def __init__(self, width, height, title):
        super(Game, self).__init__(width, height, title)

        # Sprite lists
        self.board = game.SpriteList()
        self.piece_list = game.SpriteList()
        self.coin_list = game.SpriteList()

        # Score
        self.score = 0

        # Set up the player
        self.board = game.Sprite("board.png", 0.25)
        self.board.center_x = WIDTH // 2
        self.board.center_y = HEIGHT // 2
        self.piece_list.center_x = 50
        self.piece_list.center_y = 50

    def setup(self):
        pass

    def on_mouse_press(self, x, y, button, modifier):
        global draw, mode, index, turn, win, c
        if c == 0:
            print("It is {}'s turn".format(turn))

        if win != "White" and win != "Black":
            if button == game.MOUSE_BUTTON_LEFT:
                draw = ""
                gamex = x // (WIDTH // rows) + 1
                gamey = y // (HEIGHT // rows) + 1
                # print("You clicked at ({}, {})".format(gamex, gamey))

                if mode == "piece":
                    for c, l in enumerate(locations):
                        if l[0] == gamex and l[1] == gamey and not pieces[c].death and pieces[c].color == turn:
                            index = c
                            pieces[c].possibleLocations()
                            mode = "move"
                            break

                elif mode == "move":
                    for c, l in enumerate(locations):
                        if l[0] == gamex and l[1] == gamey and pieces[c].color == pieces[index].color and not pieces[c].death:
                            index = c
                            pieces[c].possibleLocations()
                            mode = "mov"
                            break
                    pieces[index].move(gamex, gamey)

                if bking.death:
                    win = "White"
                elif wking.death:
                    win = "Black"
        else:
            print("{} wins!".format(win))
    c += 1


    def on_key_press(self, key, modifiers):
        pass

    def update(self, delta_time):
        pass

    # Execute all drawing commands
    def on_draw(self):
        self.board.draw()
        showAll()
        exec(draw)


window = Game(HEIGHT, WIDTH, "Chess")
game.run()

