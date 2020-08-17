import os
import pygame
import random
import Functions

pygame.font.init()  # Initializes font stuff

# SET UP IMPORTANT OPTIONS #
WIDTH, HEIGHT = 750, 750
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders Clone")
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# LOAD ASSETS #

RED_SPACE_SHIP, RED_LASER, GREEN_SPACE_SHIP, GREEN_LASER, BLUE_SPACE_SHIP, BLUE_LASER, YELLOW_SPACE_SHIP, \
    YELLOW_LASER, BACKGROUND, high_score = Functions.load_assets(WIDTH, HEIGHT)


class Ship:
    MAX_COOLDOWN = 5

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_timer = 0

    def draw(self, window):
        # pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50))
        window.blit(self.ship_img, (self.x, self.y))

        # Draws all the Lasers
        for laser in self.lasers:
            laser.draw(window)

    # Getters to get the Ship's height and width
    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    # Handles the cooldown timer
    def cooldown(self):
        if self.cool_down_timer >= self.MAX_COOLDOWN:  # If current cooldown meets max cooldown, reset it
            self.cool_down_timer = 0
        elif self.cool_down_timer > 0:  # Otherwise just increment it
            self.cool_down_timer += 1

    # Handles shooting
    def shoot(self):
        if self.cool_down_timer is 0:  # Only shoots if cooldown is over
            # Creates new laser and adds it to the Ships list of Lasers
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)

            self.cool_down_timer = 1

    def move_lasers(self, velocity, obj):
        self.cooldown()  # Increments cooldown each time Lasers move

        # moves all Lasers that exist
        for laser in self.lasers:
            laser.move(velocity)

            # Handles removing the Lasers if off-screen or if they hit Player
            if laser.is_off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)


class Player(Ship):  # Inherits from Ship
    def __init__(self, x, y, health=100):
        super(Player, self).__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)  # Sets a mask for pixel-perfect collision
        self.max_health = health
        self.score = 0

    def move_lasers(self, velocity, objs):
        self.cooldown()  # Increments cooldown each time Lasers move

        # moves all Lasers that exist
        for laser in self.lasers:
            laser.move(velocity)

            # Handles removing the Lasers if off-screen or if they hit Enemy
            if laser.is_off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                # Basically, loops through all Enemies, and if one is colliding with a Laser, remove it and the Laser
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.score += 1  # Increments score

                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def health_bar(self, window):
        # Draws red rectangle with constant length
        pygame.draw.rect(window, RED, (self.x, self.y + self.ship_img.get_height() + 10,
                                       self.ship_img.get_width(), 10))

        # Draws green rectangle with a length dependant on how much health there is left
        pygame.draw.rect(window,
                         GREEN,
                         (self.x, self.y + self.ship_img.get_height() + 10,
                          self.ship_img.get_width() * (self.health / self.max_health),
                          10))

    # Overrides draw method to include health bar
    def draw(self, window):
        super(Player, self).draw(window)
        self.health_bar(window)


class Enemy(Ship):
    # Creates an association between given colours and the pictures to load
    COLOUR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    def __init__(self, x, y, colour, health=100):
        super(Enemy, self).__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOUR_MAP[colour]  # Sets ship and laser images based on given colour
        self.mask = pygame.mask.from_surface(self.ship_img)  # Sets a mask for pixel-perfect collision

    # Moves enemy ships downward
    def move(self, velocity):
        self.y += velocity

    # Handles shooting
    def shoot(self):
        if self.cool_down_timer is 0:  # Only shoots if cooldown is over
            # Creates new laser and adds it to the Ships list of Lasers
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)

            self.cool_down_timer = 1


class Laser:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self, velocity):
        self.y += velocity

    def is_off_screen(self, height):
        return not (height >= self.y >= 0)

    def collision(self, obj):
        return Functions.collide(obj, self)


