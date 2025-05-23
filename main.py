import pygame  #2:57 Drawing
from os.path import join  # can avoid using / or \ when importing from filepath

from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.original_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.image = self.original_surf
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 325

        #cooldwon
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

        #mask
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks() # runs continuously
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot: # only triggered once
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()

        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))
class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0: # bottom of laser rect
            self.kill() # gets rid of sprite after it goes off-screen, removes sprite from all groups
class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf = surf.convert_alpha()
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)# meteor generated at random x position
        self.speed = randint(400, 500)
        self.rotation_speed = randint(40, 80)
        self.rotation = 0

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center=self.rect.center)
        # creates a new rect with the same center pos as the last rect

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=pos)

    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames): #if the frame_index is less then total frames
            self.image = self.frames[int(self.frame_index)] #keep playing the animation
        else:
            self.kill()


def collisions():
    global running

    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collision_sprites:  # pygame.sprite.collide_mask is applied to all sprites
        running = False

    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            explosion_sound.play()
            explosion_sound.set_volume(0.1)


def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(str(current_time), True, (240, 240, 240)) #str converts ticks to string
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    pygame.draw.rect(display_surface, (240, 240, 240), text_rect.inflate(20, 10).move(0, -7), 5, 6)
    display_surface.blit(text_surf, text_rect)

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # main surface, only one, always visible canvas!
pygame.display.set_caption('Space Shooter')
running = True
clock = pygame.time.Clock() #clock object, control frame rate

# Imports
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 35)# none is default font
explosion_frames = [pygame.image.load(join('images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]
print(explosion_frames) #for loop iterates over explosion images up to 21

laser_sound = pygame.mixer.Sound(join('audio', 'laser.wav'))
laser_sound.set_volume(0.1)
explosion_sound = pygame.mixer.Sound(join('audio', 'explosion.wav'))
damage_sound = pygame.mixer.Sound(join('audio', 'damage.ogg'))
game_music = pygame.mixer.Sound(join('audio', 'game_music.wav'))
game_music.play(loops=1)
game_music.set_volume(0.1)


# Sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

for i in range(20):
    Star(all_sprites, star_surf) #imports the star surf only once, more efficient
player = Player(all_sprites)

# Custom events - meteor event, timer triggers 2x/1s and creates meteor
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:  # main game loop
    dt = clock.tick()/1000
    # event loop
    for event in pygame.event.get():  # check for user input, keystroke or mouse click
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == meteor_event:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor(meteor_surf, (x,y), (all_sprites, meteor_sprites)) # Creates new meteor objects from Meteor class and add them so sprite groups

    # update
    all_sprites.update(dt)
    collisions()

    # draw the game
    display_surface.fill('#3a2e3f')  # order of surfaces matters
    display_score()
    all_sprites.draw(display_surface)

    # Draw Test

    pygame.display.update()#draws all the elements in while loop on display surface

pygame.quit()
