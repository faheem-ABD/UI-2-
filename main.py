import pygame
import os

import EnemyAI as AI
import BombHandler as BH

#from pygame.sprite import _Group

# Initialising game
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.6)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Bullet Blitz")

# To set a frame time

clock = pygame.time.Clock()
FPS = 60

#define game variables
GRAVITY = 0.75
LOWER_FLOOR = 500
TILE_SIZE = 40
TILE_TYPES = 21
bg_scroll = 0

# Define player actions variable
move_left = False
move_right = False
shoot = False

img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'img/Tile/{x}.png')
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)

#load images
pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()
#store tiles in a list
water_img = pygame.image.load('img/tile/0.png').convert_alpha()

# Define bullet
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()

#define camera offset
camera_offsetX = 0
camera_offsetY = 0

#pick up boxes
health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
item_boxes = {
	'Health'	: health_box_img,
	'Ammo'		: ammo_box_img,
}

# Define colours
BG = (255, 201, 120)
White = (255, 255, 255)

font = pygame.font.SysFont('',30)



def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))




def draw_bg():
    screen.fill(BG)
    width = sky_img.get_width()
    for x in range(5):
        screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))
    for terrain in All_terrain:
        pygame.draw.rect(screen, White, pygame.Rect((terrain.x-camera_offsetX), (terrain.y-camera_offsetY), terrain.width, terrain.height))
        
    #pygame.draw.rect(screen, White, ground_platform)
    #pygame.draw.rect(screen, (0,0,255), upper_platform)
    #pygame.draw.rect(screen, (0,255,0), second_platform)

