import pygame
import os
from enum import Enum

class EnemyHandler():

    def __init__(self):

        self.listOfEnemies = []
        self.EnemyVisionLenght = 400

        self.player = None
        self.screen = None

    #import values from main
    def setup(self, playerChar, mainScreen):
        self.player = playerChar
        self.screen = mainScreen

    #add enemy and information regarding their current state
    def addEnemyToList(self, enemy):
        InternalTimer = 0
        previousState = self.State.MOVE_LEFT
        # [current State, previous State, timer for current state]
        EnemyInfo = [self.State.STAY, previousState, InternalTimer] 

        self.listOfEnemies.append([enemy, EnemyInfo])

    #update everything
    def update(self):
        self.updateEnemiesPath()

    #update enemies
    def updateEnemiesPath(self):
        for enemyStack in self.listOfEnemies:
            #Decompile 
            enemy = enemyStack[0]
            enemyInfo = enemyStack[1]

            enemy.update()
            enemy.draw()

            #default values of moving
            move_left = False
            move_right = False

            if enemy.alive:
                
                
                # ---------------------- check player --------------------------------------
                # --------------------------------------------------------------------------
                hitRect = None
                if enemy.direction > 0: #looking right
                    hitRect = pygame.Rect(enemy.rect.center[0], enemy.rect.center[1], self.EnemyVisionLenght, 1)
                else: #looking left
                    hitRect = pygame.Rect(enemy.rect.center[0]-self.EnemyVisionLenght, enemy.rect.center[1], self.EnemyVisionLenght, 1)

                # test - visualizing hitRect
                #pygame.draw.rect(self.screen, (0, 0, 0), hitRect)
                if pygame.Rect.colliderect(self.player.rect, hitRect) and self.player.alive:
                    enemy.shoot()


                # ---------------------- check movement ------------------------------------
                # --------------------------------------------------------------------------
                if enemyInfo[0] == self.State.STAY:
                    enemyInfo[2] += 1 # update timer
                    
                    #reset Timer
                    if enemyInfo[2] >= self.getStateTimerValues(self.State.STAY):
                        self.updateState(enemyInfo)

                elif enemyInfo[0] == self.State.MOVE_LEFT:
                    enemyInfo[2] += 1 # update timer
                    move_left = True
                    
                    #reset Timer
                    if enemyInfo[2] >= self.getStateTimerValues(self.State.MOVE_LEFT):
                        self.updateState(enemyInfo)

                elif enemyInfo[0] == self.State.MOVE_RIGHT:
                    enemyInfo[2] += 1 # update timer
                    move_right = True
                    
                    #reset Timer
                    if enemyInfo[2] >= self.getStateTimerValues(self.State.MOVE_RIGHT):
                        self.updateState(enemyInfo)


                # ---------------------- update animations ---------------------------------
                # --------------------------------------------------------------------------
                if enemy.in_air:
                    enemy.update_action(2)#2: jump
                elif move_left or move_right:
                    enemy.update_action(1)#1: run
                else:
                    enemy.update_action(0)#0: idle

            #update enemy movement
            enemy.movement(move_left, move_right)


            
        
    #States of the enemy
    class State(Enum):
        STAY = 1
        MOVE_RIGHT = 2
        MOVE_LEFT = 3
        #SHOOTING = 4

    #time values for the different states
    def getStateTimerValues(self, state):
        if state == self.State.STAY:
            return 90
        elif state == self.State.MOVE_LEFT or state == self.State.MOVE_RIGHT:
            return 120
        else:
            return 0
    
    # will reset the timer and update the current and previous state
    def updateState(self, enemyInfo):

        enemyInfo[2] = 0 # reset Timer
        currentState = enemyInfo[0]

        #set new current state based on the current and previous state
        if currentState == self.State.STAY:
            #check previous state and set new current
            if enemyInfo[1] == self.State.MOVE_LEFT:
                enemyInfo[0] = self.State.MOVE_RIGHT
            else:
                enemyInfo[0] = self.State.MOVE_LEFT
        
        elif currentState == self.State.MOVE_LEFT:
            enemyInfo[0] = self.State.STAY
        elif currentState == self.State.MOVE_RIGHT:
            enemyInfo[0] = self.State.STAY
        else:
            enemyInfo[0] = self.State.STAY
        
        enemyInfo[1] = currentState # set previous state to current

    # checks collision of enemies with sprites 
    def checkSpriteCollision(self, spriteGroup):
        temp_list = []
        for enemyStack in self.listOfEnemies:
            enemy = enemyStack[0]
            if enemy.alive and pygame.sprite.spritecollide(enemy, spriteGroup, False):
                temp_list.append(enemy)
        return temp_list
    
    # checks collision of enemies with rect 
    def checkRectCollision(self, collisionRect):
        temp_list = []
        for enemyStack in self.listOfEnemies:
            enemy = enemyStack[0]
            if enemy.alive and pygame.Rect.colliderect(enemy.rect, collisionRect):
                temp_list.append(enemy)
        return temp_list