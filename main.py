import pygame
import os

#from pygame.sprite import _Group

# Initialising game
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Bullet Blitz")

# To set a frame time

clock = pygame.time.Clock()
FPS = 60

#define game variables
GRAVITY = 0.75

# Define player actions variable
move_left = False
move_right = False
shoot = False

# Define bullet
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()


# Define colours
BG = (144, 201, 120)
White = (255, 255, 255)

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
        if pygame.sprite.spritecollide(enemy, bullet_group, False):
            if enemy.alive:
                enemy.health -= 20
                self.kill()






# Create a group for bullte 
bullet_group = pygame.sprite.Group()



class ChickenBombHandler():
    def __init__(self):
        self.max_amount = 10
        self.current_amount = 0
        self.time_limit = 100
        self.explo_time = 20

        self.active_bombs = list()
        self.detonated_bombs = list()

        self.img_1 = pygame.image.load(f'img/icons/chicken_bomb_1.png')
        self.img_2 = pygame.image.load(f'img/icons/chicken_bomb_2.png')
        self.img_feather = pygame.image.load(f'img/icons/feather.png')
        self.img_poof_1 = pygame.image.load(f'img/icons/poof_1.png')
        self.img_poof_2 = pygame.image.load(f'img/icons/poof_2.png')
        self.img_poof_3 = pygame.image.load(f'img/icons/poof_3.png')
        self.img_poof_4 = pygame.image.load(f'img/icons/poof_4.png')
        
        scale = 1
        self.image_1 = pygame.transform.scale(self.img_1, (int(self.img_1.get_width() * scale ), int(self.img_1.get_height() * scale))) 
        self.image_2 = pygame.transform.scale(self.img_2, (int(self.img_2.get_width() * scale ), int(self.img_2.get_height() * scale)))  
 
        self.image_feather = pygame.transform.scale(self.img_feather, (int(self.img_feather.get_width() * scale ), int(self.img_feather.get_height() * scale)))
        
        scale = 2
        self.image_poof_1 = pygame.transform.scale(self.img_poof_1, (int(self.img_poof_1.get_width() * scale ), int(self.img_poof_1.get_height() * scale)))
        self.image_poof_2 = pygame.transform.scale(self.img_poof_2, (int(self.img_poof_2.get_width() * scale ), int(self.img_poof_2.get_height() * scale)))
        self.image_poof_3 = pygame.transform.scale(self.img_poof_3, (int(self.img_poof_3.get_width() * scale ), int(self.img_poof_3.get_height() * scale)))
        self.image_poof_4 = pygame.transform.scale(self.img_poof_4, (int(self.img_poof_4.get_width() * scale ), int(self.img_poof_4.get_height() * scale)))
        

    def spawn_chicken_bomb(self, player):
        if self.current_amount >= self.max_amount:
            return
        rect = self.img_1.get_rect()
        rect.center = (player.rect.midtop[0], player.rect.midtop[1])
        dir = player.direction
        time = 0
        chicken_bomb = [rect, dir, time]
        self.active_bombs.append(chicken_bomb)
        self.current_amount += 1 

    def chicken_explo(self):
        chicken = self.active_bombs.pop(0)
        self.current_amount -= 1
        time = 0
        x = chicken[0].x
        y = chicken[0].y
        self.detonated_bombs.append([time, x, y])

    def update(self): #update bomb path, timer, and draw.
        for chicken in self.active_bombs: 
            self.draw(chicken)
            chicken[2] += 1
            if chicken[2] >= self.time_limit:
                self.chicken_explo()

            chicken[0].x += 4 * chicken[1]
            x_value = chicken[2]
            if x_value < 20:
                chicken[0].y -= 3
            else:
                chicken[0].y += 2
        for explo in self.detonated_bombs:
            self.draw_feather(explo)
            explo[0] += 1
            if explo[0] >= self.explo_time:
                self.detonated_bombs.remove(explo)


    
    def draw(self, chicken):
        time = chicken[2]
        rot_speed = 4
        if time % 8 < 4:
            screen.blit(pygame.transform.rotate(self.image_1, time*4), (chicken[0].x, chicken[0].y))
        else:
            screen.blit(pygame.transform.rotate(self.image_2, time*4), (chicken[0].x, chicken[0].y))
            
    def draw_feather(self, explo):
        time = explo[0]
        speed = 4
        screen.blit(pygame.transform.rotate(self.image_feather, 0), (explo[1]+(time*speed), explo[2]))
        screen.blit(pygame.transform.rotate(self.image_feather, 180), (explo[1]-(time*speed), explo[2]))
        screen.blit(pygame.transform.rotate(self.image_feather, 270), (explo[1], explo[2]+(time*speed)))
        screen.blit(pygame.transform.rotate(self.image_feather, 90), (explo[1], explo[2]-(time*speed)))
        
        screen.blit(pygame.transform.rotate(self.image_feather, -45), (explo[1]+(time*speed/2), explo[2]+(time*speed/2)))
        screen.blit(pygame.transform.rotate(self.image_feather, 225), (explo[1]-(time*speed/2), explo[2]+(time*speed/2)))
        screen.blit(pygame.transform.rotate(self.image_feather, 45), (explo[1]+(time*speed/2), explo[2]-(time*speed/2)))
        screen.blit(pygame.transform.rotate(self.image_feather, 135), (explo[1]-(time*speed/2), explo[2]-(time*speed/2)))

        offestX = -40
        offestY = -40
        if time < 4:
            screen.blit(self.image_poof_1, (explo[1]+offestX, explo[2]+offestY))
        elif time < 8:
            screen.blit(self.image_poof_2, (explo[1]+offestX, explo[2]+offestY))
        elif time < 12:
            screen.blit(self.image_poof_3, (explo[1]+offestX, explo[2]+offestY))
        elif time < 16:
            screen.blit(self.image_poof_4, (explo[1]+offestX, explo[2]+offestY))




     

#Creating instances with the given x,y and size co ordinates
player = Soldier('player', 200, 200, 3, 5, 20)
enemy = Soldier('enemy', 400, 200, 3, 5, 20)
 
# player2 = Soldier(400, 200, 3) #since we have created instances, just need to specify the co ordinates
#x = 200        
#y = 200
#scale = 3 # Try to avoid a float

bombHandler = ChickenBombHandler()

#Event handler
running = True
while running:

    clock.tick(FPS)
    draw_bg()
    player.update()
    player.draw() 


    enemy.update()
    enemy.draw()
    
    
    bullet_group.update()
    bullet_group.draw(screen)



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

    bombHandler.update()


     
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







