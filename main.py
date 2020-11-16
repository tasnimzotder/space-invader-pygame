import pygame
import random
import math
import os
import sys
import utils.scoreHandler as sh

from pygame import mixer

# initialize the pygame
pygame.init()

# game loop
running = False
setup_running = True

# game timing
FPS = 60
clock = pygame.time.Clock()
fps_count = 0

# blink cursor
blink_cursor = '|'

# create the screen
screenX = 800
screenY = 600
screen = pygame.display.set_mode((screenX, screenY))
background = pygame.image.load(os.path.join('assets', 'background.png'))
mixer.music.load(os.path.join('assets', 'background.wav'))
mixer.music.play(-1)

# title & icon
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(pygame.image.load(os.path.join('assets', 'enemy.png')))

# player
playerImg = pygame.image.load(os.path.join('assets', 'player.png'))
playerX = 370
playerY = 480
playerX_change = 0
player_name = ''

# bullet
bulletImg = pygame.image.load(os.path.join('assets', 'bullet.png'))
bulletX = playerX + 32
bulletY = playerY
bulletX_change = 0
bulletY_change = 25
bullet_state = 'ready'

# score
score_val = 0
font = pygame.font.Font('fonts/Audiowide-Regular.ttf', 32)

textX = 10
textY = 10


def show_score(x: float, y: float):
    score = font.render("Score:\t" + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x: float, y: float):
    screen.blit(playerImg, (x, y))


def fire(x: float, y: float):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y - 10))


def is_collision(x1: float, y1: float, x2: float, y2: float):
    distance = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
    if distance < 30:
        return True
    return False


# reload game
def reload_game(event):
    global textX, textY
    global score_val

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_F5:
            # set score diplay default
            textX = 10
            textY = 10

            score_val = 0
            main()


# quit window
def quit_window(event, var_name: str, value: bool):
    global score_val, running, setup_running

    if event.type == pygame.QUIT:
        if var_name == 'running':
            running = value
        elif var_name == 'setup_running':
            setup_running = value
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            if var_name == 'running':
                running = value
            elif var_name == 'setup_running':
                setup_running = value
            sys.exit()


# game over
over_font = pygame.font.Font('fonts/Audiowide-Regular.ttf', 64)


def game_over_text():
    global textY
    textY = -90

    scoresFile = sh.readScoresFile()
    if score_val > scoresFile['highscore']['score']:
        sh.writeScoresFile(player_name, score_val)

    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (180, 160))

    score_text = font.render("Score: " + str(score_val) + "\t\t" + player_name,
                             True, (255, 255, 255))
    screen.blit(score_text, (285, 246))

    highscore_text = font.render(
        "Highscore: " + str(scoresFile['highscore']['score']) + "\t\t" +
        scoresFile['highscore']['player'], True, (255, 255, 255))
    screen.blit(highscore_text, (212, 285))

    reload_text = font.render('* Press F5 to reload *', True, (240, 95, 38))
    screen.blit(reload_text, (220, 450))


# game setup window
def get_user_details(message: str):
    global player_name
    inp_font = pygame.font.Font('fonts/Audiowide-Regular.ttf', 32)
    text_surface = inp_font.render(message + ': ' + player_name + blink_cursor,
                                   True, (255, 255, 255))
    screen.blit(text_surface, (screenX / 2 - 220, screenY / 3))


def main():
    global playerX, playerY
    global playerX_change
    global bulletX, bulletY
    global bullet_state
    global score_val
    global player_name
    global fps_count, blink_cursor

    # game loop
    global running, setup_running

    # enemy
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 6
    enemyX_change_idx = 2.0
    enemyY_change_idx = 0.3

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load(os.path.join('assets', 'enemy.png')))
        enemyX.append(random.randint(20, screenX - 20 - 64))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(enemyX_change_idx)
        enemyY_change.append(0)

    def enemy(x: float, y: float, idx: float):
        screen.blit(enemyImg[idx], (x, y))

    # game setup window
    while setup_running:
        clock.tick(FPS)

        # fps count
        if fps_count < 60:
            fps_count += 1
        else:
            fps_count = 0

        if fps_count // 10 in [0, 1, 2]:
            blink_cursor = '|'
        else:
            blink_cursor = ''

        # background image
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            quit_window(event, setup_running, False)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    setup_running = False
                    running = True
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    if len(player_name) <= 12:
                        player_name += event.unicode

        get_user_details('Player Name')
        pygame.display.update()

    # main game window
    while running:
        clock.tick(FPS)

        screen.fill((0, 0, 0))
        # background image
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            quit_window(event, running, False)
            reload_game(event)

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    playerX_change = -1
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    playerX_change = 1
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    playerY += -5
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
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
                if event.key in [
                        pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d
                ]:
                    playerX_change = 0

        # player position change
        playerX += playerX_change * 10

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
            bulletCollision = is_collision(enemyX[i], enemyY[i], bulletX,
                                           bulletY)
            if bulletCollision is True:
                bulletY = playerY
                bullet_state = 'ready'
                enemyX[i] = random.randint(20, screenX - 20 - 64)
                enemyY[i] = random.randint(50, 150)
                score_val += 1
                print('Score: {0}'.format(score_val))
                # explosion sound
                explosion_sound = mixer.Sound(
                    os.path.join('assets', 'explosion.wav'))
                explosion_sound.play()

                # increase enemy speed
                if score_val < 13:
                    enemyX_change_idx *= 1.1
                    enemyY_change_idx *= 1.05

            # display enemy
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


if __name__ == '__main__':
    main()