import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__),'img')

# Colors (R, G, B)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Settings
WIDTH = 480
HEIGHT = 640
FPS = 60
TITLE = "Kenpo Chop"
BGCOLOR = GREEN

############ SPRITES  ############
class Player(pygame.sprite.Sprite):
    # player sprite - moves left/right, shoots
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_image,(50,50))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        # only move if arrow key is pressed
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        # move the sprite
        self.rect.x += self.speedx
        # stop at the edges
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def chop(self):
      chop = Chop(self.rect.centerx,self.rect.centery,self.rect.top)
      all_sprites.add(chop)
      attacks.add(chop)
    

class Pad(pygame.sprite.Sprite):
    # Kenpo Pad sprite - spawns above top and moves downward
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-80, -50)
        self.speedy = random.randrange(1, 6)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.y < -80:
            self.rect.y = random.randrange(-80, -50)
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.speedy = random.randrange(1, 6)

    def hit(self):
        self.speedy -= 1
        if self.speedy < -3:
          self.speedy = -3
        self.rect.y -= 20

class Chop(pygame.sprite.Sprite):
    def __init__(self, x, y, t):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(wheel_kick_image,(30,30))
        self.rect = self.image.get_rect()
        self.rect.bottom = t
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if off top of screen
        if self.rect.bottom < 0:
            self.kill()

# initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

player_image = pygame.image.load(path.join(img_dir, 'playerBoy1.png')).convert_alpha()
wheel_kick_image = pygame.image.load(path.join(img_dir, 'wheelKick.png')).convert_alpha()

# set up new game
all_sprites = pygame.sprite.Group()
pads = pygame.sprite.Group()
attacks = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

pad = Pad()
all_sprites.add(pad)
pads.add(pad)

running = True
while running:
    clock.tick(FPS)
    # check for events
    for event in pygame.event.get():
        # this one checks for the window being closed
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.chop()

    ##### Game logic goes here  #########
    all_sprites.update()
    # check if attacks hit pads
    padHits = pygame.sprite.groupcollide(pads, attacks, False, True)
    for padSprite, attackSprites in padHits.items():
      if len(attackSprites) != 0:
        padSprite.hit()
    # check if pads hit player
    hits = pygame.sprite.spritecollide(player, pads, False)
    if hits:
        running = False

    ##### Draw/update screen #########
    screen.fill(BGCOLOR)
    all_sprites.draw(screen)
    # after drawing, flip the display
    pygame.display.flip()
