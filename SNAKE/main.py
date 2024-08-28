import pygame
import sys
import random
from pygame.math import Vector2

class FRUIT:
    def __init__(self):
        self.reposition()
    
    def draw_fruit(self):
        #create and draw a rectangle
        fruit_rect = pygame.Rect(self.position.x * cell_size, self.position.y * cell_size, cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def reposition(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.position = Vector2(self.x, self.y)

class SNAKE:
    def __init__(self):
        self.body = [Vector2(6,10), Vector2(5, 10), Vector2(4, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

        self.head_up = pygame.image.load('images/snake/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('images/snake/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('images/snake/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('images/snake/head_left.png').convert_alpha()
		
        self.tail_up = pygame.image.load('images/snake/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('images/snake/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('images/snake/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('images/snake/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('images/snake/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('images/snake/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('images/snake/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('images/snake/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('images/snake/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('images/snake/body_bl.png').convert_alpha()
    
    def draw_snake(self):
        self.update_head()
        self.update_tail()
        
        for idx, block in enumerate(self.body):
            block_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)

            if idx == 0:
                screen.blit(self.head, block_rect)

            elif idx == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
                 
            else:
                previous_block = self.body[idx + 1] - block
                next_block = self.body[idx - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)

                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)

                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)

                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)

                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head(self):
        direction = self.body[1] - self.body[0]
        if direction == Vector2(1,0): 
            self.head = self.head_left
        elif direction == Vector2(-1,0): 
            self.head = self.head_right
        elif direction == Vector2(0,1): 
            self.head = self.head_up
        elif direction == Vector2(0,-1): 
            self.head = self.head_down

    def update_tail(self):
        direction = self.body[-2] - self.body[-1]
        if direction == Vector2(1,0): 
            self.tail = self.tail_left
        elif direction == Vector2(-1,0): 
            self.tail = self.tail_right
        elif direction == Vector2(0,1): 
            self.tail = self.tail_up
        elif direction == Vector2(0,-1): 
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]
    
    def add_block(self):
        self.new_block = True

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_eats()
        self.check_collision()
    
    def draw(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_eats(self):
        #check if snake eats fruit
        if self.fruit.position == self.snake.body[0]:
            #reposition fruit
            self.fruit.reposition()
            #add a block to the snake body
            self.snake.add_block()
        
        # if new fruit position comes on snake body then reposition fruit
        for block in self.snake.body[1:]:
            if block == self.fruit.position:
                self.fruit.reposition()

    def check_collision(self):
        #check if snake hits boundary
        if not 0 <= self.snake.body[0].x < cell_number or  not 0 <= self.snake.body[0].y <= cell_number :
            self.game_over()
        #check if snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    
    def draw_score(self):
        score = "SCORE : " + str(len(self.snake.body) - 3)
        score_surface = font.render(score, True, (255,255,255))
        score_rect = score_surface.get_rect(topright = (cell_size * cell_number - 60, cell_size * cell_number - 30))
        screen.blit(score_surface, score_rect)

    def game_over(self):
        pygame.time.delay(5000)
        pygame.quit()
        sys.exit()
    


pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
screen_rect = pygame.Rect(0, 0, cell_size * cell_number, cell_size * cell_number)
pygame.display.set_caption("SNAKE GAME")
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

apple = pygame.image.load('images/apple.png').convert_alpha()
apple = pygame.transform.scale(apple, (cell_size , cell_size))
grass = pygame.image.load('images/grass.jpg').convert_alpha()
grass = pygame.transform.scale(grass, (cell_size * cell_number, cell_size * cell_number))
font = pygame.font.Font('freesansbold.ttf', 25)

game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

run_game = True
while run_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if game.snake.direction.y != 1:
                    game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                if game.snake.direction.x != -1:
                    game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN:
                if game.snake.direction.y != -1:
                    game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if game.snake.direction.x != 1:
                    game.snake.direction = Vector2(-1, 0)

    screen.blit(grass, screen_rect)
    game.draw()
    pygame.display.update()
    clock.tick(60)
