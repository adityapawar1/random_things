import arcade as game
import sys
import time

HEIGHT = 600
WIDTH = 600
movespeed = 5
debug = False
AI = True
doubleAI = True
borderThreshold = 10
threshold = 5


class Colors:
    blue = (0, 0, 255)
    red = (255, 0, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)


def drawRect(x, y, width, height, color):
    game.draw_lrtb_rectangle_filled(x, x + width, y, y - height, color)


def clearScreen():
    pass


class Shape:

    def __init__(self, x, y, width, height, delta_x, delta_y, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # self.angle = angle
        self.delta_x = delta_x
        self.delta_y = delta_y
        # self.delta_angle = delta_angle
        self.color = color

    def move(self):
        self.x += self.delta_x
        self.y += self.delta_y

    def changeDir(self, deltax, deltay):
        self.delta_x = deltax
        self.delta_y = deltay
        # self.angle += self.delta_angle


class Ball(Shape):
    global cover

    def __init__(self, x, y, width, color):
        super(Ball, self).__init__(x, y, width, height=width, delta_x=2, delta_y=2, color=color)
        self.speed = 1.5
        self.speedBuffer = 0

    def addSpeed(self, delta_Time):
        global borderThreshold, threshold
        if not (HEIGHT - ball.y * ball.speed < borderThreshold or ball.y * ball.speed < borderThreshold):
            self.speed += 0.03
            print("Speed Multiplier increased to {}".format(self.speed))
            clearScreen()

    def reset(self):
        self.x, self.y = 300, 300
        self.speed = 1.5
        self.delta_x = -self.delta_x
        clearScreen()
        game.set_background_color(Colors.black)

    def bally(self):
        return self.y

    def draw(self):
        game.draw_circle_filled(self.x * self.speed, self.y * self.speed, self.width + 10 + 5 * self.speed,
                                Colors.black)
        game.draw_circle_filled(self.x * self.speed, self.y * self.speed, self.width, self.color)


class Paddle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.paddleWidth = 10
        self.paddleHeight = 100
        self.score = 0

    def move(self, diry):
        self.y += diry

    def moveTo(self, y):
        self.y = y

    def draw(self):
        drawRect(self.x, HEIGHT, self.paddleWidth, HEIGHT - self.y, Colors.black)
        drawRect(self.x, self.y, self.paddleWidth, self.paddleHeight, self.color)
        drawRect(self.x, self.y - self.paddleHeight, self.paddleWidth, self.y - self.paddleHeight, Colors.black)


player1 = Paddle(50, HEIGHT // 2, Colors.blue)
player2 = Paddle(WIDTH - 50, HEIGHT - 50, Colors.red)
ball = Ball(WIDTH // 2 - 100, HEIGHT // 2 - 100, 10, Colors.white)


def AIon(delta_time):
    if ball.x * ball.speed > player2.x - 200:
        if 105 < ball.y * ball.speed + 50 < 595:
            player2.moveTo(ball.y * ball.speed + 50)
    if doubleAI:
        if ball.x * ball.speed < player1.x + 200:
            if 105 < ball.y * ball.speed + 50 < 595:
                player1.moveTo(ball.y * ball.speed + 50)


class Game(game.Window):
    global player1, movespeed, debug

    def __init__(self, width, height, title):
        super(Game, self).__init__(width, height, title)
        self.up_pressed = False
        self.down_pressed = False
        self.up_pressed2 = False
        self.down_pressed2 = False

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == game.key.Q:
            self.up_pressed = True
        elif key == game.key.A:
            self.down_pressed = True
        if key == game.key.R:
            ball.reset()
        if not AI or debug:
            if key == game.key.P:
                self.up_pressed2 = True
            elif key == game.key.L:
                self.down_pressed2 = True
        if key == game.key.D:
            clearScreen()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == game.key.Q:
            self.up_pressed = False
        elif key == game.key.A:
            self.down_pressed = False
        if key == game.key.P:
            self.up_pressed2 = False
        elif key == game.key.L:
            self.down_pressed2 = False

    def update(self, delta_time):
        global cover, borderThreshold, threshold

        if ball.x > WIDTH:
            ball.reset()
            player1.score += 1
            print("Score is {} - {}".format(player1.score, player2.score))
            if player1.score >= 9:
                print("Player 1 Wins!")
                sys.exit()
        elif ball.x < 0:
            ball.reset()
            player2.score += 1
            print("Score is {} - {}".format(player1.score, player2.score))
            if player2.score >= 9:
                print("Player 2 Wins!")
                sys.exit()

        # Stop players from crashing game and moving player paddles
        if self.down_pressed and player1.y > 105:
            player1.move(-movespeed)

        elif self.up_pressed and player1.y < 595:
            player1.move(movespeed)

        if self.down_pressed2 and player2.y > 105:
            player2.move(-movespeed)

        elif self.up_pressed2 and player2.y < 595:
            player2.move(movespeed)
        # Collision Tracking
        if HEIGHT - ball.y * ball.speed < borderThreshold or ball.y * ball.speed < borderThreshold:
            ball.changeDir(ball.delta_x, -ball.delta_y)
            clearScreen()
            if debug:
                print("Ball hit one of the borders")
        if 0 < ball.x * ball.speed - player2.x + 10 < threshold and 0 < player2.y - ball.y * ball.speed < 100:
            ball.changeDir(-ball.delta_x, ball.delta_y)
            clearScreen()
            if debug:
                print("Ball hit player2")
        if 0 < ball.x * ball.speed - player1.x - 20 < threshold and 0 < player1.y - ball.y * ball.speed < 100:
            ball.changeDir(-ball.delta_x, ball.delta_y)
            clearScreen()
            if debug:
                print("Ball hit player1")
        ball.move()

    def on_draw(self):
        ball.draw()
        player1.draw()
        player2.draw()


def main():
    global rows, x, y
    screen = Game(WIDTH, HEIGHT, "Pong")
    game.set_background_color(Colors.black)
    game.schedule(ball.addSpeed, 3)
    if AI:
        game.schedule(AIon, 1 / 30)
    game.run()


main()