def main():
    # Sets up useful variables
    run = True
    FPS = 60
    level = 0
    lives = 5
    lost = False
    lost_count = 0
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("comicsans", 50)  # Sets the font
    laser_velocity = 25
    player = Player(300, 630)
    enemies = []
    wave_length = 5

    def redraw_window():  # Inner function to redraw window contents. Can only call in main()
        WINDOW.blit(BACKGROUND, (0, 0))  # Draws background onto Window

        # Renders and displays the level and lives text
        lives_label = main_font.render(f"Lives: {lives}", 1, WHITE)
        level_label = main_font.render(f"Level: {level}", 1, WHITE)
        score_label = main_font.render(f"Score: {player.score}", 1, WHITE)
        high_score_label = main_font.render(f"High Score: {high_score}", 1, WHITE)
        WINDOW.blit(lives_label, (10, 10))
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WINDOW.blit(score_label, ((WIDTH / 2) - (score_label.get_width() / 2), 10))
        WINDOW.blit(high_score_label, ((WIDTH / 2) - (high_score_label.get_width() / 2),
                                       10 + high_score_label.get_height()))

        # Draws all Enemies to the Window
        for enemy in enemies:
            enemy.draw(WINDOW)

        player.draw(WINDOW)  # Draws the Player to the Window

        # Handles if Player loses
        """if lost:
            lost_menu()"""

        pygame.display.update()

    # Main loop
    while run:
        clock.tick(FPS)  # Increments the timer
        redraw_window()

        # Handles making the Player lose if out of lives
        if lives <= 0 or player.health <= 0:
            lost_menu()
            #lost = True
            #lost_count += 1

        """
        # If Player loses, essentially waits 3 seconds and quits game
        if lost:
            if lost_count > FPS * 3:
                update_high_score(player)
                run = False
                # quit()
            else:
                continue
        """

        # Handles if the wave is finished
        if len(enemies) == 0:
            level += 1
            wave_length += 5

            # Spawns new enemies
            for i in range(wave_length):
                # Creates a new enemy based on random x and y position and random colour from a list
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100),
                              random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        # Checks if user has pressed the X button in the window and closes program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                update_high_score(player)
                # run = False
                quit()

        # Player movement
        Functions.move_player(player, WIDTH, HEIGHT)

        # Enemy movement
        lives, enemies = Functions.move_enemies(player, enemies, HEIGHT, laser_velocity, lives)

        # Moves Player Lasers given their velocity and the list of Enemies
        # Velocity must be negative for Lasers to move forward
        player.move_lasers(-laser_velocity, enemies)

    quit()


def update_high_score(player):
    if player.score > high_score:
        with open("HighScore.txt", 'w') as reader:
            reader.write(str(player.score))  # Updates high score in file if necessary
            high_score_menu(player)


def high_score_menu(player):
    run = True
    font = pygame.font.SysFont("comicsans", 60)
    congrats_font = pygame.font.SysFont("comicsans", 80)

    while run:
        WINDOW.blit(BACKGROUND, (0, 0))
        congrats_label = congrats_font.render("CONGRATULATIONS", 1, WHITE)
        high_score_label = font.render(f"HIGH SCORE: {player.score}", 1, WHITE)
        WINDOW.blit(congrats_label, (WIDTH / 2 - congrats_label.get_width() / 2, 350))
        WINDOW.blit(high_score_label, (WIDTH / 2 - high_score_label.get_width() / 2, 450))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main_menu()


def lost_menu():
    lost_font = pygame.font.SysFont("comicsans", 60)  # Sets the font for when Player loses
    run = True

    while run:
        WINDOW.blit(BACKGROUND, (0, 0))
        lost_label = lost_font.render("You Lost!", 1, WHITE)
        WINDOW.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))  # Shows text in centre of screen
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main_menu()

    quit()


def main_menu():
    title_font = pygame.font.SysFont("verdana", 45)
    run = True

    while run:
        WINDOW.blit(BACKGROUND, (0, 0))
        title_label1 = title_font.render("SPACE INVADERS CLONE!", 1, WHITE)
        title_label2 = title_font.render("Press mouse to play", 1, WHITE)

        WINDOW.blit(title_label1, (WIDTH / 2 - title_label1.get_width() / 2, 350))
        WINDOW.blit(title_label2, (WIDTH / 2 - title_label2.get_width() / 2, 450))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    quit()


if __name__ == '__main__':
    main_menu()