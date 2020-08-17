import pygame
import os


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


    except pygame.error as e:
        print("Couldn't load asset")

    return RED_SPACE_SHIP, RED_LASER, GREEN_SPACE_SHIP, GREEN_LASER, BLUE_SPACE_SHIP, BLUE_LASER, \
           YELLOW_SPACE_SHIP, YELLOW_LASER, BACKGROUND


def move_player(player, HEIGHT, WIDTH):
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