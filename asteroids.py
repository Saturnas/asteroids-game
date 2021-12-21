from datetime import datetime
import pygame, random, sys
from pygame.locals import *
# Game settings
WINDOWWIDTH = 800
WINDOWHEIGHT = 1000
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 60
asteroidMINSIZE = 15
asteroidMAXSIZE = 60
asteroidMINSPEED = 1
asteroidMAXSPEED = 5
ADDNEWasteroidRATE = 10
PLAYERMOVERATE = 5
now = datetime.now()
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

def terminate():
    pygame.quit()
    sys.exit()

# Game exit and exit with ESC
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: 
                    terminate()
                return

# Player collision with asteroid
def playerHasHitasteroid(playerRect, asteroids):
    for b in asteroids:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Settings for window and mouse
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Asteroids')
pygame.mouse.set_visible(False)
font = pygame.font.SysFont(None, 48)

# Game sounds
gameExplosionSound = pygame.mixer.Sound('explosion.wav')
gamePickupSound = pygame.mixer.Sound('pickup2.mp3')
gameRocketSound = pygame.mixer.Sound('rocket.mp3')
gameOverSound = pygame.mixer.Sound('end.mp3')
pygame.mixer.music.load('background.wav')
background_position = [0, 0]

# Game images
background_image = pygame.image.load("ocean.jpg").convert()
start_image = pygame.image.load('field.jpg')
playerImage = pygame.image.load('laivas3.png')
playerRect = playerImage.get_rect()
asteroidImage = pygame.image.load('asteroid.png')
explosion = pygame.image.load('explosion2.png')
cometImage = pygame.image.load('powerup.png')
bombImage = pygame.image.load('bomba1.png')
rocketImage = pygame.image.load('rocket.png')
rocketstretchedImage = pygame.transform.scale(rocketImage, (50, 120))

# Game start screen
windowSurface.blit(start_image, background_position)
drawText('Press any key to start', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 2) + 50)
pygame.display.update()
waitForPlayerToPressKey()

# Top score is kept updated
file = open("scores.txt", "r")
topScore = int(file.read())

# Start of the game setup
while True:
    bombs = []
    rockets = []
    # i is used to change rocket size
    i = 0
    rocketCounter = 0
    bombCounter = 0
    NEWbomb = random.randint(200, 400)
    asteroids = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    asteroidAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)
    
    # Spawning first comet
    comets = []
    for i in range(1):
        comets.append(pygame.Rect(random.randint(0, WINDOWWIDTH - 20),
            random.randint(0, WINDOWHEIGHT - 980), 70, 70))
    cometCounter = 0
    NEWcomet = random.randint(200, 400)

    while True: 

        # Increase score while game running
        score += 1 

        # Game exit
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            # Game controls
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                        terminate()
                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False

            # Control with mouse
            if event.type == MOUSEMOTION:
                playerRect.centerx = event.pos[0]
                playerRect.centery = event.pos[1]

        # Spawning asteroids
        if True:
            asteroidAddCounter += 1
        if asteroidAddCounter == ADDNEWasteroidRATE:
            asteroidAddCounter = 0
            asteroidSize = random.randint(asteroidMINSIZE, asteroidMAXSIZE)
            newasteroid = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - asteroidSize), 0 - asteroidSize, asteroidSize, asteroidSize),
                        'speed': random.randint(asteroidMINSPEED, asteroidMAXSPEED),
                        'surface':pygame.transform.scale(asteroidImage, (asteroidSize, asteroidSize)),
                        }
            asteroids.append(newasteroid)

        # PLayer movements
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Asteroids movement
        for b in asteroids:
            if True:
                b['rect'].move_ip(0, b['speed'])
            
        # Removing of asteroids
        for b in asteroids[:]:
            if b['rect'].top > WINDOWHEIGHT:
                asteroids.remove(b)

        # Spawning bombs
        bombCounter += 1
        if bombCounter >= NEWbomb:
            bombCounter = 0
            bombs.append(pygame.Rect(random.randint(0, WINDOWWIDTH - 20),
            random.randint(0, WINDOWHEIGHT - 980), 70, 100))
        # Bomb movement
        for f in bombs:
            f.move_ip(0, 3) 
        # Removing of bombs   
        for f in bombs:
            if f.top > WINDOWHEIGHT:
                bombs.remove(f)
        
        # Bombs turn into rockets
        for bomb in bombs[:]:
            if playerRect.colliderect(bomb):
                rockets.append(pygame.Rect(playerRect.centerx, playerRect.centery, 100, 120))
                gameRocketSound.play()
                score = score + 2000
        # Rockets removing asteroids
        for rocket in rockets[:]:
            for b in asteroids:
                if rocket.colliderect(b['rect']):    
                    asteroids.remove(b)
        for bomb in bombs[:]:
            if playerRect.colliderect(bomb):
                bombs.remove(bomb)
        # Rocket movements and growing in size
        for e in rockets:
            e.move_ip(0, -7)
            i += 1        
            rocketstretchedImage = pygame.transform.scale(rocketImage,
                (40 + i, 120 + i))
        for e in rockets:
            if e.bottom < 0:
                rockets.remove(e)
                i = 0

        # Spawning comets
        cometCounter += 1
        if cometCounter >= NEWcomet:
            cometCounter = 0
            comets.append(pygame.Rect(random.randint(0, WINDOWWIDTH - 20),
            random.randint(0, WINDOWHEIGHT - 980), 40, 70))
        # Comet moving and shaking
        for f in comets:
            f.move_ip(random.randint(-1, 1), 3)
        # Removing of comets
        for f in comets:
            if f.top > WINDOWHEIGHT:
                comets.remove(f)
        # Player interaction with comets
        for comet in comets[:]:
            if playerRect.colliderect(comet):
                gamePickupSound.play()
                comets.remove(comet)
                # Removing part of asteroids
                for b in asteroids:
                    asteroids.remove(b)
                score = score + 1000
        
        # Game window image with scores
        windowSurface.blit(background_image, background_position)
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        # Players image
        windowSurface.blit(playerImage, playerRect)

        # Interactable objects
        for b in asteroids:
            windowSurface.blit(b['surface'], b['rect'])
        for comet in comets:
            windowSurface.blit(cometImage, comet)
        for bomb in bombs:
            windowSurface.blit(bombImage, bomb)
        for rocket in rockets:
            windowSurface.blit(rocketstretchedImage, rocket)
        pygame.display.update()

        # Player and asteroid collision
        if playerHasHitasteroid(playerRect, asteroids):
            gameExplosionSound.play()
            windowSurface.blit(explosion, background_position)
            # Setting of new top score
            if score > topScore:
                topScore = score 
            break

        mainClock.tick(FPS)

    # End of game screen
    pygame.mixer.music.stop()
    gameOverSound.play()
    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 2))
    drawText('Score: %s' % (score), font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 2) + 50)
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 2) + 90)
    
    # Saving of top score and recording game score and date
    file = open("scores.txt","r")
    a = int(file.read())    
    if score > a:
        file = open("scores.txt","w")
        file.write('%s'% (score))
        file.close()
    file = open("scoresrecord.txt","a")
    file.write("\n" + date_time + " Score: %s"%(score))
    file.close()
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()