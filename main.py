import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants for the window size
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

# Create the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Kate vs Cats")

# Define colors
WHITE = (255, 255, 255)
ORANGE = (255, 153, 0)
PINK = (255, 128, 179)

# Images
chigs_img =  pygame.image.load('assets/chigs_img.png')
chigs_img = pygame.transform.scale(chigs_img, (80,80))
pippin_img =  pygame.image.load('assets/pippin_img.png')
pippin_img = pygame.transform.scale(pippin_img, (80,80))
kate_img =  pygame.image.load('assets/kate_img.png')
kate_img = pygame.transform.scale(kate_img, (80,80))
background_img =  pygame.image.load('assets/background.png')
background_img = pygame.transform.scale(background_img, (WINDOW_WIDTH,WINDOW_HEIGHT))
dreamie_img =  pygame.image.load('assets/dreamies_img.png')
dreamie_img = pygame.transform.scale(dreamie_img, (80,80))

# Game variables
clock = pygame.time.Clock()
is_running = True
font = pygame.font.Font('freesansbold.ttf', 32)
score = 0

class Wall():
    def __init__(self,left,top,width,height,colour):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.left,self.top,self.width,self.height)
        self.rect2 = pygame.Rect(self.left-3,self.top-3,self.width+6,self.height+6)
        self.colour = colour
        
    def draw(self):
        pygame.draw.rect(screen,(1,1,1),self.rect2)
        pygame.draw.rect(screen,self.colour,self.rect)
        

class Background():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img = background_img

    def draw(self):
        screen.blit(self.img,(self.x,self.y))

class Collectible():
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = img

    def draw(self):
        self.x += 2
        self.y = (math.sin(self.x/120))*150
        screen.blit(self.img,(self.x,self.y))

class Cat():
    def __init__(self,x,y,img,target_player,bullet_colour):
        self.x = x 
        self.y = y
        self.img = img
        self.bullet_colour = bullet_colour
        self.target_player = target_player
        self.bullets = []
        self.shoot_timer = 0
        self.circle_radius = 0
        self.increase_radius = True

    def draw(self):
        screen.blit(self.img,(self.x,self.y))
        if self.circle_radius == 70: self.increase_radius = False
        if self.circle_radius == self.img.get_width()/2: self.increase_radius = True
        if self.increase_radius:
            self.circle_radius +=1
        else:
            self.circle_radius -=1
        RANDOM_COLOUR = (random.randint(1,255),random.randint(1,255),random.randint(1,255))
        pygame.draw.circle(screen,RANDOM_COLOUR,(self.x + (self.img.get_width()/2),self.y + 5 + (self.img.get_height()/2)),self.circle_radius,random.randint(2,10))
        pygame.draw.circle(screen,RANDOM_COLOUR,(self.x + (self.img.get_width()/2),self.y + 5 + (self.img.get_height()/2)),self.circle_radius-10,random.randint(2,10))
    def shoot(self):
        self.bullets.append(Projectile(self.x,self.y + (self.img.get_height()/2),6,self.target_player.x,self.target_player.y,self.bullet_colour))

class Particle():
    def __init__(self,x,y,radius,colour):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.y_direction = random.randint(-1,1)

    def draw(self):
        pygame.draw.circle(screen,(255,255,255),(self.x,self.y),self.radius+1)
        pygame.draw.circle(screen,self.colour,(self.x,self.y),self.radius)
        self.radius -= 0.5
        self.x -= random.randint(5,15)
        if self.y_direction == 1:
            self.y += 1
        else:
            self.y += -1

class Player():
    def __init__(self,x,y,img):
        self.x = x 
        self.y = y
        self.img = img
        self.projectiles = []
        self.allow_shoot = True
        self.shoot_cooldown = 0

    def draw(self):
        screen.blit(self.img,(self.x,self.y))

    def shoot(self):
        self.projectiles.append(Kate_Projectile(self.x + self.img.get_width(),self.y + int(self.img.get_height()/2)))

class Kate_Projectile():
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.circle(screen,(1,1,1),(self.x,self.y),10)
        pygame.draw.circle(screen,(255,255,255),(self.x,self.y),9)
        
class Projectile():
    def __init__(self,x,y,speed,target_player_x,target_player_y,colour):
        self.x = x
        self.y = y
        self.speed = speed
        self.colour = colour
        self.colour_timer = 0
        # Doubling the x and y distances for the target to enable it to leave the screen.
        # By subtracting the x and y differences
        self.target_player_x = (target_player_x - (self.x - target_player_x))
        self.target_player_y = (target_player_y - (self.y - target_player_y))

    def draw(self):
        x_change = self.x - self.target_player_x
        y_change = self.y - self.target_player_y
        hypotenuse = math.sqrt((int(x_change)**2 + int(y_change)**2))
        if hypotenuse != 0: 
            x_move = x_change/hypotenuse
            self.x -= (x_move * self.speed)

            y_move = y_change/hypotenuse
            self.y -= (y_move * self.speed)
        bullet_colour = self.colour
        self.colour_timer += 1
        if self.colour_timer < 15:
            bullet_colour = WHITE
        elif self.colour_timer > 15 and self.colour_timer < 30:
            bullet_colour = self.colour 
        if self.colour_timer == 45:
            self.colour_timer = 0   
        pygame.draw.circle(screen,(1,1,1),(self.x,self.y),8)
        pygame.draw.circle(screen,bullet_colour,(self.x,self.y),5)
        
       

