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
        self.CIRCLE_COORDINATE = [[(100, 150), (250, 150), (400, 150)], [(100, 300), (250, 300), (400, 300)], [(100, 450), (250, 450), (400, 450)]]        
        self.tile = (-100, -100)
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        #GameObject list
        self.gameObjects = {}
        
    def run_game(self):
        
        ###TEST SECTION
        #linkWalkAnim = AnimationClip("Assets\\Sprites\\Link_gif", "Walk", True, 1000)
        #self.gameObjects["Player"] = GameObject("Player", (100, 20), 0, (5, 5), [linkWalkAnim])
        
        #timer = 0
        #testCooldown = 2000
        #cooldownElapsed = 0
        ####

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.tile = self.get_tile(event.pos[0]//1, event.pos[1]//1)
                    if ((event.pos[0]-self.tile[0]) * (event.pos[0]-self.tile[0])  + (event.pos[1]-self.tile[1]) * (event.pos[1]-self.tile[1]) > 4900):
                        self.tile = (-100, -100)
                        
                        

            
            ##TEST SECTION
                #if (timer + testCooldown < pygame.time.get_ticks()):
                #    cooldownElapsed += 1
                #    self.gameObjects["Player"].animator.GetClip("Walk").speedScale += 1
                #    timer = pygame.time.get_ticks()
            ###
            
            self.Update()
            self.Draw()
            pygame.draw.circle(self.screen, (255, 0, 0), self.tile, 70)
            pygame.display.update()
            
        pygame.quit()
        
    def Update(self):
        for key in self.gameObjects:
            self.gameObjects[key].Update()
            

    def draw_circle_matrix(self):
        radius = 70
        for row in range(3):
            for col in range(3):
                # Draw the circle on the screen
                pygame.draw.circle(self.screen, (0, 0, 0), self.CIRCLE_COORDINATE[row][col], radius)
    def Draw(self):
        for key in self.gameObjects:
            self.gameObjects[key].Draw(self.screen)
        self.screen.fill((255, 255, 255))  # Fill the screen with black
        self.draw_circle_matrix()     # Draw the circle matrix
        for key in self.gameObjects:
            self.gameObjects[key].Draw(self.screen)
    
    def get_tile(self, x, y):
        # Define margins and grid size
        margin_left_right = 50
        margin_top_bottom = 100
        grid_size = 400  # Total size of the grid excluding margins
        tile_size = grid_size // 3  # Size of each tile (400/3)

        # Check if the (x, y) is inside the grid boundaries
        if not (margin_left_right <= x <= margin_left_right + grid_size and
                margin_top_bottom <= y <= margin_top_bottom + grid_size):
            return (-100,-100)  # Outside the grid

        # Calculate the column and row based on the position inside the grid
        c = (x - margin_left_right) // tile_size
        r = (y - margin_top_bottom) // tile_size

        return self.CIRCLE_COORDINATE[r][c]
        
        
        
if __name__ == '__main__':
    game = Game("setting.json")
    game.run_game()
    
        