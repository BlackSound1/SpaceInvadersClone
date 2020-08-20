import pygame

import os


def load_sounds():
    enemy_laser_1 = None
    enemy_laser_2 = None
    enemy_laser_3 = None
    enemy_laser_4 = None
    player_laser_1 = None
    player_laser_2 = None
    player_hit = None
    #space_theme = None

    pygame.mixer.init()

    # pygame.mixer.music.load("sounds/Space theme.wav")
    # pygame.mixer.music.play()

    """TEST = pygame.mixer.Sound("sounds/Enemy Ship Laser 1.wav")
    TEST.play()"""

    try:
        # LASERS
        enemy_laser_1 = pygame.mixer.Sound("sounds/Enemy Ship Laser 1.wav")
        enemy_laser_2 = pygame.mixer.Sound("sounds/Enemy Ship Laser 2.wav")
        enemy_laser_3 = pygame.mixer.Sound("sounds/Enemy Ship Laser 3.wav")
        enemy_laser_4 = pygame.mixer.Sound("sounds/Enemy Ship Laser 4.wav")
        player_laser_1 = pygame.mixer.Sound("sounds/Player Laser-001.wav")
        player_laser_2 = pygame.mixer.Sound("sounds/Player Laser-002.wav")
        player_hit = pygame.mixer.Sound("sounds/Player Gets Hit.wav")

        # MUSIC
        # space_theme = pygame.mixer.Sound("sounds/Space theme.wav")

    except pygame.error as e:
        print("Couldn't load sound")
        quit()

    # Lowers the volume for the sounds
    volume_modifier = 0.3

    enemy_laser_1.set_volume(volume_modifier)
    enemy_laser_2.set_volume(volume_modifier)
    enemy_laser_3.set_volume(volume_modifier)
    enemy_laser_4.set_volume(volume_modifier)
    player_laser_1.set_volume(volume_modifier)
    player_laser_2.set_volume(volume_modifier)
    player_hit.set_volume(volume_modifier)

    return enemy_laser_1, enemy_laser_2, enemy_laser_3, enemy_laser_4, player_laser_1, player_laser_2, player_hit


def load_assets(width, height):
    blue_laser = None
    blue_space_ship = None
    red_laser = None
    red_space_ship = None
    green_laser = None
    green_space_ship = None
    yellow_laser = None
    yellow_space_ship = None
    background = None

    try:
        # SHIPS
        red_space_ship = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
        green_space_ship = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
        blue_space_ship = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

        # PLAYER
        yellow_space_ship = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

        # LASERS
        red_laser = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
        green_laser = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
        blue_laser = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
        yellow_laser = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

        # BACKGROUND
        # Also scales background to window size
        background = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "background-black.png")), (width, height))

    except pygame.error as e:
        print("Couldn't load asset")
        quit()

    return red_space_ship, red_laser, green_space_ship, green_laser, blue_space_ship, blue_laser, \
        yellow_space_ship, yellow_laser, background


def move_player(player, height, width):
    health_bar_offset = 15
    player_velocity = 15

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player.x - player_velocity > 0:
        player.x -= player_velocity
    if keys[pygame.K_d] and player.x + player_velocity + player.get_width() < width:
        player.x += player_velocity
    if keys[pygame.K_w] and player.y - player_velocity > 0:
        player.y -= player_velocity
    if keys[pygame.K_s] and player.y + player_velocity + player.get_height() + health_bar_offset < height:
        player.y += player_velocity
    if keys[pygame.K_SPACE]:
        player.shoot()
