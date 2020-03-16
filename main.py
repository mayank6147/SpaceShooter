import pygame
import random
import math
from pygame import mixer

# Intialize the  pygame
pygame.init()
pygame.mixer.init()
# Title and Icon
pygame.display.set_caption("SpaceShooter")
icon = pygame.image.load('battleship.png')
pygame.display.set_icon(icon)
# for window
screen = pygame.display.set_mode((800, 600))  # (width,hight)
# Background
background = pygame.image.load('bg2.png')
# Player
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
player_change = 0

#  Enemy

enemyImg=[]
enemyX = []
enemyY = []
enemy_changeX =[]
enemy_changeY =[]
num_of_enemy =6
for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemy_changeX.append(10)
    enemy_changeY.append(40)



# Bullet
pos = playerX
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bullet_changeX = 0
bullet_changeY = 10
bullet_state = 'ready'

# Score
score_value =0
font = pygame.font.Font('freesansbold.ttf',32)
game_over_font = pygame.font.Font('freesansbold.ttf',64)
textX = 10
textY = 10

# Background
mixer.music.load("background.wav")
mixer.music.play(-1)
# Function
def player(x, y):
      screen.blit(playerImg, (x, y))  # blit function is used for draw  imge on screen


def enemy(x, y,i):
      screen.blit(enemyImg[i], (x, y))  # blit function is used for draw  imge on screen


def fire_bullet(x, y):
     global bullet_state
     bullet_state = 'fire'
     screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
     distance = math.sqrt(math.pow((enemyX-bulletX),2)+math.pow((enemyY-bulletY),2))
     if distance <27:
         return True
     else:
         return False
def show_score(x,y):
    score = font.render("Score : "+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

# Gmae Over
def game_over_text():
    over_text = game_over_font.render("GAME OVER : ",True,(255,255,255))
    screen.blit(over_text,(200,250))


# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))  # is above every things
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_change = -5
            if event.key == pygame.K_RIGHT:
                player_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                  bulletSound =mixer.Sound("laser.wav")
                  bulletSound.play()
                    # GET THE CURRENT X CORDINATES
                  bulletX = playerX
                  fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or pygame.K_LEFT:
                player_change = 0

    # RGB  -red ,Green ,Blue
    playerX += player_change

    if playerX <= 0:
        playerX = 0
    # 800-64 =736 because picture is 64 x 64 picxel
    if playerX >= 736:
        playerX = 736

    # for enemy movement
    for i in range(num_of_enemy):
        if enemyY[i] > 480:
            for j in range(num_of_enemy):
                enemyY[j]=2000
            game_over_text()
            break
        enemyX[i] += enemy_changeX[i]

        if enemyX[i] <= 0:
            enemy_changeX[i] = 5
            enemyY[i] += enemy_changeY[i]
        # 800-64 =736 because picture is 64 x 64 picxel
        if enemyX[i] >= 736:
            enemy_changeX[i] = -5
            enemyY[i] += enemy_changeY[i]

      #  if enemyY[i] >= 536:
      #      enemyY[i] = 50
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            enemyY[i] = random.randint(50, 150)
            enemyX[i] = random.randint(0, 736)
            score_value += 1
            #print(score)
        enemy(enemyX[i], enemyY[i],i)

    if bulletY <=0:
        bulletY=480
        bullet_state = "ready"

    if bullet_state is 'fire':
         fire_bullet(bulletX, bulletY)
         bulletY -= bullet_changeY



    player(playerX, playerY)
   # enemy(enemyX, enemyY)
    show_score(textX,textY)
    pygame.display.update()
