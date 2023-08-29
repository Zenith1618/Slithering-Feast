import pygame
import random
from enum import Enum
from collections import namedtuple      # namedtuple assign a meaning to each position in tuple which increase readability 

pygame.init()       # To initialize the modules
font = pygame.font.Font('arial.ttf', 25)        #we can use file from the system as well by using SysFont but thats slow

# This restrict the type of command one can give to make the game errorless(like someone might even say d or down)
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


#this is a lightweight class, whose objects can be directly created
Point = namedtuple('Point', 'x, y')   

BLOCK_SIZE = 20     #to make uniformity with the snake size and pixel
SPEED = 10          # higher the number faster is the game

#rgb Colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0,0,255)
BLUE2 = (0,100,255)
BLACK = (0,0,0)

class SnakeGame:

    #w: width       h: height
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        # initialize display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake")     # Screen Caption
        self.clock = pygame.time.Clock()        # To track time, but basically being usef here to control the speed of game


        #initialize game state
        self.direction = Direction.RIGHT

        # self.head = [self.w, self.h]  
        # # Like list[0] is x and list[1] is y coord, but this is error prone
        self.head = Point(self.w/2, self.h/2)       # to start from the centre
        self.snake = [self.head, Point(self.head.x - BLOCK_SIZE, self.head.y), 
                      Point(self.head.x - (2*BLOCK_SIZE), self.head.y)]      #to make the snake
        
        self.score = 0
        self.food = None

        # Helper function(because it will be used later on, so no need to repeat the same code) to place food
        self._place_food()

    def _place_food(self):

        x = random.randint(0, (self.w - BLOCK_SIZE)// BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE)// BLOCK_SIZE)*BLOCK_SIZE

        self.food = Point(x, y)

        # to check if the food has not been placed on the snake itself
        if self.food in self.snake:
            self._place_food()



    def play_step(self):
        
        #1. Collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        #2. move
        self._move(self.direction)   #update the head
        self.snake.insert(0, self.head)     #to insert at beginning 

        #3. Check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
        
        #4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()    #because in the move we added a block

        #5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED+(self.score*0.3))


        #6. return game over and score
        
        return game_over, self.score
    

    def _is_collision(self):
        
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True

        # hits itself
        if self.head in self.snake[1:]:
            return True
        
        return False

    def _update_ui(self):
        # the order here is important
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12,12))

        #for food
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        #Score
        text = font.render("Score: "+ str(self.score), True, WHITE)
        self.display.blit(text, [0,0])  # to show the the text on the screen
        pygame.display.flip()   # To update the whole display to screen


    def _move(self, direction):
        x = self.head.x
        y = self.head.y

        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        
        self.head = Point(x,y)


if __name__ == '__main__':
    game = SnakeGame()

    #game loop
    while True:
        game_over, score = game.play_step()

        # break if game over
        if game_over == True:
            break
    print('Final Score', score)
    pygame.quit()       #To close all the modules