class Soldier(pygame.sprite.Sprite):
     def __init__(self , char_type, x, y , scale, speed, ammo):  # Creating instance for the movement of characters of sprites 
         self.alive = True
         self.char_type = char_type 
         self.speed = speed
         self.ammo = ammo
         self.start_ammo = ammo
         self.shoot_cooldown = 0
         self.health = 100
         self.max_health = self.health
         self.direction = 1
         self.vel_y = 0
         self.jump = False
         self.in_air = True
         self.flip = False
         self.animation_list = []
         self.frame_index = 0
         self.action = 0
         self.update_time = pygame.time.get_ticks()


         animation_types = ['Idle', 'Run', 'Jump', 'Death']
         for animation in animation_types:
            temp_list = []
            #Get a list of all the files in the directory
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        

         # To create a boundary tp contol the environemnt , 
         # where the image is drawn and self controls as instance 
         self.image = self.animation_list[self.action][self.frame_index]
         self.rect = img.get_rect()

         # Aligning to the cordinates
         self.rect.center = (x ,y)
         
         # initialize and sets the sensors for the characters
         self.left_sensor = pygame.Rect(x,y,10,100)
         self.left_sensor.center = self.rect.midleft
         self.right_sensor = pygame.Rect(x,y,10,100)
         self.right_sensor.center = (self.rect.right-20, self.rect.centery)
         self.bottom_sensor = pygame.Rect(self.rect.left+5,self.rect.bottom-5,75,10)

         # These instances are like blue prints,
         #  we can create as many as we want for the various actions

     def update(self):
         self.update_animation()
         self.check_alive()
         if self.shoot_cooldown > 0:
             self.shoot_cooldown -= 1


     def movement(self, move_left, move_right): # Create variables for the movements
         #set movement variables
         dx = 0
         dy = 0
        
         # will move the character left or right
         # if collision with terrain, will stop movement in the corresponding direction
         if move_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
            if pygame.Rect.collidelist(self.left_sensor, All_terrain) > -1:
                dx = 0
         if move_right:
             self.flip = False
             self.direction = 1
             dx = self.speed
             if pygame.Rect.collidelist(self.right_sensor, All_terrain) > -1:
                dx = 0
        
         # checks if the player have collision downwards and set the vairable "self.in_air" accorddingly
         terrain_index = pygame.Rect.collidelist(self.bottom_sensor, All_terrain)
         if terrain_index > -1:
            terrain = All_terrain[terrain_index]
            dy = terrain.top - self.rect.bottom
            self.in_air = False
            self.vel_y = 0
         else: 
            self.in_air = True

         # Jump
         if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        
        # Gravity
         if self.in_air:
            self.vel_y += GRAVITY
            if self.vel_y > 10:
                self.vel_y
            dy += self.vel_y

         #if self.rect.bottom + dy > LOWER_FLOOR:
         #   dy = LOWER_FLOOR - self.rect.bottom
         #   self.in_air = False

        # Update rect position   
         self.rect.x += dx
         self.rect.y += dy
         
         # updates the x and y for the sensors
         self.left_sensor.x += dx
         self.left_sensor.y += dy
         self.right_sensor.x += dx
         self.right_sensor.y += dy
         self.bottom_sensor.x += dx
         self.bottom_sensor.y += dy

         if self.char_type == 'player':
            global camera_offsetX, camera_offsetY
            camera_offsetX += dx
            camera_offsetY += dy

     def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20 # Reload number, lower number faster speed
            bullet = Bullet(self.rect.centerx + (0.6* self.rect.size[0]* self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            self.ammo -= 1
    
     def update_animation(self):
        #as long as it fast enough it can update animation prefectly.
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #when animation ran out then reset it
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) -1
            else:
                self.frame_index =0
     
     
     def update_action(self, new_action):
		#check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
			#update settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    
     def check_alive(self):
         if self.health <= 0:
             self.health = 0
             self.speed = 0
             self.alive = False
             self.update_action(3)

     def draw(self): # Create methods to reduce the calling
         
          #Blit function copies image from the surface to the screen 
          # using Object Oriented Programmingm

          # tests - used to visualize the indicators of the soldiers (inlc. the player)
         #pygame.draw.rect(screen, (0,0,0), pygame.Rect((self.right_indicator.x-camera_offsetX), (self.right_indicator.y-camera_offsetY), self.right_indicator.width, self.right_indicator.height))
         #pygame.draw.rect(screen, (0,0,100), pygame.Rect((self.left_indicator.x-camera_offsetX), (self.left_indicator.y-camera_offsetY), self.left_indicator.width, self.left_indicator.height))
         #pygame.draw.rect(screen, (0,0,200), pygame.Rect((self.bottom_indicator.x-camera_offsetX), (self.bottom_indicator.y-camera_offsetY), self.bottom_indicator.width, self.bottom_indicator.height))
         #pygame.draw.rect(screen, (0,0,0), self.right_indicator)
         #pygame.draw.rect(screen, (0,0,100), self.left_indicator)
         #pygame.draw.rect(screen, (0,0,200), self.bottom_indicator)
         
         screen.blit(pygame.transform.flip(self.image, self.flip, False),
                         pygame.Rect((self.rect.x-camera_offsetX), (self.rect.y-camera_offsetY), self.rect.width, self.rect.height)) 
         #screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect) 
         


class ItemBox(pygame.sprite.Sprite):
	def __init__(self, item_type, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.item_type = item_type
		self.image = item_boxes[self.item_type]
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

	def update(self):
        # Check  collision 
		
		if pygame.sprite.collide_rect(self, player):
			#check what kind of box it was
			if self.item_type == 'Health':
				player.health += 25
				if player.health > player.max_health:
					player.health = player.max_health
			elif self.item_type == 'Ammo':
				player.ammo += 15
			self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # Bullet move forward
        self.rect.x += (self.direction * self.speed)
        # If bullet disppaer from screen then kill it 
        if self.rect.right < (0+camera_offsetX) or self.rect.left > (SCREEN_WIDTH+camera_offsetX):
            self.kill()
        # Collision check
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        #get collision of all enemies and pick out the first in the list
        listOfHitEnemies = EnemyHandler.checkSpriteCollision(bullet_group)
        if listOfHitEnemies: # check if non empty list
            hitEnemy = listOfHitEnemies[0]
            if hitEnemy.alive:
                hitEnemy.health -= 20
                self.kill()
        #if pygame.sprite.spritecollide(enemy, bullet_group, False):
        #    if enemy.alive:
        #        enemy.health -= 20
        #        self.kill()

    #def draw(self, surface):
    #    surface.blit(self.image, pygame.Rect((self.rect.x-camera_offsetX), (self.rect.y-camera_offsetY), self.rect.width, self.rect.height)) 
        




upper_platform = pygame.Rect(1000, 400, 150, 100)
ground_platform = pygame.Rect((-100, LOWER_FLOOR-5), (SCREEN_WIDTH+100, 10))
second_platform = pygame.Rect((700, 450), (300, 300))

All_terrain = [upper_platform, ground_platform, second_platform]

# Create a group for bullte 
bullet_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()


item_box = ItemBox('Health', 100,450 )
item_box_group.add(item_box)
item_box = ItemBox('Ammo', 400, 450)
item_box_group.add(item_box)




#Creating instances with the given x,y and size co ordinates
player = Soldier('player', 500, 450, 3, 5, 20)
enemy = Soldier('enemy', 450, 250, 3, 5, 20)
 
# player2 = Soldier(400, 200, 3) #since we have created instances, just need to specify the co ordinates
#x = 200        
#y = 200
#scale = 3 # Try to avoid a float

bombHandler = BH.ChickenBombHandler()
EnemyHandler = AI.EnemyHandler()

bombHandler.setup(player, screen, EnemyHandler, All_terrain)

EnemyHandler.setup(player, screen, All_terrain)
EnemyHandler.addEnemyToList(enemy)

#Event handler
running = True
while running:

    if(False): #disables the camera offset
        camera_offsetX = 0
    camera_offsetY = 0

    clock.tick(FPS)
    draw_bg()
    draw_text(f'AMMO:{player.ammo}',font,White, 15, 20)
    draw_text(f'HEALTH:{player.health}',font,White, 15, 50)

    player.update()
    player.draw() 
    
    EnemyHandler.update()

    bombHandler.update(camera_offsetX, camera_offsetY)
    
    bullet_group.update()
    # have to blit and not call ".draw" of group as camera offset doesn't work.
    for spr in bullet_group.sprites():
        bullet_group.spritedict[spr] = screen.blit(spr.image, pygame.Rect((spr.rect.x-camera_offsetX), (spr.rect.y-camera_offsetY), spr.rect.width, spr.rect.height))

    item_box_group.update()
    item_box_group.draw(screen)
    



    if player.alive:
        if shoot:
            player.shoot()
        if player.in_air:
            player.update_action(2)#2: jump
        elif move_left or move_right:
            player.update_action(1)#1: run
        else:
            player.update_action(0)#0: idle
        player.movement(move_left, move_right)


     
    for event in pygame.event.get():

        # To quit game
        if event.type == pygame.QUIT:
            running = False

         # Event handler for Keyboard controls  
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a: # keyboard button a is set for the left movemen
                move_left = True    
            if event.key == pygame.K_d: # keyboard button b is set for the right movemen
                move_right  = True 
            if event.key == pygame.K_SPACE: # keyboard button SPACE is set for shooting
                shoot  = True    
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_b:
                bombHandler.spawn_chicken_bomb(player)

         # Set a release mode
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False    
            if event.key == pygame.K_d: 
                move_right = False    
            if event.key == pygame.K_SPACE: 
                shoot = False  
            if event.key == pygame.K_ESCAPE : # set a button for esc button
                run = False 
 
    # To update and call the image according to the rectangle  from the blit
    pygame.display.update()        

pygame.quit()







