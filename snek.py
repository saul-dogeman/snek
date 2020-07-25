import sys
import pygame

vec = pygame.math.Vector2

# print(pygame.__version__)

pygame.init()
pygame.mixer.init()

pygame.display.set_caption('Snek. enhanced edition.')
clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)
main_grey = (32, 32, 32)

# initialize and resolution
collision = False
FPS = 30  # 10

r_width = 1280
r_height = 960

xx = (r_width * 0.5)  # środek ekranu
yy = (r_height * 0.9)  # dół

left_wall: int = 160  # 160 px od lewej krawędzi
right_wall: int = 1120  # tyle px od prawej
up_wall = (0 - 1280, 960)  # niedziałające gówno
down_wall = (0 - 960, 10)

mainscreen = pygame.display.set_mode((r_width, r_height))

# snekimg_rect = snekimg.get_rect()
# snekimg_rect.center = (xx, yy)

ev_sprites = pygame.sprite.Group()

snekimg = pygame.image.load('squaresnek.png')


# snek sprite and location
class snek(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rot_speed = 0
        self.speed = 0
        self.speedx = 0
        self.speedy = 0
        self.rot = 0
        self.image = snekimg
        self.org_image = self.image

        self.rect = self.image.get_rect()
        self.vel = vec()
        self.rect.center = (xx, yy)
        self.angle = 0
        self.angle_change = 0

    # def rot_90(self, xx, yy):
    #     orig_rect = snekimg.get_rect()
    #     rot_image = pygame.transform.rotate(self, (xx, yy))
    #     rot_rect = orig_rect.copy()
    #     rot_rect.center = rot_image.get_rect().center
    #     rot_image = rot_image.subsurface(rot_rect).copy()
    #     return rot_image

    def update(self):
        if self.angle_change != 0:
            self.angle += self.angle_change
            self.image = pygame.transform.rotozoom(self.org_image, self.angle, 1)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.angle += self.angle_change
            if self.angle > 360:
                self.angle -= 360
            elif self.angle < 0:
                self.angle += 360

        self.speedx = 0
        self.speedy = 0
        self.angle = 0
        # self.vel = vec()
        # self.rot = (self.rot + self.rot_speed) % 360

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_w] or keystate[pygame.K_UP]:
            self.speedy = 5
            #    self.vel = vec(-Snek_speed, 0).rotate(-self.rot)
        if keystate[pygame.K_s] or keystate[pygame.K_DOWN]:
            #    self.vel = vec(Snek_speed, 0).rotate(-self.rot)
            self.speedy = -5
        if keystate[pygame.K_d] or keystate[pygame.K_RIGHT]:
            #   self.rot_speed = -Snek_rot_speed
            self.speedx = 5
            self.angle_change -= 5
            if self.angle >= 90:
                self.angle_change = 0
        if keystate[pygame.K_a] or keystate[pygame.K_LEFT]:
            #   self.rot_speed = Snek_rot_speed
            self.speedx = -5
            self.angle_change += 5
        self.rect.x += self.speedx
        self.rect.y -= self.speedy

        # collisions
        if self.rect.left < left_wall:
            self.rect.left = left_wall
        if self.rect.right > right_wall:
            self.rect.right = right_wall
        # if self.rect.top > up_wall:
        #     self.rect.top = up_wall
        # if self.rect.bottom < down_wall:
        #     self.rect.bottom = down_wall
        # if pygame.sprite.collide_Rect(Snek, top_wall):
        #    self.speedy = 0


snek = snek()
ev_sprites.add(snek)

# player = pygame.Rect(round(xx), round(yy), 40, 75)
# snek = snekimg_rect.blit(snekimg, (10, 10))

# Loop
while not collision:
    mainscreen.fill(black)
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit(0)

    # things
  
    pygame.draw.rect(mainscreen, main_grey, pygame.Rect(left_wall, 10, 960, 960))
    pygame.draw.rect(mainscreen, black, pygame.Rect(left_wall, 950, 960, 10))
    # pygame.draw.rect(mainscreen, black, pygame.Rect(0, 1280, 960, 10))
    # top_wall = pygame.Rect(0, 1280, 960, 10)
    # pygame.draw.rect(mainscreen, main_grey, player)
    # gamebox = pygame.Rect(160, 10, 960, 960) and pygame.Rect(160, 950, 960, 10)

    # update
    ev_sprites.update()
    ev_sprites.draw(mainscreen)
    pygame.display.flip()

# pygame.display.update()
# pygame.display.flip()

