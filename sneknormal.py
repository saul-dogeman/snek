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
speed = 10

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


# CLASS AMBROSIA (FOOD)
class AmbrosiaFood(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ambrosia_food
        self.sprite = sprite
        self.rect_y = random.randrange(15, 930)
        self.rect_x = random.randrange(left_wall + 40, right_wall - 40)
        self.rect = self.image.get_rect(center=(self.rect_x // 2, self.rect_y // 2))
        self.position = [self.rect_x, self.rect_y]
        self.ambrosia_spawn = True

    def randomposition(self):
        self.rect_y = random.randrange(15, 930)
        self.rect_x = random.randrange(left_wall, right_wall)
        self.rect = self.image.get_rect()
        self.position = [self.rect_x, self.rect_y]
        self.ambrosia_spawn = True

    def showup(self):
        mainscreen.blit(self.image, (self.rect_x, self.rect_y))

    def update(self):
        self.rect = self.image.get_rect(center=(self.rect_x // 2, self.rect_y // 2))
        self.rect.inflate_ip(-25, -25)


# CLASS SNEK
class Snek(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = snekimg
        self.sprite = pygame.sprite.Sprite()
        self.sprite = sprite
        self.length = 10

        self.direction = "up"
        self.x_position = xx
        self.y_position = yy
        self.x = 0
        self.y = 0
        self.rect = self.image.get_rect(center=(self.x_position // 2, self.y_position // 2))
        self.position = [self.x_position, self.y_position]

    def showup(self):
        mainscreen.blit(snek.image, (snek.x_position, snek.y_position))

    def movement(self):
        self.y_position += self.y
        self.x_position += self.x

        keystate = pygame.key.get_pressed()
        if snek.direction != "down" and keystate[pygame.K_w] or keystate[pygame.K_UP]:
            self.x = 0
            self.y = -speed
            # snek.y_position[1] -= speed
            self.direction = "up"
            self.image = snekimg
            # self.rect.move_ip(0, -1)

        if snek.direction != "left" and keystate[pygame.K_d] or keystate[pygame.K_RIGHT]:
            self.x = speed
            self.y = 0
            # snek.position[0] += speed
            self.direction = "right"
            self.image = pygame.transform.rotate(snekimg, 270)
            # self.rect.move_ip(1, 0)

        if snek.direction != "right" and keystate[pygame.K_a] or keystate[pygame.K_LEFT]:
            self.x = -speed
            self.y = 0
            # snek.position[0] -= speed
            self.direction = "left"
            self.image = pygame.transform.rotate(snekimg, 90)
            # self.rect.move_ip(-1, 0)

        if snek.direction != "up" and keystate[pygame.K_s] or keystate[pygame.K_DOWN]:
            self.x = 0
            self.y = speed
            # snek.position[1] += speed
            self.direction = "down"
            self.image = pygame.transform.rotate(snekimg, 180)
            # self.rect.move_ip(0, 1)

    def update(self):
        self.position = [self.x_position // 2, self.y_position // 2]
        self.rect = self.image.get_rect(center=(self.x_position // 2, self.y_position // 2))
        self.rect.inflate_ip(-25, -25)
        # pygame.draw.rect(self.image, white, self.rect) #debugfeature
        # self.set_body()

    # def set_body(self):
    #     all_of_sneks.insert(0, list(snek.position))
    #     if snek.position[0] == ambrosia_food_obj.position[0] and snek.position[1] == ambrosia_food_obj.position[1]:
    #         print("essa")
    #         score += 1
    #         snek.length += 1
    #         ambrosia_food_obj.ambrosia_spawn = False
    #     else:
    #         print("essa2")
    #         all_of_sneks.pop()
    #     # print(self.all_of_sneks)
    #
    #     if not ambrosia_food_obj.ambrosia_spawn:
    #         ambrosia_food_obj.randomposition()

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
        self.rect_x = 0
        self.rect_y = 0
        self.position = (self.rect_x, self.rect_y)

    def showup(self):
        for XnY in all_of_sneks:
            mainscreen.blit(snek_body.image, (XnY[0], XnY[1]))
            self.rect = snek_body.image.get_rect(center=(snek_body.rect_x // 2, snek_body.rect_y // 2))
            self.rect.inflate_ip(-25, -25)

        # for XnY in all_of_sneks:
        #     if snek.direction == "left":
        #         self.rect = snek_body.image.get_rect(center=(snek_body.rect_x // 2, snek_body.rect_y // 2))
        #         self.rect.inflate_ip(-25, -25)
        #         mainscreen.blit(snek_body.image, ((XnY[0] + 50), XnY[1]))
        #
        #     elif snek.direction == "right":
        #         self.rect = snek_body.image.get_rect(center=(snek_body.rect_x // 2, snek_body.rect_y // 2))
        #         self.rect.inflate_ip(-25, -25)
        #         mainscreen.blit(snek_body.image, (XnY[0] - 50), (XnY[1]))
        #
        #     elif snek.direction == "up":
        #         self.rect = snek_body.image.get_rect(center=(snek_body.rect_x // 2, snek_body.rect_y // 2))
        #         self.rect.inflate_ip(-25, -25)
        #         mainscreen.blit(snek_body.image, (XnY[0], (XnY[1] + 50)))
        #
        #     elif snek.direction == "down":
        #         self.rect = snek_body.image.get_rect(center=(snek_body.rect_x // 2, snek_body.rect_y // 2))
        #         self.rect.inflate_ip(-25, -25)
        #         mainscreen.blit(snek_body.image, (XnY[0], (XnY[1] - 50)))

    def update(self):
        self.rect = self.image.get_rect(center=(self.rect_x // 2, self.rect_y // 2))
        self.rect.inflate_ip(-25, -25)


snek = Snek()
snek_body = SnekBody()
ambrosia_food_obj = AmbrosiaFood()
all_of_sneks = []

ev_sprites.add(snek_body, snek, ambrosia_food_obj)
# Loop
while snek.collision:
    mainscreen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.time.wait(500)
            sys.exit(0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.time.delay(500)
            sys.exit(0)


    snekleb = []
    snekleb.append(snek.x_position)     # - snek.x
    snekleb.append(snek.y_position)     # - snek.y
    all_of_sneks.append(snekleb)

    if len(all_of_sneks) > snek.length:
        del all_of_sneks[0]
    for eachSegment in all_of_sneks:
        collision = True

    if pygame.Rect(snek.rect).colliderect(ambrosia_food_obj.rect):
        print("essa dziala")
        ambrosia_food_obj.randomposition()
        snek.length += 5
        score += 1

    # świecące prostokąty
    mainscreen.blit(background_image, [0, 0])
    pygame.draw.rect(mainscreen, main_grey, pygame.Rect(arena))
    snek_body.showup()
    snek_body.update()

    ev_sprites.update()
    # ev_sprites.draw(mainscreen)

    snek.showup()
    snek.movement()
    snek.update()

    ambrosia_food_obj.showup()
    ambrosia_food_obj.update()

    snek.collision()
    pygame.display.flip()
    clock.tick(FPS)
