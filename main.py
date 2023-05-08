import pygame
import os

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

# Define colours

BG = (144, 201, 120)
White = (255, 255, 255)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, White, (0, 300), (SCREEN_WIDTH, 300))

class Soldier(pygame.sprite.Sprite):
     def __init__(self , char_type, x, y , scale, speed):  # Creating instance for the movement of characters of sprites 
         pygame.sprite.Sprite.__init__(self)
         self.alive = True
         self.char_type = char_type 
         self.speed = speed
         self.direction = 1
         self.vel_y = 0
         self.jump = False
         self.in_air = True
         self.flip = False
         self.animation_list = []
         self.frame_index = 0
         self.action = 0
         self.update_time = pygame.time.get_ticks()


         animation_types = ['Idle', 'Run', 'Jump']
         for animation in animation_types:
            temp_list = []
            #Get a list of all the files in the directory
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        

         # To create a boundary tp contol the environemnt , 
         # where the image is drawn and self controls as instance 
         self.image = self.animation_list[self.action][self.frame_index]
         self.rectangle = img.get_rect()

         # Aligning to the cordinates
         self.rectangle.center = (x ,y)

         # These instances are like blue prints,
         #  we can create as many as we want for the various actions


     def movement(self, move_left, move_right): # Create variables for the movements
         #set movement variables
         dx = 0
         dy = 0
         
        # Move left or right
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
         if self.rectangle.bottom + dy > 300:
            dy = 300 - self.rectangle.bottom
            self.in_air = False
                        

        # Update rectangle position   
         self.rectangle.x += dx
         self.rectangle.y += dy    

     def update_animation(self):
        #as long as it fast enough it can update animation prefectly.
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #when animation ran out then reset it
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index =0
     
     
     def update_action(self, new_action):
		#check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
			#update settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
                        

     def draw(self): # Create methods to reduce the calling
         
          #Blit function copies image from the surface to the screen 
          # using Object Oriented Programmingm
         screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rectangle) 


         
    
     
     

#Creating instances with the given x,y and size co ordinates
player = Soldier('player', 200, 200, 2, 5)
enemy = Soldier('enemy', 400, 200, 2, 5)



#Event handler
running = True
while running:

    clock.tick(FPS)
    draw_bg()
    player.update_animation()
    player.draw()
    enemy.draw()


    if player.alive:
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
            if event.key == pygame.K_d: # keyboard button a is set for the right movemen
                move_right  = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:# set a button for esc button
                run = False        

         # Set a release mode
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False    
            if event.key == pygame.K_d: 
                move_right  = False    
  
 
    # To update and call the image according to the rectangle  from the blit
    pygame.display.update()        

pygame.quit()



