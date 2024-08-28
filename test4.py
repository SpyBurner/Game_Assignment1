import pygame
import pygame_gui
from CustomClasses import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Game")
        
        SCREEN_WIDTH = 1280
        SCREEN_HEIGHT = 720
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.gameObjects = []
        
    def run_game(self):
        self.gameObjects.append(GameObject("Player", (20, 20), 0, (5, 5), ["Assets\\Sprites\\Link _gif"], [True]))
        
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
    
        