import pygame
import random
import math
pygame.init()

WIDTH, HEIGHT = 800 , 550
MY_WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("<Play_PONG_with_ME>")

FPS = 60

PADDLE_WIDTH , PADDLE_HEIGHT = 25, 110
BALL_RADIUS = 10

SCORE_FONT = pygame.font.SysFont("dejavuserif", 50)
WINNING_SCORE = 10

PURPLE = (61, 0, 77)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
GREEN = (152, 251, 152) 
BLACK = (0, 0, 0)

class My_Paddle:
    COLOR = GOLD
    VELOCITY = 5

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = self.original_width = width
        self.height = self.original_height = height
    
    def draw(self, my_win):
        pygame.draw.rect(my_win, self.COLOR, (self.x, self.y, self.width, self.height), 0)
        for _ in range(4):
            pygame.draw.rect(my_win, RED, (self.x - _, self.y - _, self.width + 5, self.height + 5), 1)
    
    def move(self, up = True):
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.width = self.original_width
        self.height = self.original_height


class My_Ball:
    MAX_VELOCITY = 5
    COLOR = GOLD 

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_velo = self.MAX_VELOCITY
        self.y_velo = 0
        self.border_width = 2
        
    def draw(self, my_win):
        pygame.draw.circle(my_win, self.COLOR, (self.x, self.y), self.radius)
        pygame.draw.circle(my_win, RED, (self.x, self.y), self.radius + 2, self.border_width)

    def move(self):
        self.x += self.x_velo
        self.y += self.y_velo
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_velo = 0
        self.x_velo *= -1


def main():
    run = True 
    clock = pygame.time.Clock()
    left_paddle = My_Paddle(10, HEIGHT //2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = My_Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    ball = My_Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0
    flag = True

    while run:

        #if left_score == 0 and right_score == 0 and pygame.time.get_ticks() == 1:
        if flag == True:
            welcome(MY_WINDOW)
            pygame.display.update()
            pygame.time.delay(3000)
            #MY_WINDOW.blit(,(0,0))
            draw(MY_WINDOW,[left_paddle, right_paddle], ball, left_score, right_score)
        
        flag = False

        clock.tick(FPS)

        draw(MY_WINDOW,[left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed()
        manage_movement_paddle(keys, left_paddle, right_paddle)
        ball.move()
        manage_ball_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            pygame.time.delay(500)
            right_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
        elif ball.x > WIDTH:
            pygame.time.delay(500)
            left_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()

        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "LEFT PLAYER WON" 
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "RIGHT PLAYER WON"

        if won:
            flag = True
            text = SCORE_FONT.render(win_text, 1 , GREEN)
            MY_WINDOW.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
            draw(MY_WINDOW,[left_paddle, right_paddle], ball, left_score, right_score)

    pygame.quit()

def manage_movement_paddle(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY >= 0:
        left_paddle.move(up = True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VELOCITY + left_paddle.height <= HEIGHT:
        left_paddle.move(up = False)
    
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VELOCITY >= 0:
        right_paddle.move(up = True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VELOCITY + right_paddle.height <= HEIGHT:
        right_paddle.move(up = False)

def manage_ball_collision(ball, left_paddle, right_paddle):

    if ball.y + ball.radius >= HEIGHT or ball.y - ball.radius <= 0: # collision with upper or lower boundaries
        ball.y_velo *= -1

    if ball.x_velo < 0: # collision with left paddle
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_velo *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y_value = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VELOCITY
                y_velocity = difference_in_y_value / reduction_factor
                ball.y_velo = -1 * y_velocity
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_velo *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y_value = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VELOCITY
                y_velocity = difference_in_y_value / reduction_factor
                ball.y_velo = -1 * y_velocity




def draw(my_win, my_paddles, ball, left_score, right_score):
    my_win.fill(PURPLE)
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    my_win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    my_win.blit(right_score_text, (WIDTH * (3 / 4) - right_score_text.get_width() // 2, 20))
    
    for paddle in my_paddles:
        paddle.draw(my_win)
    for i in range(4, HEIGHT, HEIGHT // 40):
        if i % 2 == 1:
            continue
        pygame.draw.rect(my_win, WHITE, (WIDTH // 2 - 2, i, 4, HEIGHT // 40))
    ball.draw(my_win)

    pygame.display.update()

def welcome(my_win):
    my_win.fill(BLACK)
    text = "WELCOME TO A NEW GAME"
    text2 = SCORE_FONT.render(text, 1 , GOLD)
    MY_WINDOW.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 - text2.get_height() // 2))

if __name__ == '__main__':
    main()