# Walls
wall_list = []
wall_timer = 0

# Collectibles
dreamie_list = []
dreamie_timer = 0

# Particles
particles_list = []
particle_timer = 0

# Sprites
kate = Player(80,WINDOW_HEIGHT/2,kate_img)
chigs = Cat(WINDOW_WIDTH * random.randint(2,4),random.randint(0,WINDOW_HEIGHT),chigs_img,kate,ORANGE)
pippin = Cat(WINDOW_WIDTH * random.randint(2,4),random.randint(0,WINDOW_HEIGHT),pippin_img,kate,PINK)
background_1 = Background(0,0)
background_2 = Background(WINDOW_WIDTH,0)


# Main game loop
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        kate.y -= 8
    if keys[pygame.K_DOWN]:
        kate.y += 8
    if keys[pygame.K_RIGHT] and kate.x < 250:
        kate.x += 8
    if keys[pygame.K_LEFT] and kate.x > 1:
        kate.x -= 8
    if keys[pygame.K_SPACE] and kate.allow_shoot:
        kate.shoot()
        kate.allow_shoot = False
    
    # Erase old drawings by filling screen
    background_1.draw()
    background_1.x -= 2
    background_2.draw()
    background_2.x -= 2
    if background_1.x == (0-background_1.img.get_width()): background_1.x += (background_1.img.get_width()*2)
    if background_2.x == (0-background_2.img.get_width()): background_2.x += (background_2.img.get_width()*2)

    wall_random_x = random.randint(1,WINDOW_WIDTH)
    wall_timer += 1
    
    if len(wall_list) < 3 and wall_timer == 180 :
        RANDOM_COLOUR = (random.randint(1,255),random.randint(1,255),random.randint(1,255))
        wall = Wall(WINDOW_WIDTH + wall_random_x,random.randint(0,WINDOW_HEIGHT),50,random.randint(60,200),RANDOM_COLOUR)
        wall_list.append(wall)
        wall_timer = 0

    for wall in wall_list:
        wall.draw()
        wall.rect.left -= 5
        wall.rect2.left -= 5
        if wall.rect.left < 0:
            wall_list.remove(wall)

    dreamie_random_x = random.randint(-WINDOW_WIDTH,0)
    dreamie_timer += 1
    
    if len(dreamie_list) < 3 and dreamie_timer > 180 :
        dreamie = Collectible(random.randint(-WINDOW_WIDTH,0),random.randint(0,WINDOW_HEIGHT),dreamie_img)
        dreamie_list.append(dreamie)
        dreamie_timer = 0

    for dreamie in dreamie_list:
        dreamie.draw()
        if dreamie.x > WINDOW_WIDTH:
            dreamie_list.remove(dreamie)

    if chigs.x < (0-chigs.img.get_width()):
        chigs.x += (WINDOW_HEIGHT * random.randint(2,3))
    else:
        chigs.x -= 5
    
    chigs.shoot_timer += 1
    if chigs.shoot_timer == 120:
        chigs.shoot()
        chigs.shoot_timer = 0
    chigs.draw()
    for bullet in chigs.bullets:
        if int(bullet.x) < 0 or int(bullet.y) < 0 or bullet.x == bullet.target_player_x:
            chigs.bullets.remove(bullet)
        else:
            bullet.draw()

    if pippin.x < (0-pippin.img.get_width()):
        pippin.x += (WINDOW_HEIGHT * random.randint(2,3))
    else:
        pippin.x -= 5
    
    pippin.shoot_timer += 1
    if pippin.shoot_timer == 120:
        pippin.shoot()
        pippin.shoot_timer = 0
    pippin.draw()
    for bullet in pippin.bullets:
        if int(bullet.x) < 0 or int(bullet.y) < 0 or bullet.x == bullet.target_player_x:
            pippin.bullets.remove(bullet)
        else:
            bullet.draw()

    if particle_timer == 1:
        particle_x = kate.x - random.randint(1,100)
        particle_y = random.randint((int(kate.y)),int(kate.y+kate.img.get_height()))
        RANDOM_PARTICLE_COLOUR = (random.randint(1,255),random.randint(1,255),random.randint(1,255))
        particles_list.append(Particle(particle_x,particle_y,10,RANDOM_PARTICLE_COLOUR))
        particle_timer = 0

    particle_timer += 1
    for particle in particles_list:
        if particle.radius == 1:
            particles_list.remove(particle)
        else:
            particle.draw()

    kate.draw()
    kate.shoot_cooldown += 1
    if kate.shoot_cooldown == 60: 
        kate.shoot_cooldown = 0
        kate.allow_shoot = True
    for bullet in kate.projectiles:
        bullet.x += 5

        if bullet.x > WINDOW_WIDTH:
            kate.projectiles.remove(bullet)
        else:
            bullet.draw()


    # create a text surface object, on which text is drawn on it.
    score += 1
    text = font.render(str(score),False,(255,255,255),(0,0,0))
 
    screen.blit(text, (0,0))

    
    

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
