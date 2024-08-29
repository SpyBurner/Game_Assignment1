import json
import pygame
import random
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
        self.hit = 0
        self.miss = 0
        self.random_x = 0
        self.random_y = 0
        
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
        self.last_random_time = 0
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ((event.pos[0]-self.tile[0]) * (event.pos[0]-self.tile[0])  + (event.pos[1]-self.tile[1]) * (event.pos[1]-self.tile[1]) > 4900):
                       
                        self.miss += 1
                    else:
                        self.last_random_time-=5000
                        self.hit+=1
                        

            self.get_random_xy_every_5_seconds()
            self.tile = self.CIRCLE_COORDINATE[self.random_x][self.random_y]
            ##TEST SECTION
                #if (timer + testCooldown < pygame.time.get_ticks()):
                #    cooldownElapsed += 1
                #    self.gameObjects["Player"].animator.GetClip("Walk").speedScale += 1
                #    timer = pygame.time.get_ticks()
            ###
            
            self.Update()
            self.Draw()
            pygame.draw.circle(self.screen, (255, 0, 0), self.tile, 70)
            self.draw_text_in_top_margin(str(self.hit)+":"+str(self.miss))
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
        
    def draw_text_in_top_margin(self, text):
        # Define font and size
        font = pygame.font.SysFont(None, 40)  # Default font with size 40
    
        # Render the text
        text_surface = font.render(text, True, (0, 0, 0))  # White color text
    
        # Calculate the position to center the text horizontally
        screen_width = self.screen.get_width()
        margin_top_bottom = 100
        text_rect = text_surface.get_rect(center=(screen_width // 2, margin_top_bottom // 2))
    
        # Blit (draw) the text onto the screen
        self.screen.blit(text_surface, text_rect)

    def get_random_xy_every_5_seconds(self):
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds

        # Check if 5 seconds (5000 ms) have passed since the last update
        if current_time - self.last_random_time >= 5000:
            # Update last random time
            self.last_random_time = current_time

            # Generate random (x, y) in range [0, 2]
            self.random_x = random.randint(0, 2)
            self.random_y = random.randint(0, 2)

        
        
if __name__ == '__main__':
    game = Game("setting.json")
    game.run_game()
    
        