
import pygame
from random import randint

#SOUS-PROGRAMME

def CreateTopPath(startPos, steps, padding, surfaceHeight, surfaceWidth, roughness):
    pointsList = [startPos]
    spacing = int(surfaceWidth/steps)

    for i in range(1, steps+1):
        x = pointsList[i-1][0] + spacing
        y = int(pointsList[i-1][1] + randint(-pointsList[i-1][1] + padding, surfaceHeight - padding - pointsList[i-1][1]) * roughness)
        pointsList.append((x, y))

    return pointsList

def CreateBottomPath(startPos, topPath, minThickness, maxThickness, roughness):
    pointList = [startPos]

    for i in range(1,len(topPath)):
        pointList.append((topPath[i][0], topPath[i][1] + randint(minThickness, minThickness + int(maxThickness * roughness))))

    return pointList

def CreateNewSurface(w, h, position, imageString):
    newSurface = pygame.image.load(imageString).convert()
    newSurface = pygame.transform.scale(newSurface, (w, h))
    newRect = newSurface.get_rect(midleft = position)
    return newSurface, newRect

def CreateNewTile(width, height, position, imageStr):
    newSurface = CreateNewSurface(width,height,position,imageStr)
    return {
        'SURFACE': newSurface[0],
        'RECT': newSurface[1],
        'INIT':False,
        'TUNNEL_TOP_LIST':[],
        'TUNNEL_BOTTOM_LIST':[]
    }

#INITIAL GAME

SCREEN_WIDTH=800
SCREEN_HEIGHT=600

pygame.init()
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption("Voyages interstellaire")

#FONT
test_font = pygame.font.Font('../../Font/pixeltype/Pixeltype.ttf', 50)


