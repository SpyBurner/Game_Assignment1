import pygame
import pygame_gui
from CustomClasses import *

class Game:
    def __init__(self):
        
        #Pygame init
        pygame.init()
        pygame.display.set_caption("Game")
        
        pygame.time.Clock().tick(60)
        
        #Screen init
        SCREEN_WIDTH = 1280
        SCREEN_HEIGHT = 720
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        #GameObject list
        self.gameObjects = []
        
    def run_game(self):
        self.gameObjects.append(GameObject("Player", (100, 20), 0, (5, 5), ["Assets\\Sprites\\Link _gif"], [True], [1000]))
        
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            self.Update()
            
            self.Draw()
            
            pygame.display.update()
            
        pygame.quit()
        
    def Update(self):
        for gameObject in self.gameObjects:
            gameObject.Update()
            
    def Draw(self):
        for gameObject in self.gameObjects:
            gameObject.Draw(self.screen)
        
if __name__ == '__main__':
    game = Game()
    game.run_game()
    
        