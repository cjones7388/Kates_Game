import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants for the window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Create the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Kate vs Cats")

# Define colors
WHITE = (255, 255, 255)

# Images
chigs_img =  pygame.image.load('assets/chigs_img.png')
chigs_img = pygame.transform.scale(chigs_img, (80,80))
background_img =  pygame.image.load('assets/background.png')
background_img = pygame.transform.scale(background_img, (WINDOW_WIDTH,WINDOW_HEIGHT))

# Game variables
clock = pygame.time.Clock()
is_running = True

class Wall():
    def __init__(self,left,top,width,height,colour):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.left,self.top,self.width,self.height)
        self.colour = colour
        
    def draw(self):
        pygame.draw.rect(screen,self.colour,self.rect)

class Background():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img = background_img

    def draw(self):
        screen.blit(self.img,(self.x,self.y))

class Cat():
    def __init__(self,x,y,img,target_player):
        self.x = x 
        self.y = y
        self.img = img
        self.target_player = target_player
        self.bullets = []
        self.shoot_timer = 0

    def draw(self):
        screen.blit(self.img,(self.x,self.y))

    def shoot(self):
        self.bullets.append(Projectile(self.x,self.y + (self.img.get_height()/2),5,self.target_player.x,self.target_player.y))

class Player():
    def __init__(self,x,y,img):
        self.x = x 
        self.y = y
        self.img = img

    def draw(self):
        #screen.blit(self.img,(self.x,self.y))
        pygame.draw.rect(screen,(255,100,100),pygame.Rect(self.x,self.y,50,50))

class Projectile():
    def __init__(self,x,y,speed,target_player_x,target_player_y):
        self.x = x
        self.y = y
        self.speed = speed
        self.target_player_x = target_player_x
        self.target_player_y = target_player_y

    def draw(self):
        x_change = self.x - self.target_player_x
        y_change = self.y - self.target_player_y
        hypotenuse = math.sqrt((int(x_change)**2 + int(y_change)**2))
        if hypotenuse != 0: 
            x_move = x_change/hypotenuse
            self.x -= (x_move * self.speed)

            y_move = y_change/hypotenuse
            self.y -= (y_move * self.speed)
        pygame.draw.rect(screen,(255,20,147),pygame.Rect(self.x,self.y,8,10))
       

# Walls
wall_list = []
wall_timer = 0

# Sprites
kate = Player(40,WINDOW_HEIGHT/2,000)
chigs = Cat(WINDOW_WIDTH + random.randint(1,100),random.randint(0,WINDOW_HEIGHT),chigs_img,kate)
background_1 = Background(0,0)
background_2 = Background(WINDOW_WIDTH,0)


# Main game loop
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        kate.y -= 5
    if keys[pygame.K_DOWN]:
        kate.y += 5

    wall_random_x = random.randint(1,WINDOW_WIDTH)
    wall_timer += 1
    
    if len(wall_list) < 3 and wall_timer == 180 :
        RANDOM_COLOUR = (random.randint(1,255),random.randint(1,255),random.randint(1,255))
        wall = Wall(WINDOW_WIDTH + wall_random_x,random.randint(0,WINDOW_HEIGHT),50,random.randint(60,200),RANDOM_COLOUR)
        wall_list.append(wall)
        wall_timer = 0
    
    # Erase old drawings by filling screen black
    # screen.fill((0,0,0))
    background_1.draw()
    background_1.x -= 2
    background_2.draw()
    background_2.x -= 2
    if background_1.x == (0-background_1.img.get_width()): background_1.x += (background_1.img.get_width()*2)
    if background_2.x == (0-background_2.img.get_width()): background_2.x += (background_2.img.get_width()*2)

    # Game logic goes here
    for wall in wall_list:
        wall.draw()
        wall.rect.left -= 5
        if wall.rect.left < 0:
            wall_list.remove(wall)

    if chigs.x < (0-chigs.img.get_width()):
        chigs.x += WINDOW_HEIGHT + random.randint(100,1000)
    else:
        chigs.x -= 2
    
    chigs.shoot_timer += 1
    if chigs.shoot_timer == 50:
        chigs.shoot()
        chigs.shoot_timer = 0
    chigs.draw()
    for bullet in chigs.bullets:
        if int(bullet.x) <= 40:
            chigs.bullets.remove(bullet)
        else:
            bullet.draw()

    kate.draw()
    

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
