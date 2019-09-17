import arcade as game
import sys
import time

HEIGHT = 600
WIDTH = 600
count = 0


end = False


class Board:
    def __init__(self, line1, line2, line3):
        self.line1 = line1
        self.line2 = line2
        self.line3 = line3
        # print(self.line1.split("|"))

    def show(self):
        horizLine = "-----"
        print(self.line1)
        print(horizLine)
        print(self.line2)
        print(horizLine)
        print(self.line3)

    def placePiece(self, x, y, player):
        error = False
        if y == 1:
            line = self.line1.split("|")
            if line[x - 1] != " ":
                print("Invalid Location")
                error = True
            if error is False:
                line[x - 1] = player
                self.line1 = line[0] + "|" + line[1] + "|" + line[2]

        elif y == 2:
            line = self.line2.split("|")
            if line[x - 1] != " ":
                print("Invalid Location")
                error = True
            if error is False:
                line[x - 1] = player
                self.line2 = line[0] + "|" + line[1] + "|" + line[2]

        elif y == 3:
            line = self.line3.split("|")
            if line[x - 1] != " ":
                print("Invalid Location")
                error = True
            if error is False:
                line[x - 1] = player
                self.line3 = line[0] + "|" + line[1] + "|" + line[2]
        return error

    def check(self, player):
        global end
        win = False

        lineI = self.line1.split("|")
        lineII = self.line2.split("|")
        lineIII = self.line3.split("|")
        down1 = [lineI[0], lineII[0], lineIII[0]]
        middle = [lineI[1], lineII[1], lineIII[1]]
        down2 = [lineI[2], lineII[2], lineIII[2]]
        diagonalR = [lineI[0], lineII[1], lineIII[2]]
        diagonalL = [lineI[2], lineII[1], lineIII[0]]

        if lineI.count(player) == 3:
            win = True
        elif lineII.count(player) == 3:
            win = True
        elif lineIII.count(player) == 3:
            win = True
        elif down1.count(player) == 3:
            win = True
        elif middle.count(player) == 3:
            win = True
        elif down2.count(player) == 3:
            win = True
        elif diagonalL.count(player) == 3:
            win = True
        elif diagonalR.count(player) == 3:
            win = True
        if win:
            end = True
            print(player.capitalize() + " Wins!")
        return end

end = False
gameBoard = Board(" | | ", " | | ", " | | ")
gameBoard.show()
print("TicTacToe!")
count = 0

class Colors:
    blue = (0, 0, 255)
    red = (255, 0, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)


def drawRect(x, y, width, height, color):
    game.buffered_draw_commands.create_rectangle(x, x + width, y, y - height, color)


class Game(game.Window):
    def __init__(self, width, height, title):
        super(Game, self).__init__(width, height, title)

    def on_mouse_press(self, x, y, button, modifier):
        global count
        print("You clicked button number: {}".format(button))
        if button == game.MOUSE_BUTTON_LEFT:
            if HEIGHT > y > 2 * HEIGHT // 3:
                clickY = 1
                centery = HEIGHT * 0.75 + 40
            elif y > HEIGHT // 3:
                clickY = 2
                centery = HEIGHT // 2
            else:
                clickY = 3
                centery = HEIGHT // 4 - 40

            if WIDTH > x > 2 * WIDTH // 3:
                clickX = 3
                centerx = WIDTH * 0.75 + 40
            elif x > WIDTH // 3:
                clickX = 2
                centerx = WIDTH // 2
            else:
                clickX = 1
                centerx = WIDTH // 4 - 40

        if count % 2 == 1:
            if not gameBoard.placePiece(clickX, clickY, "o"):
                game.draw_circle_filled(centerx, centery, 70, Colors.red)
                game.draw_circle_filled(centerx, centery, 50, Colors.black)
                gameBoard.show()
                count += 1
                if gameBoard.check("o"):
                    sys.exit()
        else:
            if not gameBoard.placePiece(clickX, clickY, "x"):
                game.draw_rectangle_filled(centerx, centery, 20, 80, Colors.blue, tilt_angle=45)
                game.draw_rectangle_filled(centerx, centery, 20, 80, Colors.blue, tilt_angle=-45)
                gameBoard.show()
                count += 1
                if gameBoard.check("x"):
                    sys.exit()



        print("({},{})".format(clickX, clickY))

    def on_draw(self):
        x = 0
        y = 0
        rows = 3
        for i in range(rows):
            game.draw_line(x, 0, x, WIDTH, Colors.white)
            game.draw_line(0, y, HEIGHT, y, Colors.white)
            x += WIDTH // rows
            y += HEIGHT // rows
        if count % 2 == 0:
            drawRect(0, HEIGHT, 30, 30, Colors.blue)
        else:
            drawRect(0, HEIGHT, 30, 30, Colors.red)


def main():
    global rows, x, y
    screen = Game(WIDTH, HEIGHT, "TicTacToe")
    game.set_background_color(Colors.black)

    game.run()


main()
