# initialize
import sys
import pygame
from pygame import sprite
import random

pygame.init()
pygame.mixer.init()

pygame.display.set_caption('Snek. normal edition.')
clock = pygame.time.Clock()

# colors
white = (255, 255, 255)
black = (0, 0, 0)
main_grey = (32, 32, 32)

# resolution, positions
collision = False
FPS = 30
score = 0

xx = 640  # round(r_width * 0.5)  # środek ekranu
yy = 890  # round(r_height * 0.9) # dół
r_width = 1280
r_height = 990
left_wall: int = 160
right_wall: int = 1120

mainscreen = pygame.display.set_mode((r_width, r_height))
mainscreencenter = (round(r_width * 0.3), round(r_height * 0.3))
arena = pygame.Rect(left_wall, 10, 960, 960)

# images + rect
snekimg = pygame.image.load('squaresnek.png').convert_alpha()
background_image = pygame.image.load("background.jpg").convert()
endscreen1 = pygame.image.load("niewiemstary.jpg").convert()
endscreen2 = pygame.image.load("endscreen2.jpg").convert()
ambrosia_food = pygame.image.load("ambrosia_food.png").convert_alpha()
snekbodytype = pygame.image.load("snekbody.png").convert_alpha()

snekimg_rect = snekimg.get_rect()
endscreen_rect = endscreen1.get_rect()
bg_rect = background_image.get_rect()
arena.center = bg_rect.center
endscreen_rect.center = arena.center

# sprites group
ev_sprites = pygame.sprite.Group()

# parts of full body / lista lista
all_of_sneks = []


# CLASS AMBROSIA (FOOD)
class AmbrosiaFood(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ambrosia_food
        self.sprite = sprite
        self.rect_y = random.randrange(15, 930)
        self.rect_x = random.randrange(left_wall + 40, right_wall - 40)
        self.rect = self.image.get_rect(center=(self.rect_x * 0.5, self.rect_y * 0.5))
        self.position = (self.rect_x, self.rect_y)

    def randomposition(self):
        self.rect_y = random.randrange(15, 930)
        self.rect_x = random.randrange(left_wall, right_wall)
        self.rect = self.image.get_rect()
        self.position = (self.rect_x, self.rect_y)

    def showup(self):
        mainscreen.blit(self.image, (self.rect_x, self.rect_y))

    def update(self):
        self.rect = self.image.get_rect(center=(self.rect_x * 0.5, self.rect_y * 0.5))
        self.rect.inflate_ip(-25, -25)


# CLASS SNEK
class Snek(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = snekimg
        self.sprite = pygame.sprite.Sprite()
        self.sprite = sprite
        self.length = 1

        self.direction = "up"
        self.x_position = xx
        self.y_position = yy
        self.x = 0
        self.y = 0
        self.rect = self.image.get_rect(center=(self.x_position * 0.5, self.y_position * 0.5))

    def showup(self):
        mainscreen.blit(self.image, (snek.x_position, snek.y_position))

    def update(self):
        self.rect = self.image.get_rect(center=(self.x_position * 0.5, self.y_position * 0.5))
        self.rect.inflate_ip(-25, -25)
        # pygame.draw.rect(self.image, white, self.rect) #debugfeature

    def movement(self):
        self.y_position += self.y
        self.x_position += self.x

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_w] or keystate[pygame.K_UP]:
            self.x = 0
            self.y = -5
            self.direction = "up"
            self.image = snekimg
            # self.rect.move_ip(0, -1)

        if keystate[pygame.K_d] or keystate[pygame.K_RIGHT]:
            self.x = 5
            self.y = 0
            self.direction = "right"
            self.image = pygame.transform.rotate(snekimg, 270)
            # self.rect.move_ip(1, 0)

        if keystate[pygame.K_a] or keystate[pygame.K_LEFT]:
            self.x = -5
            self.y = 0
            self.direction = "left"
            self.image = pygame.transform.rotate(snekimg, 90)
            # self.rect.move_ip(-1, 0)

        if keystate[pygame.K_s] or keystate[pygame.K_DOWN]:
            self.x = 0
            self.y = 5
            self.direction = "down"
            self.image = pygame.transform.rotate(snekimg, 180)
            # self.rect.move_ip(0, 1)

    def collision(self):
        keystate = pygame.key.get_pressed()

        if not self.x_position >= left_wall or self.x_position >= (right_wall - 47):
            mainscreen.blit(endscreen1, mainscreencenter)

        elif not self.y_position >= 15 or self.y_position >= 930:
            mainscreen.blit(endscreen1, mainscreencenter)

        elif keystate[pygame.K_ESCAPE]:
            mainscreen.blit(endscreen2, mainscreencenter)


class SnekBody(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = snekbodytype
        self.rect = self.image.get_rect
        self.sprite = sprite
        # self.rect_x = 0
        # self.rect_y = 0
        self.rect_x = snek.x_position
        self.rect_y = snek.y_position
        self.position = (self.rect_x, self.rect_y)

    def showup(self):
        self.rect_x = snek.x_position
        self.rect_y = snek.y_position

        if snek.direction == "left":
            snek_body.rect_x += 50
            snek_body.rect_y += 0
            snek_body.rect = snek_body.image.get_rect(center=(snek_body.rect_x * 0.5, snek_body.rect_y * 0.5))
            snek_body.rect.inflate_ip(-25, -25)
            mainscreen.blit(snek_body.image, (snek_body.rect_x, snek_body.rect_y))

    def update(self):
        self.rect = self.image.get_rect(center=(self.rect_x * 0.5, self.rect_y * 0.5))
        self.rect.inflate_ip(-25, -25)


snek = Snek()
snek_body = SnekBody()
ambrosia_food_obj = AmbrosiaFood()

ev_sprites.add(snek_body, snek, ambrosia_food_obj)

# Loop
while snek.collision:
    mainscreen.fill(black)
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.time.wait(500)
            sys.exit(0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.time.delay(500)
            sys.exit(0)

    if pygame.Rect(snek.rect).colliderect(ambrosia_food_obj.rect):
        print("+1 byczq")
        snek.length += 1
        score += 1
        ambrosia_food_obj.randomposition()
        snek_body.showup()

    elif score == 1:
        print("no to ladnie")

    # if not pygame.Rect(left_wall, 10, 960, 960).contains(snek.rect):
    #     mainscreen.blit(endscreen1, mainscreencenter)

    # świecące prostokąty
    mainscreen.blit(background_image, [0, 0])
    pygame.draw.rect(mainscreen, main_grey, pygame.Rect(arena))

    # update
    ev_sprites.update()
    # ev_sprites.draw(mainscreen)
    ambrosia_food_obj.showup()
    snek.showup()
    snek.movement()
    snek.update()
    # snek_body.showup()
    snek_body.update()
    ambrosia_food_obj.update()
    snek.collision()
    pygame.display.flip()
