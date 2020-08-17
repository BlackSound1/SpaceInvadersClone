import os
import pygame
import random


def load_assets(WIDTH, HEIGHT):
    BLUE_LASER, RED_SPACE_SHIP, RED_LASER, GREEN_SPACE_SHIP, GREEN_LASER, BLUE_SPACE_SHIP, \
    YELLOW_SPACE_SHIP, YELLOW_LASER, BACKGROUND, high_score = None, None, None, None, None, None, \
                                                              None, None, None, None

    try:
        # SHIPS
        RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
        GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
        BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

        # PLAYER
        YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

        # LASERS
        RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
        GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
        BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
        YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

        # BACKGROUND
        # Also scales background to window size
        BACKGROUND = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

        # HIGH SCORE
        with open("HighScore.txt", 'r') as reader:
            high_score = int(reader.read(-1))  # Reads whole file

    except pygame.error as e:
        print("Couldn't load asset")

    return RED_SPACE_SHIP, RED_LASER, GREEN_SPACE_SHIP, GREEN_LASER, BLUE_SPACE_SHIP, BLUE_LASER, \
           YELLOW_SPACE_SHIP, YELLOW_LASER, BACKGROUND, high_score


def move_player(player, WIDTH, HEIGHT):
    HEALTH_BAR_OFFSET = 15
    player_velocity = 15

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player.x - player_velocity > 0:
        player.x -= player_velocity
    if keys[pygame.K_d] and player.x + player_velocity + player.get_width() < WIDTH:
        player.x += player_velocity
    if keys[pygame.K_w] and player.y - player_velocity > 0:
        player.y -= player_velocity
    if keys[pygame.K_s] and player.y + player_velocity + player.get_height() + HEALTH_BAR_OFFSET < HEIGHT:
        player.y += player_velocity
    if keys[pygame.K_SPACE]:
        player.shoot()


def move_enemies(player, enemies, HEIGHT, laser_velocity, lives):
    enemy_velocity = 10

    for enemy in enemies[:]:  # [:] makes a copy of enemies, I think?
        enemy.move(enemy_velocity)

        enemy.move_lasers(laser_velocity, player)  # Moves Enemy Lasers given their velocity and the player

        # Handles Enemy randomly shooting each second
        if random.randrange(0, 4 * 60) == 1:
            enemy.shoot()

        # If Enemy collides with Player, remove Player health and remove Enemy
        if collide(enemy, player):
            player.health -= 10
            enemies.remove(enemy)

        # If Enemy is off-screen, remove it
        elif enemy.y + enemy.get_height() > HEIGHT:
            lives -= 1
            enemies.remove(enemy)

        return lives, enemies


def collide(object1, object2):
    # Determines if there are overlapping pixels between 2 objects
    offset_x = object2.x - object1.x
    offset_y = object2.y - object1.y
    return object1.mask.overlap(object2.mask, (offset_x, offset_y)) is not None
