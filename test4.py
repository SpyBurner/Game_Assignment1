import copy
import json
import pygame
import pygame_gui
from CustomClasses import *

class Game:
    def __init__(self, settingsPath):
        settingFile = open(settingsPath)
        settingData = json.load(settingFile)
        
        #Pygame init
        pygame.init()
        pygame.display.set_caption("Game")
        
        pygame.time.Clock().tick(settingData["FPS"])
        
        #Screen init
        SCREEN_WIDTH = settingData["SCREEN_WIDTH"]
        SCREEN_HEIGHT = settingData["SCREEN_HEIGHT"]
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        #GameObject list
        self.gameObjects = {}
        
    def run_game(self):
        
        ##TEST SECTION
        linkWalkAnim = AnimationClip("Assets\\Sprites\\Link_1Sprite", "Walk", True, 1000)
        self.gameObjects["Player"] = GameObject("Player", (50, 50), 0, (5, 5), [linkWalkAnim])
        
        previousObject = self.gameObjects["Player"]
        
        timer = 0
        testCooldown = 2000
        cooldownElapsed = 0
        ###

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            ##TEST SECTION
            if (timer + testCooldown < pygame.time.get_ticks()):
                cooldownElapsed += 1

                newPos = (previousObject.position[0] + 100, previousObject.position[1])
                newRot = previousObject.rotation + 10
                
                newObject = GameObject.Instantiate("Player" + str(cooldownElapsed), previousObject, newPos, newRot)
                
                self.gameObjects[newObject.name] = newObject
                newObject.animator.GetClip("Walk").speedScale = previousObject.animator.GetClip("Walk").speedScale + 1
                
                previousObject = newObject

                timer = pygame.time.get_ticks()
            ###
            
            self.Update()
            self.Draw()
            pygame.display.update()
            
        pygame.quit()
        
    def Update(self):
        for key in self.gameObjects:
            self.gameObjects[key].Update()
            
    def Draw(self):
        for key in self.gameObjects:
            self.gameObjects[key].Draw(self.screen)
        
if __name__ == '__main__':
    game = Game("setting.json")
    game.run_game()
    
        