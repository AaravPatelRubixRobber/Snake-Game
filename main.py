#imports and initializes neccasary variables

import pygame
import time
import random


pygame.init()
pygame.font.init()

black = (0,0,0)
white = (255, 255, 255)
green = (0, 255, 0)
dark_green = (0, 200, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
purple = (255, 0, 255)
yellow = (255, 255, 0)
gray = (100, 100, 100)

screen_x, screen_y = 600, 600
screen = pygame.display.set_mode((screen_x, screen_y), 0, 32)

unit = screen_x/10

#creates the snake
class snake:

    def __init__(self, game, apple, length, head_pos):
        self.game = game
        self.apple = apple
        self.length = length
        self.color = green
        self.head_pos = head_pos#on square grid
        self.dir = "UP"
        self.body_pos = [[head_pos[0], head_pos[1] + i] for i in range(length)]

    def HIT_SELF(self):
        #checks if the snake hit himself
        for pos in self.body_pos:
            if self.body_pos.count(pos) >= 2:
                return True
        else:
            return False

    def HIT_WALL(self):
        #checks if the snake hit a wall
        if self.head_pos[0] >= self.game.side_len or self.head_pos[0] < 0:
            return True
        elif self.head_pos[1] >= self.game.side_len or self.head_pos[1] < 0:
            return True
        else:
            return False

    def HIT_APPLE(self):
        #checks if the snake hit an apple
        if self.head_pos == self.apple.pos:
            return True
        else:
            return False

    def increase_len(self):
        #increases the length of the snake
        self.length += 1
        self.body_pos.append([-1, -1])
        

    def update_pos(self):
        #moves the snake
        
        pressed = pygame.key.get_pressed()
        
        if pressed[pygame.K_LEFT] and self.dir != "RIGHT":
            self.dir = "LEFT"
        if pressed[pygame.K_RIGHT] and self.dir != "LEFT":
            self.dir = "RIGHT"
        if pressed[pygame.K_UP] and self.dir != "DOWN":
            self.dir = "UP"
        if pressed[pygame.K_DOWN] and self.dir != "UP":
            self.dir = "DOWN"
            
        if self.dir == "LEFT":
            self.head_pos = [self.head_pos[0] - 1, self.head_pos[1]]

            temp_body_pos = [self.head_pos]
            for i in self.body_pos[:-1]:
                temp_body_pos.append(i)
            self.body_pos = temp_body_pos
            
        if self.dir == "RIGHT":
            self.head_pos = [self.head_pos[0] + 1, self.head_pos[1]]

            temp_body_pos = [self.head_pos]
            for i in self.body_pos[:-1]:
                temp_body_pos.append(i)
            self.body_pos = temp_body_pos
            
        if self.dir == "UP":
            self.head_pos = [self.head_pos[0], self.head_pos[1] - 1]
            
            temp_body_pos = [self.head_pos]
            for i in self.body_pos[:-1]:
                temp_body_pos.append(i)
            self.body_pos = temp_body_pos
            
        if self.dir == "DOWN":
            self.head_pos = [self.head_pos[0], self.head_pos[1] + 1]

            temp_body_pos = [self.head_pos]
            for i in self.body_pos[:-1]:
                temp_body_pos.append(i)
            self.body_pos = temp_body_pos
            
    def draw(self):

        #draws the snake
        for pos in self.body_pos[:1]:
            pygame.draw.rect(screen, dark_green, (pos[0]*self.game.unit_dim, pos[1]*self.game.unit_dim, self.game.unit_dim, self.game.unit_dim))
        for pos in self.body_pos[1:]:
            pygame.draw.rect(screen, green, (pos[0]*self.game.unit_dim, pos[1]*self.game.unit_dim, self.game.unit_dim, self.game.unit_dim))

        #displays score
        myfont = pygame.font.SysFont('Arial', 30)

        textsurface = myfont.render(str(self.length), False, yellow)

        screen.blit(textsurface,(0,0))

#creates an apple
class apple:
    def __init__(self, game_width, unit_width):
        self.pos = [game_width//2, game_width//4]
        self.growth = 1
        self.game_width = game_width
        self.unit_width = unit_width
    def spawn(self):

        #creates a random place for the apple to spawn
        self.pos = [random.randint(0, game_width-1), random.randint(0, game_width-1)]
    def draw(self):

        #draws the apple
        pygame.draw.rect(screen, red, (self.pos[0]*self.unit_width, self.pos[1]*self.unit_width, self.unit_width, self.unit_width))

class game:
    def __init__(self, side_len):
        self.side_len = side_len
        self.color = black
        self.unit_dim = int(screen_x/side_len)
    def draw(self):

        #draws the background
        screen.fill(black)

        #vert lines
        for i in range(1, self.side_len):
            pygame.draw.line(screen, white, (i*self.unit_dim, 0), (i*self.unit_dim, screen_y))

        #hori line
        for i in range(1, self.side_len):
            pygame.draw.line(screen, white, (0, i*self.unit_dim), (screen_x, i*self.unit_dim))

        #pygame.font.init() 
        

#initializes all the objects           
game_width = 20

a = apple(game_width, int(screen_x/game_width))
g = game(game_width)        
s = snake(g, a, 1, [game_width//2, game_width//2])


run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #updates the snake's position
    s.update_pos()

    #checks if the snake hit anything
    if s.HIT_WALL():
        run = False
        print("hit wall")

    if s.HIT_SELF():
        run = False
        print("hit self")

    if s.HIT_APPLE():
        s.increase_len()
        a.spawn()
        
    
    #draws stuff
    g.draw()
    s.draw()
    a.draw()

    pygame.display.update()

    time.sleep(.1)



