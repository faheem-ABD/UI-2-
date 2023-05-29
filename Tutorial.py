import pygame
import os

class Tutorial():
    def __init__(self, mainScreen, cameraOffsetX, cameraOffsetY, screenWidth, screenHeight):
        self.screen = mainScreen
        self.offsetX = cameraOffsetX
        self.offsetY = cameraOffsetY
        self.WIDTH = screenWidth
        self.HEIGHT = screenHeight
        self.selectedLanguage = 0


        self.terrainList = list()
        floorLevel = 600
        floor = pygame.Rect((-100, floorLevel), (self.WIDTH*2, screenHeight-floorLevel))
        self.terrainList.append(floor)

        self.TutorialPaused = False
        self.TutorialEnd = False
        self.selectedMenuOption = 0

        self.font = pygame.font.SysFont('',30)
        self.large_font = pygame.font.SysFont('',50)
        self.extreme_font = pygame.font.SysFont('',100)

        self.colorLightGreen = (208,240,192)

        self.TextList = list()
        tutorialTextFile = open("TutorialText.txt", "r")
        for line in tutorialTextFile:
            self.TextList.append(line)
        tutorialTextFile.close()

    def getTextFromFile(self, index):
        textIndex = index + self.selectedLanguage * 5
        returnText = self.TextList[textIndex]
        return returnText[:-1]


    def draw_text(self, text, font, text_color, x, y):
        img = font.render(text, True, text_color)
        self.screen.blit(img, (x, y))

    def resetTutorial(self):
        self.selectedMenuOption = 0
        self.TutorialPaused = False
        self.TutorialEnd = False

    def startTutorial(self):
        return

    def updateTutorial(self, eventList, language):
        #update varaibles from the main file
        self.selectedLanguage = language

        #updates the terrain for the tutorial
        self.updateTutorialTerrain()
        
        #check if the tutorial is paused
        if self.TutorialPaused:
            self.updateTutorialMenu()
            

            for event in eventList:
                # event Type "QUIT" is handled before enetering update in tutorial
                # Event handler for Keyboard controls  
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.TutorialPaused = False
                    if event.key == pygame.K_RETURN:
                        if self.selectedMenuOption == 0:
                            self.TutorialPaused = False
                        elif self.selectedMenuOption == 1:
                            self.TutorialEnd = True
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.selectedMenuOption -= 1
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.selectedMenuOption += 1
            
            if (self.selectedMenuOption > 1):
                self.selectedMenuOption = 1
            if (self.selectedMenuOption < 0):
                self.selectedMenuOption = 0

        else:
            for event in eventList:
                # event Type "QUIT" is handled before enetering update in tutorial
                # Event handler for Keyboard controls  
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.TutorialPaused = True

    def updateTutorialTerrain(self):
        for terrain in self.terrainList:
            pygame.draw.rect(self.screen, self.colorLightGreen, pygame.Rect((terrain.x-self.offsetX), (terrain.y-self.offsetY), terrain.width, terrain.height))

    def updateTutorialMenu(self):
        backgroundDim = pygame.Surface((self.WIDTH, self.HEIGHT))
        backgroundDim.set_alpha(100)
        backgroundDim.fill((0,0,0))
        self.screen.blit(backgroundDim, (0,0))

        self.draw_text(self.getTextFromFile(1), self.extreme_font, (220,220,220), 240,200)

        xPlacement = 370
        yPlacement = 480
        boxWidth = 380
        textOffset = 40 - 30 * self.selectedLanguage

        for i in range(2):
            color = (0,0,0)
            if self.selectedMenuOption == i:
                color = (100,100,100)
                
            pygame.draw.rect(self.screen, color, pygame.Rect(xPlacement, yPlacement+(70*i), boxWidth, 50))

        self.draw_text(self.getTextFromFile(2), self.large_font, (255,255,255), xPlacement+textOffset, 490)
        self.draw_text(self.getTextFromFile(3), self.large_font, (255,255,255), xPlacement+textOffset, 560)


