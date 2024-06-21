import math
import random
from pygame import mixer
import pygame

pygame.init()

# Screen
screen = pygame.display.set_mode((800, 600))
# background
background = pygame.image.load("background.png")
# Background sound
mixer.music.load("background.wav")
mixer.music.play(-1)
# Title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("rocket.png")
playerX = 335
playerY = 480
player_X_CHANGE = 0
player_Y_CHANGE = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemy_X_CHANGE = []
enemy_Y_CHANGE = []
number = 6
for i in range(number):
    enemyImg.append(pygame.image.load("outer.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemy_X_CHANGE.append(3)
    enemy_Y_CHANGE.append(40)

# bullet
bulletIMG = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bullet_X_CHANGE = 0
bullet_Y_CHANGE = 10
bullet_state = "ready"

# SCORE
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# game over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render('Score :' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text(x, y):
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (x,y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def bullet_fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletIMG, (x + 16, y + 10))


def collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_X_CHANGE = -3

            if event.key == pygame.K_RIGHT:
                player_X_CHANGE = 3

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound("laser.wav")
                    bullet_Sound.play()

                    bulletX = playerX
                    bullet_fire(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_X_CHANGE = 0
    # bullet movement
    if bullet_state == "fire":
        bullet_fire(bulletX, bulletY)
        bulletY -= bullet_Y_CHANGE
    playerX += player_X_CHANGE
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736
    for i in range(number):
        # Game over
        if enemyY[i] > 440:
            for j in range(number):
                enemyY[j] = 2000
            game_over_text(200,250)
            break

        if enemyX[i] <= 0:
            enemy_X_CHANGE[i] = 3
            enemyY[i] += enemy_Y_CHANGE[i]
        if enemyX[i] >= 736:
            enemy_X_CHANGE[i] = -3
            enemyY[i] += enemy_Y_CHANGE[i]

        enemyX[i] += enemy_X_CHANGE[i]
        iscollision = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if iscollision:
            explosion_Sound = mixer.Sound("explosion.wav")
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1

            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    # collision

    enemyX += enemy_X_CHANGE
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
