import pygame

class Snake:
    def __init__(self, dir, headRect, rectSize, windowSizex, windowSizey):
        self.headRect = headRect
        self.body = [self.headRect]
        self.directionHistory = [dir]
        self.rectSize = rectSize
        self.windowSizex = windowSizex
        self.windowSizey = windowSizey
        self.lastDirection = 0
        #self.directionHistory = [direction]

    def addDirection(self, newDirection):
        self.directionHistory.insert(0,newDirection)

    def moveSnakeBody(self, newDirection):
        self.addDirection(newDirection)
        print(self.directionHistory)
        print(newDirection)
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
        print(self.body)

        #self.directionHistory.pop()
            #teleport(self.body[i])

    def moveUp(self):
        return 0, -self.rectSize
    def moveDown(self):
        return 0, self.rectSize
    def moveLeft(self):
        return -self.rectSize, 0
    def moveRight(self):
        return self.rectSize, 0

    def drawSnake(self, screen, image):
        for element in self.body:
            screen.blit(image, element)

    def checkCollide(self, food):
        if food.centerx == self.body[0].centerx and food.centery == self.body[0].centery:
            self.addSegment()
        #if self.body[0].colliderect(food):


    def addSegment(self):
        print("addSegment")
        print("direction.History: ", self.directionHistory)
        self.body.append(self.body[-1].copy())
        if self.directionHistory[-1] == "w":
            self.body[-1].move_ip(self.moveDown())
        if self.directionHistory[-1] == "s":
            self.body[-1].move_ip(self.moveUp())
        if self.directionHistory[-1] == "a":
            self.body[-1].move_ip(self.moveRight())
        if self.directionHistory[-1] == "d":
            self.body[-1].move_ip(self.moveLeft())

        #print("Ile segmentów:",len(self.body))
        for elem in self.body:
            print(elem)

    def teleport(self, currentRect):
        if currentRect.centerx >= self.windowSizex:
            currentRect.move_ip(-self.windowSizex, 0)
        if currentRect.centerx <= 0:
            currentRect.move_ip(self.windowSizex, 0)
        if currentRect.centery >= self.windowSizey:
            currentRect.move_ip(0, -self.windowSizey)
        if currentRect.centery <= 0:
            currentRect.move_ip(0, self.windowSizey)

successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))
#Dimmension settings
rectSize = 32
windowSizex = rectSize*20
windowSizey = rectSize*10
screen = pygame.display.set_mode((windowSizex, windowSizey))
clock = pygame.time.Clock()
FPS = 2  # Frames per second.


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# RED = (255, 0, 0), GREEN = (0, 255, 0), BLUE = (0, 0, 255).
GREEN = (0, 255, 0)

rect = pygame.Rect((0, 0), (rectSize, rectSize))
food = pygame.Rect((rectSize*3, rectSize*4), (rectSize * 3, rectSize * 4))
image = pygame.Surface((rectSize, rectSize))
image .fill(WHITE)
image2 = pygame.Surface((rectSize, rectSize))
image2 .fill(GREEN)
pygame.display.set_caption('Snake PG')
getTicksLastFrame = 0
buttonPressed = "d"
snake = Snake(dir, rect, rectSize, windowSizex, windowSizey)

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                buttonPressed = "w"
            elif event.key == pygame.K_s:
                buttonPressed = "s"
            elif event.key == pygame.K_a:
                buttonPressed = "a"
            elif event.key == pygame.K_d:
                buttonPressed = "d"
            #elif event.key == pygame.K_p:
                #snake.addSegment()

    snake.moveSnakeBody(buttonPressed)
    snake.checkCollide(food)

    #snake.drawSnake()
    #teleport(rect)

    screen.fill(BLACK)
    snake.drawSnake(screen, image)
    #screen.blit(image, rect)
    screen.blit(image2, food)
    pygame.display.update()  # Or pygame.display.flip()
