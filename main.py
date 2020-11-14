import pygame
import random
import math
import os

from pygame import mixer

# initialize the pygame
pygame.init()

# create the screen
screenX = 800
screenY = 600
screen = pygame.display.set_mode((screenX, screenY))
background = pygame.image.load(os.path.join('assets', 'background.png'))
mixer.music.load(os.path.join('assets', 'background.wav'))
mixer.music.play(-1)

# title & icon
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(pygame.image.load(os.path.join('assets', 'ufo.png')))

# player
playerImg = pygame.image.load(os.path.join('assets', 'player.png'))
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
enemyX_change_idx = 0.8
enemyY_change_idx = 0.1

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load(os.path.join('assets', 'enemy.png')))
    enemyX.append(random.randint(20, screenX - 20 - 64))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(enemyX_change_idx)
    enemyY_change.append(0)

# bullet
bulletImg = pygame.image.load(os.path.join('assets', 'bullet.png'))
bulletX = playerX + 32
bulletY = playerY
bulletX_change = 0
bulletY_change = 15
bullet_state = 'ready'

# score
score_val = 0
font = pygame.font.Font('fonts/Audiowide-Regular.ttf', 32)

textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score:" + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, idx):
    screen.blit(enemyImg[idx], (x, y))


def fire(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y - 10))


def is_collision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
    if distance < 30:
        return True
    return False


# game over
over_font = pygame.font.Font('fonts/Audiowide-Regular.ttf', 64)


def game_over_text():
    global textY
    textY = -90
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200, 230))
    score_text = font.render("Score:" + str(score_val), True, (255, 255, 255))
    screen.blit(score_text, (345, 296))


# game loop
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
                playerX_change = -1
            elif event.key == pygame.K_RIGHT:
                playerX_change = 1
            elif event.key == pygame.K_UP:
                playerY += -5
            elif event.key == pygame.K_DOWN:
                playerY += 5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound(
                        os.path.join('assets', 'laser.wav'))
                    bullet_sound.play()
                    # bulletY = playerY
                    bulletX = playerX
                    fire(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # player position change
    playerX += playerX_change * 5

    if playerX <= 0:
        playerX = 0
    elif playerX >= screenX - 64:
        playerX = screenX - 64
    if playerY <= 0:
        playerY = 0
    elif playerY >= screenY - 64:
        playerY = screenY - 64

    # enemy position change
    for i in range(num_of_enemies):
        # game over
        if enemyY[i] >= playerY - 70:
            for j in range(num_of_enemies):
                enemyY[j] = 2020

            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        enemyY[i] += enemyY_change_idx

        if enemyX[i] <= 20:
            enemyX_change[i] = enemyX_change_idx
        elif enemyX[i] >= screenX - 64 - 20:
            enemyX_change[i] = -enemyX_change_idx

        # collision
        bulletCollision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if bulletCollision is True:
            bulletY = playerY
            bullet_state = 'ready'
            enemyX[i] = random.randint(20, screenX - 20 - 64)
            enemyY[i] = random.randint(50, 150)
            score_val += 1
            print(score_val)
            # explosion sound
            explosion_sound = mixer.Sound(
                os.path.join('assets', 'explosion.wav'))
            explosion_sound.play()

            # increase enemy speed
            enemyX_change_idx *= 1.1
            enemyY_change_idx *= 1.05

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = playerY

    if bullet_state == 'fire':
        fire(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
