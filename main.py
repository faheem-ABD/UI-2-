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
TILE_SIZE = 40

# Define player actions variable
move_left = False
move_right = False
shoot = False

# Define bullet
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()

#pick up boxes
health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
item_boxes = {
	'Health'	: health_box_img,
	'Ammo'		: ammo_box_img,
}

# Define colours
BG = (144, 201, 120)
White = (255, 255, 255)

font = pygame.font.SysFont('Time new roman', 30)


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))




def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, White, (0, 300), (SCREEN_WIDTH, 300), 10)

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
         
        
         if move_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
         if move_right:
             self.flip = False
             self.direction = 1
             dx = self.speed
             
         # Jump
         if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        # Gravity
         self.vel_y += GRAVITY
         if self.vel_y > 10:
            self.vel_y
         dy += self.vel_y

		#check collision with floor
         if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False
                        

        # Update rect position   
         self.rect.x += dx
         self.rect.y += dy    

     def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20 # Reload number, lower number faster speed
            bullet = Bullet(self.rect.centerx + (0.6* self.rect.size[0]* self.direction),self.rect.centery,self.direction)
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
         screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect) 
         


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
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
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
            hitEnemy.health -= 20
            self.kill()
        #if pygame.sprite.spritecollide(enemy, bullet_group, False):
        #    if enemy.alive:
        #        enemy.health -= 20
        #        self.kill()






# Create a group for bullte 
bullet_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()


item_box = ItemBox('Health', 100, 260)
item_box_group.add(item_box)
item_box = ItemBox('Ammo', 400, 260)
item_box_group.add(item_box)




#Creating instances with the given x,y and size co ordinates
player = Soldier('player', 200, 200, 3, 5, 20)
enemy = Soldier('enemy', 400, 200, 3, 5, 20)
 
# player2 = Soldier(400, 200, 3) #since we have created instances, just need to specify the co ordinates
#x = 200        
#y = 200
#scale = 3 # Try to avoid a float

bombHandler = BH.ChickenBombHandler()
EnemyHandler = AI.EnemyHandler()

bombHandler.setup(player, screen, EnemyHandler)

EnemyHandler.setup(player, screen)
EnemyHandler.addEnemyToList(enemy)

#Event handler
running = True
while running:

    clock.tick(FPS) 
    draw_bg()
    draw_text(f'AMMO:{player.ammo}',font,White, 15, 20)
    draw_text(f'HEALTH:{player.health}',font,White, 15, 50)

    player.update()
    player.draw() 
    
    EnemyHandler.update()

    bombHandler.update()
    
    bullet_group.update()
    bullet_group.draw(screen)

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







