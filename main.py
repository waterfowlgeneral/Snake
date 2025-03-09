import pygame, sys, random, asyncio
from pygame.math import Vector2

#initialize pygame
pygame.init()
titleFont = pygame.font.Font(None, 60)
scoreFont = pygame.font.Font(None, 40)

# colors
GRAY = (50, 50, 50)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
WHITE = (255, 255, 255)

# individual cells that make up the grid
cellSize = 30
cellNum = 25

offset = 75

class Food:
    def __init__(self, snakeBody):
        self.position = self.randomPos(snakeBody)
    # draw food
    def draw(self):
        foodRect = pygame.Rect(offset + self.position.x * cellSize, offset + self.position.y * cellSize, cellSize, cellSize)
        pygame.draw.rect(screen, RED, foodRect, 0, 13)
    def generateRandomCell(self):
        x = random.randint(0, cellNum - 1)
        y = random.randint(0, cellNum - 1)
        return Vector2(x, y)
    # generate random x and y coordinate
    def randomPos(self, snakeBody):
        position = self.generateRandomCell()
        while position in snakeBody:
            position = self.generateRandomCell()
        return position
    
class Snake:
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1,0)
        self.addSeg = False
    # draw segments of snake
    def draw(self):
        for seg in self.body:
            segRect = (offset + seg.x * cellSize, offset + seg.y * cellSize, cellSize, cellSize)
            pygame.draw.rect(screen, GREEN, segRect, 0, 7)
    # update snake position
    def update(self):
        self.body.insert(0, self.body[0] + self.direction)
        if self.addSeg == True:
            self.addSeg = False
        else:
            self.body = self.body[:-1]
    def reset(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1,0)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "RUNNING"
        self.score = 0
    def draw(self):
        self.food.draw()
        self.snake.draw()
    def update(self):
        if (self.state == "RUNNING"):
            self.snake.update()
            self.checkEat()
            self.checkEdge()
            self.checkTail()
    def checkEat(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.randomPos(self.snake.body)
            self.snake.addSeg = True
            self.score += 1
    def checkEdge(self):
        if self.snake.body[0].x == cellNum or self.snake.body[0].x == -1:
            self.gameOver()
        if self.snake.body[0].y == cellNum or self.snake.body[0].y == -1:
            self.gameOver()
    def checkTail(self):
        bodyNoHead = self.snake.body[1:]
        if self.snake.body[0] in bodyNoHead:
            self.gameOver()
    def gameOver(self):
        self.snake.reset()
        self.food.position = self.food.randomPos(self.snake.body)
        self.state = "STOPPED"
        self.score = 0
    
# 750x750 canvas
screen = pygame.display.set_mode((2 * offset + cellSize * cellNum, 2 * offset + cellSize * cellNum))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock() 

game = Game()
snakeUpdate = pygame.USEREVENT
pygame.time.set_timer(snakeUpdate, 200)

async def main():
    while True:
        for event in pygame.event.get():
            # update snake position
            if event.type == snakeUpdate:
                game.update()
            # exit game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # user control
            if event.type == pygame.KEYDOWN:
                if game.state == "STOPPED":
                    game.state = "RUNNING"
                if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                    game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                    game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                    game.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                    game.snake.direction = Vector2(1, 0)

        # fill screen with gray background
        screen.fill(GRAY)
        pygame.draw.rect(screen, WHITE, 
                        (offset - 5, offset - 5, cellSize * cellNum + 10, cellSize * cellNum + 10), 5)
        game.draw()
        titleSurface = titleFont.render("Snake", True, WHITE)
        scoreSurface = scoreFont.render(str(game.score), True, WHITE)
        screen.blit(titleSurface, (offset - 5, 20))
        screen.blit(scoreSurface, (offset - 5, offset + cellSize * cellNum + 10))
        # update game window
        pygame.display.update()
        # set game to 60 ticks
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())