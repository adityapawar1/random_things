import pygame
import random

pygame.init()  # initialize pygame

rand = random.random()


class screen:
    height = 700
    width = 700



class snake:
    speed = 7
    velocity = [0, 0]
    x1 = 0
    y1 = 0
    x2 = 10
    y2 = 10

    def move(self):
        self.x1 += velocity[0]
        self.y1 += velocity[1]
        self.x2 += velocity[0]
        self.y2 += velocity[1]
        display.fill((0, 0, 0))
        snakeHead.move_ip(velocity[0], velocity[1])
        pygame.draw.rect(display, red, snakeHead)



class foodClass:
    foodX1 = random.randint(1, screen.width)
    foodY1 = random.randint(1, screen.height)

    def makeFood(self):
        self.x = self.foodX1
        self.y = self.foodY1

        self.foodX1 = random.randint(1, screen.width)
        self.foodY1 = random.randint(1, screen.height)

        self.movex = self.x - self.foodX1
        self.movey = self.y - self.foodY1

        food = pygame.Rect(self.foodX1, self.foodY1, 10, 10)

        food.move_ip(self.movex, self.movey)

        pygame.draw.rect(display, blue, food)

        print("Making Food... x:", food.x, " y:", food.y)
        print(food)


snakeHead = pygame.Rect(snake.x1, snake.y1, snake.x2, snake.y2)

food = pygame.Rect((foodClass.foodX1, foodClass.foodY1), (10, 10))

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

display = pygame.display.set_mode((screen.width, screen.height))  # set the size of display

pygame.display.set_caption("snake")  # sets the title of the window to snake

gameClock = pygame.time.Clock()  # time

rand = random.Random()

#food = pygame.Rect((foodX1, foodY1), (10, 10))
pygame.draw.rect(display, blue, food)

#print(foodX1, "", foodY1)

print(random)

crashed = False
print(snakeHead)
while not crashed:
    snake.move()

    if food.colliderect(pygame.Rect(snakeHead)):
        makeFood()

        print("The snake got the food")
    for event in pygame.event.get():  # creates an array of events and loops through
        if event.type == pygame.QUIT:  # checks if user quits
            crashed = True  # exits loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                velocity = [speed * -1, 0]
            elif event.key == pygame.K_RIGHT:
                velocity = [speed, 0]
            elif event.key == pygame.K_UP:
                velocity = [0, speed * -1]
            elif event.key == pygame.K_DOWN:
                velocity = [0, speed]

    pygame.display.update()  # update the screen
    gameClock.tick(20)  # FPS

pygame.quit()
quit
