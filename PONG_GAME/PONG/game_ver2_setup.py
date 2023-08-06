from .paddle import Paddle
from .ball import Ball
import pygame
import random
import winsound
pygame.init()


class GameInformation:
    def __init__(self, left_hits, right_hits, left_score, right_score):
        self.left_hits = left_hits
        self.right_hits = right_hits
        self.left_score = left_score
        self.right_score = right_score


class Game:
    SCORE_FONT = pygame.font.SysFont("dejavuserif", 50)
    FONT2 = pygame.font.SysFont("ariel", 40)
    FONT3 = pygame.font.SysFont("ariel", 25)
    PURPLE = (61, 0, 77)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    GOLD = (255, 215, 0)
    GREEN = (152, 251, 152) 
    BLACK = (0, 0, 0)
    flag = True
    flag2 = False

    def __init__(self, window, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height

        self.left_paddle = Paddle(10, self.window_height // 2 - Paddle.HEIGHT // 2)
        self.right_paddle = Paddle(self.window_width - 10 - Paddle.WIDTH, self.window_height // 2 - Paddle.HEIGHT//2)
        self.ball = Ball(self.window_width // 2, self.window_height // 2)

        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0
        self.window = window

    def _draw_score(self):
        left_score_text = self.SCORE_FONT.render(f"{self.left_score}", 1, self.WHITE)
        right_score_text = self.SCORE_FONT.render(f"{self.right_score}", 1, self.WHITE)
        self.window.blit(left_score_text, (self.window_width // 4 - left_score_text.get_width()//2, 20))
        self.window.blit(right_score_text, (self.window_width * (3/4) - right_score_text.get_width()//2, 20))

    def _draw_hits(self):
        hits_text = self.SCORE_FONT.render(f"{self.left_hits + self.right_hits}", 1, self.RED)
        self.window.blit(hits_text, (self.window_width // 2 - hits_text.get_width()//2, 10))

    def _draw_divider(self):
        for i in range(4, self.window_height, self.window_height//40):
            if i % 2 == 1:
                continue
            pygame.draw.rect(self.window, self.WHITE, (self.window_width//2 - 2, i, 4, self.window_height//40))

    def _handle_collision(self):
        ball = self.ball
        left_paddle = self.left_paddle
        right_paddle = self.right_paddle

        if ball.y + ball.RADIUS >= self.window_height:
            ball.y_velo *= -1
        elif ball.y - ball.RADIUS <= 0:
            ball.y_velo *= -1

        if ball.x_velo < 0:
            if ball.y >= left_paddle.y and ball.y <= left_paddle.y + Paddle.HEIGHT:
                if ball.x - ball.RADIUS <= left_paddle.x + Paddle.WIDTH:
                    ball.x_velo *= -1

                    middle_y = left_paddle.y + Paddle.HEIGHT / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (Paddle.HEIGHT / 2) / ball.MAX_VEL
                    y_velo = difference_in_y / reduction_factor
                    ball.y_velo = -1 * y_velo
                    self.left_hits += 1
                    winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

        else:
            if ball.y >= right_paddle.y and ball.y <= right_paddle.y + Paddle.HEIGHT:
                if ball.x + ball.RADIUS >= right_paddle.x:
                    ball.x_velo *= -1

                    middle_y = right_paddle.y + Paddle.HEIGHT / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (Paddle.HEIGHT / 2) / ball.MAX_VEL
                    y_velo = difference_in_y / reduction_factor
                    ball.y_velo = -1 * y_velo
                    self.right_hits += 1
                    winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

    def draw(self, draw_score=True, draw_hits=False):
        self.window.fill(self.PURPLE)

        self._draw_divider()

        if draw_score:
            self._draw_score()

        if draw_hits:
            self._draw_hits()

        for paddle in [self.left_paddle, self.right_paddle]:
            paddle.draw(self.window)

        self.ball.draw(self.window)

    def welcome(self):
        self.window.fill(self.BLACK)
        text = "WELCOME TO A NEW GAME"
        instruction = "Press 'W' for moving up and 'S' for moving down"
        text2 = self.SCORE_FONT.render(text, 1 , self.GOLD)
        text3 = self.FONT2.render(instruction, 1, self.GOLD)
        self.window.blit(text2, (self.window_width // 2 - text2.get_width() // 2, 100))
        self.window.blit(text3, (self.window_width // 2 - text3.get_width() // 2, 350))

    # def rewelcome(self):
    #     self.window.fill(self.BLACK)
    #     text = """Press spacebar to continue with a new game 
    #                     otherwise press ESC to exit"""
    #     text_ =self.FONT3.render(text, 1 ,self.GOLD)
    #     self.window.blit(text_, (self.window_width // 2 - text_.get_width() // 2, 250))
    
    def move_paddle(self, left=True, up=True):
        
        if left:
            if up and self.left_paddle.y - Paddle.VELOCITY < 0:
                return False
            if not up and self.left_paddle.y + Paddle.HEIGHT > self.window_height:
                return False
            self.left_paddle.move(up)
        else:
            if up and self.right_paddle.y - Paddle.VELOCITY < 0:
                return False
            if not up and self.right_paddle.y + Paddle.HEIGHT > self.window_height:
                return False
            self.right_paddle.move(up)

        return True

    def loop(self):
        if self.flag == True:
            self.flag = False
            self.welcome()
            pygame.display.update()
            pygame.time.delay(3000)
            self.draw()
        
        # if self.flag2 == True:
        #     self.flag2 = False
        #     self.rewelcome()
        #     pygame.display.update()
        #     pygame.time.delay(3000)
        #     self.draw()

        self.ball.move()
        self._handle_collision()

        score = False
        if self.ball.x < 0:
            score = True
            self.ball.reset()
            self.right_score += 1
        elif self.ball.x > self.window_width:
            score = True
            self.ball.reset()
            self.left_score += 1
        if score  == True:
            self.left_paddle.reset()
            self.right_paddle.reset()

        game_info = GameInformation(self.left_hits, self.right_hits, self.left_score, self.right_score)
        
        won = False
        WIN_SCORE = 10
        if self.left_score >= WIN_SCORE:
            won = True
            win_text = "YOU HAVE WON" 
        elif self.right_score >= WIN_SCORE:
            won = True
            win_text = "COMPUTER WINS"

        if won:
            self.flag = True
            self.flag2 = True
            self.draw()
            text = self.SCORE_FONT.render(win_text, 1 , self.GREEN)
            self.window.blit(text, (self.window_width // 2 - text.get_width() // 2, self.window_height // 2 - text.get_height() // 2))
            pygame.display.update()
            winsound.PlaySound('SystemExclamation',winsound.SND_ALIAS)
            pygame.time.delay(5000)
            self.ball.reset()
            self.left_paddle.reset()
            self.right_paddle.reset()
            self.left_score = 0
            self.right_score = 0

        return game_info

    def reset(self):
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0
