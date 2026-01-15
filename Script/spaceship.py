import pygame
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
pygame.init()

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

ship_img = pygame.image.load("../Image/vaisseau.png")
ship_img = pygame.transform.scale(ship_img, (50, 50))
'''asteroid_img = pygame.image.load("asteroid.png").convert_alpha()
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))

solar_img = pygame.image.load("solareflare.png").convert_alpha()
solar_img = pygame.transform.scale(solar_img, (160, 50))

bg_img = pygame.image.load("background.png").convert()
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))'''

class Player:
    def __init__(self):
        self.width = SHIP_WIDTH
        self.height = SHIP_HEIGHT
        self.speed = SHIP_SPEED
        self.image = ship_img
        self.x = (SCREEN_WIDTH // 2) - 320
        self.y = 300
        self.hitbox = pygame.Rect(self.x,self.y,self.width,self.height)
    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and ship.x > 0:
            ship.x -= ship.speed

        if keys[pygame.K_RIGHT] and ship.x + SHIP_WIDTH < SCREEN_WIDTH:
            ship.x += ship.speed

        if keys[pygame.K_UP] and ship.y > 0:
            ship.y -= ship.speed

        if keys[pygame.K_DOWN] and ship.y + SHIP_HEIGHT < SCREEN_HEIGHT:
            ship.y += ship.speed

        self.hitbox.x = self.x
        self.hitbox.y = self.y

#SPACESHIP
SHIP_WIDTH = 50
SHIP_HEIGHT = 50
SHIP_SPEED = 5

ship = Player()

class Obstacle:
    def __init__(self):
        self.width = OBSTACLES_WIDTH
        self.height = OBSTACLES_HEIGHT
        self.speed = OBSTACLES_SPEED
        self.x = SCREEN_WIDTH
        self.y = random.randint(0,SCREEN_HEIGHT - OBSTACLES_HEIGHT)
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.x -= OBSTACLES_SPEED
        if self.x < 0:
            self.x = SCREEN_WIDTH
            self.y = random.randint(0, SCREEN_HEIGHT - OBSTACLES_HEIGHT)
        self.hitbox.x= self.x
        self.hitbox.y= self.y

    def draw(self,screen):
        pygame.draw.rect(screen, BLUE, self.hitbox)


# OBSTACLES
OBSTACLES_WIDTH = 50
OBSTACLES_HEIGHT = 50
OBSTACLES_SPEED = 3
obstacles = []
for i in range(5):
    obstacles.append(Obstacle())

class Laser:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.speed = LASER_SPEED
        self.width = LASER_WIDTH
        self.height = LASER_HEIGHT
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, self.hitbox)

    def update(self):
        self.x += self.speed
        self.hitbox.x = self.x

# LASER
LASER_WIDTH = 10
LASER_HEIGHT = 5
LASER_SPEED = 7
lasers = []


screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption("Voyages interstella")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

ship_surface = pygame.image.load("../Image/vaisseau.png").convert_alpha()
ship_rect = ship_surface.get_rect(midbottom = (50,250))
bg_surface = pygame.image.load("../Image/background.png").convert()
bg_surface = pygame.transform.scale(bg_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                laser_x = ship.x
                laser_y = ship.y + (ship.height//2) - (LASER_HEIGHT//2)
                new_lazer = Laser(laser_x,laser_y)
                lasers.append(new_lazer)

    ship.update()
    for obstacle in obstacles:
        obstacle.update()
    for laser in lasers:
        laser.update()
    for laser in lasers:
        for obstacle in obstacles:
            if laser.hitbox.colliderect(obstacle.hitbox):
                lasers.remove(laser)
                obstacles.remove(obstacle)
                break
    for obstacle in obstacles:
        if ship.hitbox.colliderect(obstacle.hitbox):
            print("GAME OVER")
            running = False
            break


    #Redessin l'écran
    screen.fill(BLACK)
    screen.blit(bg_surface, (0, 0))
    ship.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)

    for laser in lasers:
        laser.draw(screen)


    clock.tick(FPS)


    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()