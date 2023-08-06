import pygame
from pygame import mixer
import math
import random
pygame.init()

screen = pygame.display.set_mode((850, 600))

pygame.display.set_caption("SPACE INVADERS")
icon = pygame.image.load('images/arcade-game.png')
pygame.display.set_icon(icon)

background = pygame.image.load('images/background.png')
default = (850, 600)
background = pygame.transform.scale(background, default)

pygame.time.delay(4000)

player_imag = pygame.image.load('images/space-invaders.png')
default_imag_size = (64,64)
player_imag = pygame.transform.scale(player_imag, default_imag_size)
player_pos_x = 395
player_pos_y = 480
change_x = 0

enemy_imag = []
enemy_pos_x = []
enemy_pos_y = []
change_enemy_x =[]
change_enemy_y = []
number_of_enemies = 6
for i in range(number_of_enemies):
    imag = pygame.image.load('images/ufo.png')
    default_imag_size2 = (35,35)
    imag = pygame.transform.scale(imag, default_imag_size2)
    enemy_imag.append(imag)
    enemy_pos_x.append(random.randint(0, 785))
    enemy_pos_y.append(random.randint(25, 130))
    x = random.randint(1, 2)
    change_enemy_x.append(0.3 if x == 1 else -0.3)
    change_enemy_y.append(30)

bullet_imag = pygame.image.load('images/bullet.png')
default_imag_size3 = (32, 32)
bullet_imag = pygame.transform.scale(bullet_imag, default_imag_size3)
bullet_pos_x = 0
bullet_pos_y = 480
change_bullet_y = -1.1
bullet_state = "ready"


score_value = 0
flag = 0
font = pygame.font.Font('freesansbold.ttf',32)
text_x = 10
text_y = 10

over_font = pygame.font.Font('freesansbold.ttf',64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (250, 250, 250))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(player_imag, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_imag[i], (x, y))

def fire_bullet(x, y):
    global bullet_state 
    bullet_state = "fire"
    screen.blit(bullet_imag, (x + 16, y + 16))

def collision(x_enemy, y_enemy, x_bullet, y_bullet):
    distance = math.sqrt((x_enemy - x_bullet) ** 2 + (y_enemy - y_bullet) ** 2)
    return distance <= 25

game = True
while game:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                change_x = -0.5
            if event.key == pygame.K_RIGHT:
                change_x = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('audio/laser.mp3')
                    bullet_sound.play()
                    bullet_pos_x = player_pos_x
                    fire_bullet(bullet_pos_x, bullet_pos_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                change_x = 0
    player_pos_x += change_x

    if player_pos_x <= 0:
        player_pos_x = 0
    if player_pos_x >= 786:
        player_pos_x = 786

    for i in range(number_of_enemies):

        if enemy_pos_y[i] >= 440:
            for j in range(number_of_enemies):
                enemy_pos_y = 1000
            game_over_text()
            flag = 1
            break

        enemy_pos_x[i] += change_enemy_x[i]
        if enemy_pos_x[i] <= 0:
            change_enemy_x[i] = 0.3
            enemy_pos_y[i] += change_enemy_y[i] 
        elif enemy_pos_x[i] >= 805:
            change_enemy_x[i] = -0.3
            enemy_pos_y[i] += change_enemy_y[i]
        col = collision(enemy_pos_x[i], enemy_pos_y[i], bullet_pos_x,bullet_pos_y)
        if col:
            explosion_sound = mixer.Sound('audio/explosion.wav')
            explosion_sound.play()
            bullet_pos_y = 480
            bullet_state = "ready"
            score_value+= 1
            enemy_pos_x[i] = random.randint(0, 785)
            enemy_pos_y[i] = random.randint(25, 130) 
        enemy(enemy_pos_x[i], enemy_pos_y[i], i)

    if bullet_pos_y <= 0:
        bullet_pos_y = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_pos_x, bullet_pos_y)
        bullet_pos_y += change_bullet_y
    
            
    player(player_pos_x, player_pos_y)
    show_score(text_x, text_y)
    pygame.display.update()
    if flag == 1:
        pygame.time.delay(5000)