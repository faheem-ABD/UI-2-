import pygame



# Initialising game
pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bullet Blitz")


x = 200
y = 200

img = pygame.image.load('img/player/Idle/0.png')

# To create a boundary tp contol the environemnt , where the image is drawn
rectangle = img.get_rect()

#Aligning to the cordinates
rectangle.center = (x ,y)

#Event handler
running = True
while running:

    #Blit function copies image from the surface to the screen
    screen.blit(img , rectangle)


     
    for event in pygame.event.get():

        # To quit game
        if event.type == pygame.QUIT:
            running = False
     
    # To update and call the image according to the rectangle  from the blit
    pygame.display.update()        

pygame.quit()

print("Hekko word")



