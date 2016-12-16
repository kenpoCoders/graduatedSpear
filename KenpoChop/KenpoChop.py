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
SIDEPAD = 20
FPS = 60
TITLE = "Kenpo Chop"
BGCOLOR = GREEN

############ SPRITES  ############
class Player(pygame.sprite.Sprite):
    # player sprite - moves left/right, shoots
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_image,(50,100))
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
        if self.rect.right > (WIDTH - SIDEPAD):
            self.rect.right = (WIDTH - SIDEPAD)
        if self.rect.left < (SIDEPAD):
            self.rect.left = SIDEPAD

    def chop(self):
      chop = Chop(self.rect.centerx,self.rect.centery,self.rect.top)
      all_sprites.add(chop)
      attacks.add(chop)
    

class Pad(pygame.sprite.Sprite):
    # Kenpo Pad sprite - spawns above top and moves downward
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(badguy_image,(50,100))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SIDEPAD, (WIDTH - SIDEPAD) - self.rect.width)
        self.rect.y = random.randrange(-80, -50)
        self.speedy = random.randrange(1, 6)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.y < -80:
            self.rect.y = random.randrange(-80, -50)
            self.rect.x = random.randrange(SIDEPAD, (WIDTH - SIDEPAD) - self.rect.width)
            self.speedy = random.randrange(1, 6)

    def hit(self):
        self.speedy -= 1
        if self.speedy < -3:
          self.speedy = -3
        self.rect.y -= 20

class Chop(pygame.sprite.Sprite):
    def __init__(self, x, y, t):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice( attack_images )
        self.rect = self.image.get_rect()
        self.rect.bottom = t
        self.rect.centerx = x
        self.speedy = -3

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
badguy_image = pygame.image.load(path.join(img_dir, 'kenpoPlayerRectangle.png')).convert_alpha()

attack_images = []
attack_images.append( pygame.image.load(path.join(img_dir, 'wheelKick1.png')).convert_alpha() )
attack_images.append( pygame.image.load(path.join(img_dir, 'hammerFist.png')).convert_alpha() )
attack_images.append( pygame.image.load(path.join(img_dir, 'sparklyUnicornKick.png')).convert_alpha() )

dojo_image = pygame.image.load(path.join(img_dir, 'dojoFloorTextured.png')).convert_alpha()
dojo_rect = dojo_image.get_rect()

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
    screen.blit(dojo_image,dojo_rect)
    all_sprites.draw(screen)
    # after drawing, flip the display
    pygame.display.flip()