#Vaisseau
SHIP_WIDTH = 50
SHIP_HEIGHT = 50
SHIP_SURFACE_SPEED = 5
ship_x = (SCREEN_WIDTH // 2) - 320
ship_y = (SCREEN_HEIGHT//2)-(SHIP_HEIGHT//2)
#ship_surface = pygame.Surface((SHIP_WIDTH,SHIP_HEIGHT))
#IMAGE VAISSEAU
ship_img = pygame.image.load("../../Image/vaisseau.png").convert_alpha()
ship_img = pygame.transform.scale(ship_img, (SHIP_WIDTH,SHIP_HEIGHT))
rectangle_ship = ship_img.get_rect(midleft = (ship_x,ship_y))

#Surface
SURFACE_HEIGHT = SCREEN_HEIGHT*3
tilePadding = SCREEN_HEIGHT//2
SURFACE_WIDTH = SCREEN_WIDTH*2
SURF_SURFACE_SPEED_MIN = 2
SURF_SURFACE_SPEED_MAX = 8
SURFACE_SPEED = 5

#TUNNEL
TUNNEL_TOP_COULEUR = 'Red'
TUNNEL_BOTTOM_COULEUR = 'Blue'
TUNNEL_STEP = 10
TUNNEL_LARGEUR_MIN = 200
TUNNEL_LARGEUR_MAX = 300
TUNNEL_ROUGH = 0.1

tileA = CreateNewTile(SURFACE_WIDTH, SURFACE_HEIGHT, (0,SCREEN_HEIGHT//2), '../../Image/surface.png')
tileB = CreateNewTile(SURFACE_WIDTH, SURFACE_HEIGHT, (SURFACE_WIDTH,SCREEN_HEIGHT//2), '../../Image/surface.png')
tileList = [tileA,tileB]

topPathStart = (0, SURFACE_HEIGHT // 2 - TUNNEL_LARGEUR_MIN // 2)
bottomPathStart = (0, SURFACE_HEIGHT // 2 + TUNNEL_LARGEUR_MIN // 2)

#Obstacle
OBSTACLE_WIDTH = 60
OBSTACLE_HEIGHT = 60
Obstacles = [] #liste qui contients tous les obstacles a l'ecran

asteroid_img = pygame.image.load("../../Image/asteroidd.png").convert_alpha()
asteroid_img = pygame.transform.scale(asteroid_img, (OBSTACLE_WIDTH,OBSTACLE_HEIGHT))
rectangle_obstacle = asteroid_img.get_rect(topleft=(-200, -200))
asteroid_img.set_colorkey((0, 0, 0))

#Obstacles eclat
obstacle_eclat_list = []
DURER_EXPLOTION = 100
asteroid_eclat_img = pygame.image.load("../../Image/asteroid_eclat.png").convert_alpha()
asteroid_eclat_img = pygame.transform.scale(asteroid_eclat_img, (OBSTACLE_WIDTH,OBSTACLE_HEIGHT))
asteroid_eclat_img.set_colorkey((0, 0, 0))

#LASER
LASER_WIDTH = 40
LASER_HEIGHT = 20
LASER_SPEED = 7
laser_surf = pygame.image.load("../../Image/laser.png").convert_alpha()
laser_surf = pygame.transform.scale(laser_surf, (LASER_WIDTH,LASER_HEIGHT))

lasers = []

#lASER BONUS
#Obstacles eclat
laser_bonus_list = []
DURER_LASER_BONUS = 5000

#SCORE
Current_score = 0

#BONUS
BONUS_WIDTH = 40
BONUS_HEIGHT = 40
Bonus_list = [] #liste qui contients tous les bonus a l'ecran

bonus_img = pygame.image.load("../../Image/bonus.png").convert_alpha()
bonus_img = pygame.transform.scale(bonus_img, (BONUS_WIDTH,BONUS_HEIGHT))
rectangle_bonus = bonus_img.get_rect(topleft=(-200, -200))
bonus_img.set_colorkey((0, 0, 0))

#events obstace et bonus
obstacle_event = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_event,1000)

bonus_event = pygame.USEREVENT + 2
pygame.time.set_timer(bonus_event,6000)

running = True
clock = pygame.time.Clock()
while running:
    clock.tick(FPS)

    ####BOUCLE POUR LES EVENTS:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == obstacle_event:
            obstacle_copy = rectangle_obstacle.copy()
            obstacle_copy.x = SCREEN_WIDTH + OBSTACLE_WIDTH
            obstacle_copy.y = randint(SCREEN_HEIGHT//2 - TUNNEL_LARGEUR_MIN//4, SCREEN_HEIGHT//2 + TUNNEL_LARGEUR_MIN//4)
            Obstacles.append(obstacle_copy)

        if event.type == bonus_event:
            bonus_copy = rectangle_bonus.copy()
            bonus_copy.x = SCREEN_WIDTH + BONUS_WIDTH
            bonus_copy.y = randint(SCREEN_HEIGHT//2 - TUNNEL_LARGEUR_MIN//4, SCREEN_HEIGHT//2 + TUNNEL_LARGEUR_MIN//4)
            Bonus_list.append(bonus_copy)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                laser_rect = pygame.Rect(rectangle_ship.centerx,rectangle_ship.centery - LASER_HEIGHT // 2,
                                         LASER_WIDTH,LASER_HEIGHT)
                lasers.append(laser_rect)
        if Current_score < 0:
            running = False

    #CONTROLES DU VAISSEAU:

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and ship_x > 0:
        SURFACE_SPEED -= 0.1
        if SURFACE_SPEED < SURF_SURFACE_SPEED_MIN:
            SURFACE_SPEED = SURF_SURFACE_SPEED_MIN
        # ralentir la vitesse de écran

    if keys[pygame.K_RIGHT] and ship_x + SHIP_WIDTH < SCREEN_WIDTH:
        SURFACE_SPEED += 0.1
        Current_score+=10
        if SURFACE_SPEED > SURF_SURFACE_SPEED_MAX:
            SURFACE_SPEED = SURF_SURFACE_SPEED_MAX
        # accélerer la vitesse de écran

    if keys[pygame.K_UP] and rectangle_ship.top > 0:
        rectangle_ship.y -= SHIP_SURFACE_SPEED

    if keys[pygame.K_DOWN] and rectangle_ship.bottom < SCREEN_HEIGHT:
        rectangle_ship.y += SHIP_SURFACE_SPEED

    for tile in tileList:

        tile['RECT'].x -= SURFACE_SPEED

        if tile['RECT'].left <= -SURFACE_WIDTH or not tile['INIT']:
            tile['SURFACE'].fill((0, 0, 0))  #transparent ancienne tunnel

            topPointList = CreateTopPath(topPathStart, TUNNEL_STEP, tilePadding, SURFACE_HEIGHT, SURFACE_WIDTH, TUNNEL_ROUGH)
            tile['TUNNEL_TOP_LIST']=topPointList
            print(topPointList)
            topPathStart = (0, topPointList[len(topPointList)-1][1])
            pygame.draw.lines(tile['SURFACE'], TUNNEL_TOP_COULEUR, False, topPointList, 2)

            bottomPointList = CreateBottomPath(bottomPathStart, topPointList, TUNNEL_LARGEUR_MIN, TUNNEL_LARGEUR_MAX, TUNNEL_ROUGH)
            tile['TUNNEL_BOTTOM_LIST']=bottomPointList
            print(bottomPointList)
            bottomPathStart = (0, bottomPointList[len(bottomPointList)-1][1])
            pygame.draw.lines(tile['SURFACE'], TUNNEL_BOTTOM_COULEUR, False, bottomPointList, 2)

            if not tile['INIT']:
                tile['INIT'] = True

            elif tile['RECT'].left <= -SURFACE_WIDTH:
                tile['RECT'].x = SURFACE_WIDTH

        screen.blit(tile['SURFACE'],tile['RECT'])

    screen.blit(ship_img, rectangle_ship)

    ###BOUCLE POUR METTRE A JOUR LES OBJECTS:
    for obstacle_rect in Obstacles:
        obstacle_rect.x -= SURFACE_SPEED
        screen.blit(asteroid_img,obstacle_rect)

        if rectangle_ship.colliderect(obstacle_rect):
            running= False

    for bonus_rect in Bonus_list:
        bonus_rect.x -= SURFACE_SPEED
        screen.blit(bonus_img,bonus_rect)

        if rectangle_ship.colliderect(bonus_rect):
            Bonus_list.remove(bonus_rect)
            Current_score += 20

            rectangle_laser_bonus = laser_surf.get_rect(bottomleft=rectangle_ship.topright)
            laser_bonus_list.append({'RECT': rectangle_laser_bonus, 'TIME': pygame.time.get_ticks()})
            rectangle_laser_bonus.x += LASER_SPEED
            screen.blit(laser_surf, rectangle_laser_bonus)

    for laser_rect in lasers:
        laser_rect.x += LASER_SPEED
        screen.blit(laser_surf,laser_rect)

    #BOUCLE POUR SUPPRIMER LES OBJECTS:
    for obstacle_rect in Obstacles:
        if obstacle_rect.x < -OBSTACLE_WIDTH:
            Obstacles.remove(obstacle_rect)

    for bonus_rect in Bonus_list:
        if bonus_rect.x < -BONUS_WIDTH:
            Bonus_list.remove(bonus_rect)

    for laser_rect in lasers:
        if laser_rect.x > SCREEN_WIDTH:
            lasers.remove(laser_rect)
            print(len(lasers))

    #COLLISIONS
    for obstacle_rect in Obstacles:
        for laser_rect in lasers:
            if laser_rect.colliderect(obstacle_rect):
                Obstacles.remove(obstacle_rect)
                lasers.remove(laser_rect)
                Current_score += 50

                #collision laser et obstacle -> eclate
                rectangle_obstacle_eclat = asteroid_eclat_img.get_rect(center = obstacle_rect.center)
                obstacle_eclat_list.append({'RECT':rectangle_obstacle_eclat,'TIME':pygame.time.get_ticks()})
                rectangle_obstacle_eclat.x -= SURFACE_SPEED
                screen.blit(asteroid_eclat_img,rectangle_obstacle_eclat)



    for tile in tileList:
        for i in range(len(tile['TUNNEL_TOP_LIST'])-2):
            if rectangle_ship.clipline(tile['TUNNEL_TOP_LIST'][i],tile['TUNNEL_TOP_LIST'][i+1]):
                Current_score -= 50

        for i in range(len(tile['TUNNEL_BOTTOM_LIST'])-2):
            if rectangle_ship.clipline(tile['TUNNEL_BOTTOM_LIST'][i],tile['TUNNEL_BOTTOM_LIST'][i+1]):
                Current_score -= 50

    screen.blit(ship_img,rectangle_ship)

    SCORE_TEXT = test_font.render(f"SCORE : {Current_score}", True, (255, 255, 255))
    SCORE_RECT = SCORE_TEXT.get_rect(bottomright=(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20))

    screen.blit(SCORE_TEXT, SCORE_RECT)

    #GARDER SEULEMENT CE QUI SONT PAS ENCORE DEPASSER LE TEMPS (ECLATE DE OBSTACLES) ET LASER
    current_time_obstacle = pygame.time.get_ticks()

    NEW_ECLAT = []
    for obstacle_eclat in obstacle_eclat_list:
        timepass_obstacle = current_time_obstacle - obstacle_eclat['TIME']
        if timepass_obstacle <= DURER_EXPLOTION:
            NEW_ECLAT.append(obstacle_eclat)

    obstacle_eclat_list = NEW_ECLAT


    for laser_bonus in laser_bonus_list:
        if pygame.time.get_ticks() - laser_bonus['TIME'] <= DURER_LASER_BONUS:
            laser_bonus_list.remove(laser_bonus)

    # dessiner toutes les explosions restantes
    for obstacle_eclat in obstacle_eclat_list:
        screen.blit(asteroid_eclat_img, obstacle_eclat['RECT'])
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()