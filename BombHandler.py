import pygame
import math


class ChickenBombHandler():
    def __init__(self):
        #set the max and current amount of chicken bombs.
        self.max_amount = 10
        self.current_amount = 0
        #sets the time limiit of the bomb until explosion and how long the exposion will last
        self.time_limit = 100
        self.explo_time = 20

        # list of all active bombs and exposions
        self.active_bombs = list()
        self.detonated_bombs = list()

        # setup all sprites used for the chicken and the explosion.
        # 1-2 = chicken
        # 3 = feather
        # 4-7 = poof cloud
        self.animationFrames = []
        animation_types = [("chicken_bomb", 2, 1), ("feather", 1, 1), ("poof", 4, 2)]
        for (animation, num_of_frames, scale) in animation_types:
            temp_list = []
            #Get a list of all the files in the directory
            for i in range(1, num_of_frames+1):
                img = pygame.image.load(f'img/icons/{animation}_{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animationFrames.append(temp_list)

        # variables imported from main
        self.player = None
        self.screen = None
        self.enemyHandler = None

    #import data from main
    def setup(self, playerChar, mainScreen, enemy_handler):
        self.player = playerChar
        self.screen = mainScreen
        self.enemyHandler = enemy_handler

    def spawn_chicken_bomb(self, player):
        # if the amount of spawned chickens bombs are larger than the allowed max value, will then reurn and not spawn a new one.
        if self.current_amount >= self.max_amount:
            return
        rect = self.animationFrames[0][0].get_rect()
        rect.center = (player.rect.midtop[0], player.rect.midtop[1])
        dir = player.direction
        time = 0
        chicken_bomb = [rect, dir, time]
        self.active_bombs.append(chicken_bomb)
        self.current_amount += 1 

    def chicken_explo(self):
        # removes the chicken bombs first in the list and decrease the current amount of chickens bombs with 1
        chicken = self.active_bombs.pop(0)
        self.current_amount -= 1

        # variables for setting the explosion
        time = 0
        x = chicken[0].x
        y = chicken[0].y

        # set the size of the exposion for collision with other objects, ex. player, enemies
        area = 50
        explosion_area = pygame.Rect(x-area, y-area, area*2, area*2)

        self.detonated_bombs.append([time, x, y, explosion_area])

    def update(self): #update bomb path, timer, and draw.
        
        # ---------- draws all chicken bombs ------
        # -----------------------------------------
        for chicken in self.active_bombs: 
            self.draw_chicken(chicken)
            chicken[2] += 1 #increase chicken bomb timer
            if chicken[2] >= self.time_limit:
                self.chicken_explo()

            # path of the chicken bomb when thrown
            chicken[0].x += 4 * chicken[1]
            x_value = chicken[2]
            if x_value < 20:
                chicken[0].y -= 3
            else:
                chicken[0].y += 2

        # ---------- draws all exposions ----------
        # -----------------------------------------
        for explo in self.detonated_bombs:
            self.draw_explosion(explo)
            explo[0] += 1 #increase eplosion timer
            self.check_Explosion_Collision(explo[3])
            if explo[0] >= self.explo_time:
                self.detonated_bombs.remove(explo)

    def check_Explosion_Collision(self, exploRect):
        #checked every update/frame
        if pygame.Rect.colliderect(self.player.rect, exploRect):
            if self.player.alive:
                self.player.health -= 1
        listOfHitEnemies = self.enemyHandler.checkRectCollision(exploRect)
        for enemy in listOfHitEnemies:
            enemy.health -= 5
    
    #draws the chicken bomb
    def draw_chicken(self, chicken):
        time = chicken[2]
        rotation_speed = 4
        # rotates the chicken while alterating between the two sprites
        self.screen.blit(pygame.transform.rotate(self.animationFrames[0][((time % 8) // 4)], time*rotation_speed), (chicken[0].x, chicken[0].y))

    #draws the expolosion, both the cloud and the feathers
    def draw_explosion(self, explo):
        time = explo[0]
        speed = 4
        #all directions of the feathers written in x y coordinates. the values is also use for the speed of the feathers
        directions = [(1,0), (-1,0), (0,1), (0,-1),
                      (0.707,0.707), (-0.707,0.707), (0.707,-0.707), (-0.707,-0.707),
                      (0.924,0.383), (0.383,0.924), (-0.924,0.383), (-0.383,0.924),
                      (0.924,-0.383), (0.383,-0.924), (-0.924,-0.383), (-0.383,-0.924)]
        for (i, j) in directions:
            # get the roation degree from x,y
            rotation = math.atan2(i,j)/math.pi*180-90
            # draws the feather
            self.screen.blit(pygame.transform.rotate(self.animationFrames[1][0], rotation), (explo[1]+(time*speed*i), explo[2]+(time*speed*j)))

        #draws the cloud in the middle with an offset to make sure it is in the middle of the explosion.
        offestX = -40
        offestY = -40
        self.screen.blit(self.animationFrames[2][(time // 5)], (explo[1]+offestX, explo[2]+offestY))