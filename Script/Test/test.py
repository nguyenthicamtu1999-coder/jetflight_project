import pygame
import random
import math

# =====================================================
# CONFIGURATION
# =====================================================

WIDTH, HEIGHT = 800, 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Voyage Interstellaire")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

# =====================================================
# CHARGEMENT ET SCALE DES IMAGES
# =====================================================

ship_img = pygame.image.load("../../Image/vaisseau.png").convert_alpha()
ship_img = pygame.transform.scale(ship_img, (60, 60))

asteroid_img = pygame.image.load("../../Image/asteroid.png").convert_alpha()
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))

solar_img = pygame.image.load("../../Image/solareflare.png").convert_alpha()
solar_img = pygame.transform.scale(solar_img, (160, 50))

bg_img = pygame.image.load("../../Image/background.png").convert()
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

# =====================================================
# CLASSES
# =====================================================

class Spaceship:
    def __init__(self):
        self.x = 120
        self.y = HEIGHT // 2
        self.speed = 5
        self.radius = ship_img.get_width() // 2
        self.max_energy = 100
        self.energy = 100

    def move(self, keys):
        if keys[pygame.K_UP]: self.y -= self.speed
        if keys[pygame.K_DOWN]: self.y += self.speed
        if keys[pygame.K_LEFT]: self.x -= self.speed
        if keys[pygame.K_RIGHT]: self.x += self.speed
        self.x = max(0, min(WIDTH, self.x))
        self.y = max(0, min(HEIGHT, self.y))

    def take_damage(self, amount):
        self.energy = max(0, self.energy - amount)

    def draw(self):
        rect = ship_img.get_rect(center=(self.x, self.y))
        screen.blit(ship_img, rect)

    def draw_energy(self):
        pygame.draw.rect(screen, (255, 0, 0), (20, 20, 200, 15))
        pygame.draw.rect(
            screen, (0, 255, 0),
            (20, 20, 200 * (self.energy / self.max_energy), 15)
        )

class Asteroid:
    def __init__(self):
        self.x = WIDTH + random.randint(0, 300)
        self.y = random.randint(80, HEIGHT - 80)
        self.speed = random.randint(3, 6)
        self.radius = asteroid_img.get_width() // 2

    def update(self):
        self.x -= self.speed

    def draw(self):
        rect = asteroid_img.get_rect(center=(self.x, self.y))
        screen.blit(asteroid_img, rect)

    def offscreen(self):
        return self.x < -50

    def collide(self, ship):
        return math.hypot(self.x - ship.x, self.y - ship.y) < self.radius + ship.radius

class Laser:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        self.radius = 5

    def update(self):
        self.x += self.speed

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), self.radius)

    def offscreen(self):
        return self.x > WIDTH

class SolarFlare:
    def __init__(self):
        self.x = WIDTH
        self.y = random.randint(100, HEIGHT - 100)
        self.width = 160
        self.height = 50
        self.speed = 3
        self.active = True

    def update(self):
        self.x -= self.speed
        if self.x < -self.width:
            self.active = False

    def draw(self):
        screen.blit(solar_img, (self.x, self.y))

    def collide(self, ship):
        return self.x < ship.x < self.x + self.width and self.y < ship.y < self.y + self.height

# =====================================================
# INITIALISATION
# =====================================================

ship = Spaceship()
asteroids = []
lasers = []
solar_flares = []
score = 0

# =====================================================
# BOUCLE PRINCIPALE
# =====================================================

running = True
while running:
    clock.tick(FPS)
    screen.blit(bg_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    ship.move(keys)

    # LASER (SPACE)
    if keys[pygame.K_SPACE] and len(lasers) < 5:
        lasers.append(Laser(ship.x + 30, ship.y))

    # ASTEROIDS
    if random.random() < 0.02:
        asteroids.append(Asteroid())

    for a in asteroids[:]:
        a.update()
        a.draw()

        if a.collide(ship):
            ship.take_damage(20)
            asteroids.remove(a)
            score -= 5

        elif a.offscreen():
            asteroids.remove(a)

    # LASERS
    for l in lasers[:]:
        l.update()
        l.draw()

        for a in asteroids[:]:
            if math.hypot(a.x - l.x, a.y - l.y) < a.radius:
                asteroids.remove(a)
                lasers.remove(l)
                score += 10
                break

        if l.offscreen():
            lasers.remove(l)

    # SOLAR FLARES
    if random.random() < 0.005:
        solar_flares.append(SolarFlare())

    for s in solar_flares[:]:
        s.update()
        s.draw()
        if s.collide(ship):
            ship.take_damage(2)
        if not s.active:
            solar_flares.remove(s)

    # GAME OVER
    if ship.energy <= 0:
        running = False

    # HUD
    ship.draw()
    ship.draw_energy()
    score_text = font.render(f"Score : {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 45))

    pygame.display.flip()

pygame.quit()
