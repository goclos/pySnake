import pygame
import sys
from random import randint


class Snake:
    def __init__(self, dir, headRect, rectSize, windowSizex, windowSizey):
        self.headRect = headRect
        self.body = [self.headRect]
        self.directionHistory = [dir]
        self.rectSize = rectSize
        self.windowSizex = windowSizex
        self.windowSizey = windowSizey
        self.lastDirection = 0
        self.snakeKilled = False

    def overlapedWithSnake(self, object):
        for segment in self.body:
            if object == segment:
                return True
        return False

    def addDirection(self, newDirection):
        if self.directionHistory[0] == "w" and newDirection == "s":
            self.directionHistory.insert(0,"w")
            return
        if self.directionHistory[0] == "s" and newDirection == "w":
            self.directionHistory.insert(0,"s")
            return
        if self.directionHistory[0] == "a" and newDirection == "d":
            self.directionHistory.insert(0,"a")
            return
        if self.directionHistory[0] == "d" and newDirection == "a":
            self.directionHistory.insert(0,"d")
            return
        #defaoult:
        self.directionHistory.insert(0,newDirection)

    def moveSnakeBody(self, newDirection):
        self.addDirection(newDirection)
        while True:
            if len(self.directionHistory) > len(self.body):
                self.directionHistory.pop()
            else:
                break
        for i in range(0, len(self.body)):
            if self.directionHistory[i] == "w":
                self.body[i].move_ip(self.moveUp())
            if self.directionHistory[i] == "s":
                self.body[i].move_ip(self.moveDown())
            if self.directionHistory[i] == "a":
                self.body[i].move_ip(self.moveLeft())
            if self.directionHistory[i] == "d":
                self.body[i].move_ip(self.moveRight())
            self.teleport(self.body[i])
        self.checkBodyCollide()
        if self.snakeKilled:
            return "Killed"
        return "ok"

    def checkBodyCollide(self):
        for i in range(1, len(self.body)):
            if self.body[0] == self.body[i]:
                self.snakeKilled = True
                #print("collide with body")

    def teleport(self, currentRect):
        if currentRect.centerx >= self.windowSizex:
            currentRect.move_ip(-self.windowSizex, 0)
        if currentRect.centerx <= 0:
            currentRect.move_ip(self.windowSizex, 0)
        if currentRect.centery >= self.windowSizey:
            currentRect.move_ip(0, -self.windowSizey)
        if currentRect.centery <= 0:
            currentRect.move_ip(0, self.windowSizey)

    def moveUp(self):
        return 0, -self.rectSize
    def moveDown(self):
        return 0, self.rectSize
    def moveLeft(self):
        return -self.rectSize, 0
    def moveRight(self):
        return self.rectSize, 0

    def drawSnake(self, screen, image):
        if self.snakeKilled:
            image.fill((255, 0, 0)) #red
        for element in self.body:
            screen.blit(image, element)

    def checkCollideFood(self, food):
        if food == self.body[0]:
            self.addSegment()
            return True

    def addSegment(self):
        self.body.append(self.body[-1].copy())
        if self.directionHistory[-1] == "w":
            self.body[-1].move_ip(self.moveDown())
        if self.directionHistory[-1] == "s":
            self.body[-1].move_ip(self.moveUp())
        if self.directionHistory[-1] == "a":
            self.body[-1].move_ip(self.moveRight())
        if self.directionHistory[-1] == "d":
            self.body[-1].move_ip(self.moveLeft())

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def paused(display_width, display_height, gameDisplay):
    largeText = pygame.font.SysFont("consolas",128)
    TextSurf, TextRect = text_objects("Paused", largeText, (51,255,0))
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #print("escape")
                    return
        pygame.display.update()
        clock.tick(15)

def died(display_width, display_height, gameDisplay, score):
    largeText = pygame.font.SysFont("consolas",80)
    smalltext = pygame.font.SysFont("consolas",30)

    diedTextSurf, diedTextRect = text_objects("You died", largeText, (255,36,0))
    diedTextRect.center = ((display_width/2),(display_height/2)-70)

    scoreTextSurf, scoreTextRect = text_objects("Your SCORE: "+ str(score), smalltext, (51,255,0))
    scoreTextRect.center = ((display_width/2),(display_height/2))

    escTextSurf, escTextRect = text_objects("Press 'ESC' to quit", smalltext, (51,255,0))
    escTextRect.center = ((display_width/2),(display_height/2)+40)

    contTextSurf, contTextRect = text_objects("Press 'ENTER' to start again", smalltext, (51,255,0))
    contTextRect.center = ((display_width/2),(display_height/2)+80)

    gameDisplay.blit(diedTextSurf, diedTextRect)
    gameDisplay.blit(scoreTextSurf, scoreTextRect)
    gameDisplay.blit(escTextSurf, escTextRect)
    gameDisplay.blit(contTextSurf, contTextRect)
    died = True
    while died:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    return True
        pygame.display.update()
        clock.tick(15)

def moveFood(food, snake, display_width, display_height ,rectSize):
    gridCountx = display_width / rectSize
    gridCounty = display_height / rectSize
    #print(gridCountx, gridCounty)
    while True: #
        randomShiftx = 0
        randomShifty = 0
        randomShiftx = randint(1, gridCountx)
        randomShifty = randint(1, gridCounty)
        food.x = (randomShiftx * rectSize) - rectSize
        food.y = (randomShifty * rectSize) - rectSize
        if snake.overlapedWithSnake(food):
            continue
        else:
            return
if __name__ == "__main__":
    successes, failures = pygame.init()

    #Dimmension settings
    rectSize = 32   #Size of grid
    windowSizex = rectSize*20   #width of game window
    windowSizey = rectSize*10   #height of game window
    screen = pygame.display.set_mode((windowSizex, windowSizey))
    clock = pygame.time.Clock()
    FPS = 3  # Frames per second at start.
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    rect = pygame.Rect((0, 0), (rectSize, rectSize))
    food = pygame.Rect((rectSize*3, rectSize*4), (rectSize, rectSize ))
    image = pygame.Surface((rectSize, rectSize))
    image.fill(WHITE)
    image2 = pygame.Surface((rectSize, rectSize))
    image2.fill(GREEN)
    mainWindowTitle = "Snake PG"
    pygame.display.set_caption(mainWindowTitle)
    buttonPressed = "d"
    pygame.font.init()
    snake = Snake(dir, rect, rectSize, windowSizex, windowSizey)
    killed = ""
    score = 0

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    buttonPressed = "w"
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    buttonPressed = "s"
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    buttonPressed = "a"
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    buttonPressed = "d"
                elif event.key == pygame.K_ESCAPE:
                    pause = True
                    paused(windowSizex, windowSizey, screen)

        killed = snake.moveSnakeBody(buttonPressed)
        if killed == "Killed":
            respawn = died(windowSizex, windowSizey, screen,score)
            pygame.display.set_caption(mainWindowTitle + " | SCORE: "+ "0")
            if respawn:
                snake = Snake("d", rect, rectSize, windowSizex, windowSizey)
                score = 0
                FPS = 3
        if snake.checkCollideFood(food):
            score += 1
            pygame.display.set_caption(mainWindowTitle + " | SCORE: "+ str(score))
            moveFood(food, snake, windowSizex, windowSizey ,rectSize)
            if score % 6 == 0:
                FPS += 1

        screen.fill(BLACK)
        snake.drawSnake(screen, image)
        screen.blit(image2, food)
        pygame.display.update()
