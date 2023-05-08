import pygame



# Initialising game
pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Bullet Blitz")

# To set a frame time

clock = pygame.time.Clock()
FPS = 60



# Define player actions variable

move_left = False
move_right = False

# Define colours

BG = (144, 201, 120)


def draw_bg():
    screen.fill(BG)

class Soldier(pygame.sprite.Sprite):
     def __init__(self , char_type, x, y , scale, speed):  # Creating instance for the movement of characters of sprites 
         pygame.sprite.Sprite.__init__(self)
         self.char_type = char_type 
         self.speed = speed
         self.direction = 1
         self.flip = False
         img = pygame.image.load(f'img/{self.char_type}/Idle/0.png')
         # To scale an image and set the image as instance 
         self.image = pygame.transform.scale(img, (int(img.get_width() * scale ), int(img.get_height() * scale)))  

         # To create a boundary tp contol the environemnt , 
         # where the image is drawn and self controls as instance
         self.rectangle = img.get_rect()

         # Aligning to the cordinates
         self.rectangle.center = (x ,y)

         # These instances are like blue prints,
         #  we can create as many as we want for the various actions


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

        # Update rectangle position   
           
         self.rectangle.x += dx
         self.rectangle.y += dy    
         
     def draw(self): # Create methods to reduce the calling
         
          #Blit function copies image from the surface to the screen 
          # using Object Oriented Programmingm
         screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rectangle) 


         
    
     
     

#Creating instances with the given x,y and size co ordinates
player = Soldier('player', 200, 200, 3, 5)
enemy = Soldier('enemy', 400, 200, 3, 5)
 
# player2 = Soldier(400, 200, 3) #since we have created instances, just need to specify the co ordinates
x = 200        
y = 200
scale = 3 # Try to avoid a float



#Event handler
running = True
while running:

    clock.tick(FPS)
    draw_bg()
    player.draw() 
    enemy.draw()
    player.movement(move_left , move_right)
    # player2.draw()


     
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

         # Set a release mode
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False    
            if event.key == pygame.K_d: 
                move_right  = False    

            if event.key == pygame.K_ESCAPE : # set a button for esc button
                run =False            
 
    # To update and call the image according to the rectangle  from the blit
    pygame.display.update()        

pygame.quit()





