import pygame
import random

# initialize the pygame
pygame.init()

# create the screen
screenX = 800
screenY = 600
screen = pygame.display.set_mode((screenX, screenY))
background = pygame.image.load('assets/background.png')

# title & icon
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(pygame.image.load('assets/ufo.png'))

# player
playerImg = pygame.image.load('assets/player.png')
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg = pygame.image.load('assets/enemy.png')
enemyX = random.randint(20, screenX - 20 - 64)
enemyY = random.randint(50, 150)
enemyX_change = 3.6
enemyY_change = 0

# bullet
bulletImg = pygame.image.load('assets/bullet.png')
bulletX = playerX + 32
bulletY = playerY
bulletX_change = 0
bulletY_change = 10
bullet_state = 'ready'


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


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
                bulletY = playerY
                bulletX = playerX
                fire(bulletX, bulletY)
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
    enemyX += enemyX_change
    enemyY += 0.4

    if enemyX <= 20:
        enemyX_change = 3.6
    elif enemyX >= screenX - 64 - 20:
        enemyX_change = -3.6

    # bullet movement
    if bullet_state is 'fire':
        fire(bulletX, bulletY)
        bulletY -= bulletY_change

    if playerY - 2 <= enemyY <= playerY + 0.5:
        # enemy(random.randint(20, screenX - 20 - 64), random.randint(50, 150))
        pass
    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()
