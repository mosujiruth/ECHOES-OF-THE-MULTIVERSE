import pygame
import sys

pygame.init()
pygame.font.init()

BLACK = (255, 255, 255)
WHITE = (0, 0, 0)
YELLOW = (255, 255, 0)

# Initialize the screen
screen_length = 600
screen_height = 400
window = pygame.display.set_mode((screen_length, screen_height))
pygame.display.set_caption("ECHOES OF THE MULTIVERSE")
font = pygame.font.SysFont('Comic Sans', 48)

# Load images
char_1 = pygame.image.load("iron warrior.png").convert_alpha()
char_2 = pygame.image.load("captainwillie.png").convert_alpha()
char_3 = pygame.image.load("stormbreak.png").convert_alpha()
char_1 = pygame.transform.scale(char_1, (100, 100))
char_2 = pygame.transform.scale(char_2, (100, 100))
char_3 = pygame.transform.scale(char_3, (100, 100))

laser_img = pygame.image.load("laser.jpg").convert_alpha()
laser_img = pygame.transform.scale(laser_img, (20, 10))
laptopshot_img = pygame.image.load("willie sheild.jpg").convert_alpha()
laptopshot_img = pygame.transform.scale(laptopshot_img, (20, 10))
thunder_img = pygame.image.load("thunder.jpg").convert_alpha()
thunder_img = pygame.transform.scale(thunder_img, (20, 10))

enemy_photo = pygame.image.load("blueskull.jpeg").convert_alpha()
enemy_photo = pygame.transform.scale(enemy_photo, (100, 100))

# Define hero images
char_images = {
    "IRON WARRIOR": char_1,
    "CAPTAIN WILLIE": char_2,
    "STORMBREAK": char_3
}
players_healthy = 150
blueskull_healthy = 150
# Hero class
class Heroes:
    def __init__(self, image, bullet_img, bullet_speed, typesof_bullet):
        self.image = image
        self.bullet_img = bullet_img
        self.typesof_bullet = typesof_bullet
        self.bullet_speed = bullet_speed

    def firing_bullettypes(self, x, y):
        return [Bullet(self.bullet_img, x - 80, y - 10, self.bullet_speed)]

    def draw(self, window, x, y):
        window.blit(self.image, (x, y))

# Bullet class
class Bullet:
    def __init__(self, image, x, y, speed):
        self.image = image
        self.x = x
        self.y = y
        self.speed = speed

    def move(self):
        self.x += self.speed

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

# Blueskull class
class Blueskull:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.direction = 1
        self.speed = 0.25

    def move(self):
        self.y += self.direction * self.speed
        if self.y <= 50:
            self.direction = 1
        elif self.y >= screen_height - 150:
            self.direction = -1

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

# Initialize heroes
ironwarrior = Heroes(char_1, laser_img, 3, "laser")
captainwillie = Heroes(char_2, laptopshot_img, 3, "laptopshot")
stormbreak = Heroes(char_3, thunder_img, 3, "thunder")

# Select a hero (for simplicity, we'll use Captain Willie as default)
hero = captainwillie

# Initialize game variables
bullets = []
maximum_bullet = 12
bullet_cooldowntime = 300
last_shot_timimg = pygame.time.get_ticks()
players_x, players_y = 0, screen_height - 120

blueenemy = Blueskull(enemy_photo, 450, 250)

# Main game loop
running = True
while running:
    current_timimg = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if current_timimg - last_shot_timimg > bullet_cooldowntime:
                    if len(bullets) < maximum_bullet:
                        new_bullety = hero.firing_bullettypes(players_x, players_y)
                        bullets.extend(new_bullety)
                        last_shot_timimg = current_timimg

    for bullet in bullets[:]:
        bullet.move()
        if bullet.x > screen_length:
            bullets.remove(bullet)
        elif blueenemy.x < bullet.x < blueenemy.x + 100 and blueenemy.y < bullet.y < blueenemy.y + 100:
            bullets.remove(bullet)
            blueskull_healthy -= 10

    window.fill(BLACK)

    pygame.draw.rect(window, YELLOW, (10, 10, players_healthy, 20))
    pygame.draw.rect(window, YELLOW, (screen_length - blueskull_healthy - 10, 10, blueskull_healthy, 20))

    hero.draw(window, players_x, players_y)

    blueenemy.move()
    blueenemy.draw(window)
    for bullet in bullets:
        bullet.draw(window)

    pygame.display.update()

    if blueskull_healthy <= 0:
        print("Blueskull is defeated")
        running = False
    if players_healthy <= 0:
        print("You are dead")
        running = False

pygame.quit()
sys.exit()
