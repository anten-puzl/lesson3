import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
from copy import copy
from random import randint


BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0



pygame.init()
font = pygame.font.SysFont('Verdana', 20)

FPS = pygame.time.Clock()

screen = width, heigth = 800, 600

main_surface = pygame.display.set_mode(screen)

player = pygame.image.load('img\player.png').convert_alpha()
player_rect = player.get_rect()
speed = 7

def create_enemy():
    enemy = pygame.image.load('img\enemy.png').convert_alpha()
    enemy_rect = pygame.Rect(width-20, randint(0, heigth), *enemy.get_size())
    enemy_speed = randint(2,5)
    return [enemy, enemy_rect, enemy_speed]


def create_bonus():
    bonus = pygame.image.load('img/bonus.png').convert_alpha()
    bonus_width = bonus.get_size()[0]
    bonus_height = bonus.get_size()[1]
    bonus_rect = pygame.Rect(randint(0+bonus_width, width-bonus_width), 0,*bonus.get_size())
    bonus_speed = randint(2,5)
    return [bonus, bonus_rect, bonus_speed]


bg = pygame.transform.scale(pygame.image.load('img/background.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1600)


enemies = []
bonuses = []
scores = 0

is_working = True

while is_working:
    FPS.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
    pressed_key = pygame.key.get_pressed()

    bgX -= bg_speed
    bgX2 -= bg_speed

    if bgX < - bg.get_width():
        bgX = bg.get_width()
    if bgX2 < - bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(bg, (bgX,0))
    main_surface.blit(bg, (bgX2, 0))
    main_surface.blit(font.render(str(scores), True, BLACK), (width - 30, 0))
    if pressed_key[K_DOWN]:
        if player_rect.bottom <= heigth:
            player_rect = player_rect.move((0, speed))
    elif pressed_key[K_UP]:
        if player_rect.top >= 0:
            player_rect = player_rect.move((0, -speed))
    elif pressed_key[K_LEFT]:
        if player_rect.left >= 0:
            player_rect = player_rect.move((-speed, 0))
    elif pressed_key[K_RIGHT]:
        if player_rect.right <= width:
            player_rect = player_rect.move((speed, 0))

    for enemy in copy(enemies):
        enemy[1] = enemy[1].move(-enemy[2],0)
        main_surface.blit(enemy[0], enemy[1])
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
        if player_rect.colliderect(enemy[1]):
            is_working = False

    for bonus in copy(bonuses):
        bonus[1] = bonus[1].move(0,bonus[2])
        main_surface.blit(bonus[0], bonus[1])
        if bonus[1].bottom > heigth:
            bonuses.pop(bonuses.index(bonus))
        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1

    main_surface.blit(player, player_rect)

    pygame.display.flip()
