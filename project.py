import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Custom event IDs
SPRITE_COLOR_CHANGE_EVENT = pygame.USEREVENT + 1
BACKGROUND_COLOR_CHANGE_EVENT = pygame.USEREVENT + 2

# Colors
BLUE = pygame.Color('blue')
LIGHTBLUE = pygame.Color('lightblue')
DARKBLUE = pygame.Color('darkblue')
YELLOW = pygame.Color('yellow')
MAGENTA = pygame.Color('magenta')
ORANGE = pygame.Color('orange')
WHITE = pygame.Color('white')
RED = pygame.Color('red')

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Sprite class
class MovingSprite(pygame.sprite.Sprite):
    def __init__(self, color, height, width, auto_move=False):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.auto_move = auto_move
        self.velocity = [random.choice([-3, 3]), random.choice([-3, 3])] if auto_move else [0, 0]

    def update(self):
        if self.auto_move:
            self.rect.move_ip(self.velocity)
            boundary_hit = False
            if self.rect.left <= 0 or self.rect.right >= WIDTH:
                self.velocity[0] = -self.velocity[0]
                boundary_hit = True
            if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
                self.velocity[1] = -self.velocity[1]
                boundary_hit = True
            if boundary_hit:
                pygame.event.post(pygame.event.Event(SPRITE_COLOR_CHANGE_EVENT))
                pygame.event.post(pygame.event.Event(BACKGROUND_COLOR_CHANGE_EVENT))

    def change_color(self):
        self.image.fill(random.choice([YELLOW, MAGENTA, ORANGE, WHITE]))

# Background color control
def change_background_color():
    global bg_color
    bg_color = random.choice([BLUE, LIGHTBLUE, DARKBLUE])

# Create sprite group
all_sprites = pygame.sprite.Group()

# Create controlled sprite
player = MovingSprite(RED, 60, 60, auto_move=False)
player.rect.x, player.rect.y = 100, 100

# Create auto-moving sprite
enemy = MovingSprite(WHITE, 50, 50, auto_move=True)
enemy.rect.x, enemy.rect.y = 400, 300

all_sprites.add(player, enemy)

# Game variables
bg_color = BLUE
speed = 5
clock = pygame.time.Clock()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == SPRITE_COLOR_CHANGE_EVENT:
            enemy.change_color()
        elif event.type == BACKGROUND_COLOR_CHANGE_EVENT:
            change_background_color()



    # Boundary check for player
    player.rect.x = max(0, min(player.rect.x, WIDTH - player.rect.width))
    player.rect.y = max(0, min(player.rect.y, HEIGHT - player.rect.height))

    # Update sprites
    all_sprites.update()

    # Draw everything
    screen.fill(bg_color)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(120)
