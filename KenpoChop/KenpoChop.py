import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__),'img')
snd_dir = path.join(path.dirname(__file__),'snd')

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

def draw_text(text, size, x, y):
  # generic function to draw some text
  font_name = pygame.font.match_font('arial')
  font = pygame.font.Font(font_name, size)
  text_surface = font.render(text, True, WHITE)
  text_rect = text_surface.get_rect()
  text_rect.midtop = (x,y)
  screen.blit(text_surface,text_rect)

def draw_health_bar(x, y, pct):
  if pct < 0:
    pct = 0
  BAR_LENGTH = 100
  BAR_HEIGHT = 10
  fill = (pct / 100.0) * BAR_LENGTH
  outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
  fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
  pygame.draw.rect(screen, GREEN, fill_rect)
  pygame.draw.rect(screen, WHITE, outline_rect, 2)
  
  

############ SPRITES  #############
class Player(pygame.sprite.Sprite):
    # player sprite - moves left/right, shoots
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_image,(50,100))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.health = 100

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

    def attack(self):
      attack = Attack(self.rect.centerx,self.rect.centery,self.rect.top)
      all_sprites.add(attack)
      attacks.add(attack)
    

class Opponent(pygame.sprite.Sprite):
    # Kenpo Opponent sprite - spawns above top and moves downward
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(badguy_image,(50,100))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SIDEPAD, (WIDTH - SIDEPAD) - self.rect.width)
        self.rect.y = random.randrange(-80, -50)
        self.speedy = random.randrange(1, 6)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10: ## Fall off screen
          self.rect.x = random.randrange(SIDEPAD, (WIDTH - SIDEPAD) - self.rect.width)
          self.rect.y = random.randrange(-80, -50)
        if self.rect.y < -80: ## Pushed off screen
          self.kill()

    def hit(self):
        self.speedy -= 1
        if self.speedy < -3:
          self.speedy = -3
        self.rect.y -= 20
        uff_sound.play()

class Attack(pygame.sprite.Sprite):
    def __init__(self, x, y, t):
        pygame.sprite.Sprite.__init__(self)
        (self.image0,self.hasRotation, self.rotationSpeeds,self.sound) = random.choice( attacks_pydata )
        self.sound.play()
        self.image = self.image0.copy()
        self.rect = self.image.get_rect()
        self.rect.bottom = t
        self.rect.centerx = x
        self.speedy = -3
        self.rot = 0
        self.rot_speed = 0
        if self.hasRotation:
          self.rot_speed = random.choice(self.rotationSpeeds)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
      if self.hasRotation:
        now = pygame.time.get_ticks()
        ticks_since_update = now - self.last_update
        if ticks_since_update > 50:
          self.last_update = now
          self.rot = (self.rot + self.rot_speed ) % 360
          new_image = pygame.transform.rotate(self.image0,self.rot)
          old_center = self.rect.center
          self.image = new_image
          self.rect = self.image.get_rect()
          self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        # kill if off top of screen
        if self.rect.bottom < 0:
            self.kill()

# initialize pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

player_image = pygame.image.load(path.join(img_dir, 'playerBoy1.png')).convert_alpha()
badguy_image = pygame.image.load(path.join(img_dir, 'kenpoPlayerRectangle.png')).convert_alpha()


attacks = [] ## (               imageFile, rotateAttack, [rotationSpeeds],     soundFile)
attacks.append( (        'wheelKick1.png',         True,           [-8,8], 'LukeKia.wav') )
attacks.append( (        'hammerFist.png',        False,               [], 'EvieKia.wav') )
attacks.append( ('sparklyUnicornKick.png',        False,               [],  'MomKia.wav') )

attacks_pydata = []
for ( imgFile, rotateAttack, rotateSpeeds, sndFile ) in attacks:
  attacks_pydata.append( (pygame.image.load(path.join(img_dir,imgFile)).convert_alpha(), 
                          rotateAttack, 
                          rotateSpeeds,
                          pygame.mixer.Sound(path.join(snd_dir,sndFile)) ) )

dojo_image = pygame.image.load(path.join(img_dir, 'dojoFloorTextured.png')).convert_alpha()
dojo_rect = dojo_image.get_rect()

## Sounds
uff_sound = pygame.mixer.Sound(path.join(snd_dir,'Uff.wav'))


# set up new game
score = 0
all_sprites = pygame.sprite.Group()
opponents = pygame.sprite.Group()
attacks = pygame.sprite.Group()

player = Player()
all_sprites.add(player)


opponent = Opponent()
all_sprites.add(opponent)
opponents.add(opponent)

old_num_opponents = len(opponents)
new_num_opponents = len(opponents)

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
                player.attack()

    ##### Game logic goes here  #########
    all_sprites.update()
    # check if attacks hit opponents
    opponentHits = pygame.sprite.groupcollide(opponents, attacks, False, True)
    for opponentSprite, attackSprites in opponentHits.items():
      if len(attackSprites) != 0:
        opponentSprite.hit()
    # score killed opponents
    new_num_opponents = len(opponents)
    if new_num_opponents < old_num_opponents:
      score += ( old_num_opponents - new_num_opponents )
    if new_num_opponents == 0:
      opponent = Opponent()
      all_sprites.add(opponent)
      opponents.add(opponent)
    old_num_opponents = len(opponents)
    # check if opponents hit player
    hits = pygame.sprite.spritecollide(player, opponents, False)
    for opponent in hits:
      player.health -= 20
      opponent.kill()
      if player.health <= 0:
        running = False

    ##### Draw/update screen #########
    screen.fill(BGCOLOR)
    screen.blit(dojo_image,dojo_rect)
    all_sprites.draw(screen)
    score_text = str(score)
    draw_text(score_text, 18, WIDTH / 2, 10 )
    draw_health_bar(5, 5, player.health)
    # after drawing, flip the display
    pygame.display.flip()
