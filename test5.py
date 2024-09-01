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
        
        self.ZOMB_MAP = {}
        
        self.hit = 0
        self.miss = 0
        self.random_x = 0
        self.random_y = 0
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                
        #GameObject list
        self.gameObjects = {}
        
        #Sound effect
        self.hit_sound = pygame.mixer.Sound("Assets\\SFX\\hit.wav")
        self.up_sound = pygame.mixer.Sound("Assets\\SFX\\up.wav")
        self.miss_sound = pygame.mixer.Sound("Assets\\SFX\\miss.wav")
        
        self.hit_sound.set_volume(2)
        self.up_sound.set_volume(2)
        self.miss_sound.set_volume(1)
                
    def run_game(self):
        
        ###TEST SECTION
        linkUpAnim = AnimationClip("Assets\\Sprites\\Link_Up", "Up", False, 500)
        linkDownAnim = AnimationClip("Assets\\Sprites\\Link_Down", "Down", False, 500)
        linkIdleAnim = AnimationClip("Assets\\Sprites\\Link_Idle", "Idle", False, 1000)
        linkHitAnim = AnimationClip("Assets\\Sprites\\Link_Hit", "Hit", False, 500)
                
        linkPrefab = GameObject("prefab", (-100, -100), 0, (3, 3), [linkUpAnim, linkIdleAnim, linkHitAnim, linkDownAnim])
        
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
                    #Hit tile check
                    tile = self.get_tile(event.pos[0], event.pos[1])            
                            
                    if (tile == (-1,-1) or self.SquareDistance(event, self.CIRCLE_COORDINATE[tile[0]][tile[1]]) > 4900):
                        print("miss 1: clicked out side of circle")
                        self.miss += 1
                        self.miss_sound.play()
                    else:          
                        #Hit zomb check    
                        if (not tile in self.ZOMB_MAP):
                            print("miss 2: clicked empty tile")
                            self.miss += 1
                            self.miss_sound.play()
                        else:
                            #Zomb is hitable check
                            zom = self.ZOMB_MAP[tile]
                            #Hitable on UP or IDLE state
                            if zom.animator.GetClip("Down").isPlaying:
                                print("miss 3: clicked zomb late")
                                self.miss += 1
                                self.miss_sound.play()
                            elif zom.animator.GetClip("Hit").isPlaying:
                                print("no action: clicked already hit zomb")
                                continue                               
                            else:
                                print("hit")
                                self.hit_sound.play()
                                zom.animator.Play("Hit")
                        

            if (self.get_random_xy_every_5_seconds()):
                newObjectTile = (self.random_x, self.random_y)
                newObjectPos = self.CIRCLE_COORDINATE[newObjectTile[0]][newObjectTile[1]]
                
                if not newObjectTile in self.ZOMB_MAP:
                    newObjectName = "Zomb" + str(pygame.time.get_ticks())
                    newObject = GameObject.Instantiate(newObjectName, linkPrefab, newObjectPos, 0)
                    
                    newObject.animator.GetClip("Up").onComplete += lambda: newObject.animator.Play("Idle")
                    newObject.animator.GetClip("Idle").onComplete += lambda: newObject.animator.Play("Down")
                    newObject.animator.GetClip("Hit").onComplete += lambda: self.OnZombHitEnd(newObject)
                    newObject.animator.GetClip("Down").onComplete += lambda: self.OnZombEscape(newObject)
                    
                    self.gameObjects[newObject.name] = newObject
                    self.ZOMB_MAP[newObjectTile] = newObject
                    
                    self.up_sound.play()
                else:
                    self.last_random_time -= 5000
            self.Update()
            self.Draw()
            
            self.draw_text_in_top_margin(str(self.hit)+":"+str(self.miss))
            pygame.display.update()
            
        pygame.quit()

    def SquareDistance(self, pointA, pointB):
        return (pointA.pos[0]-pointB[0]) * (pointA.pos[0]-pointB[0])  + (pointA.pos[1]-pointB[1]) * (pointA.pos[1]-pointB[1])
    
    def OnZombHitEnd(self, gameObject):
        self.Destroy(gameObject)
        self.hit += 1
    
    def OnZombEscape(self, gameObject):
        self.miss_sound.play()
        self.Destroy(gameObject)
        self.miss += 1
    
    def Update(self):
        gameObjects = list(self.gameObjects.values())
        for gameObject in gameObjects:
            gameObject.Update()
            
    def Destroy(self, gameObject):
        if (gameObject.name in self.gameObjects):
            self.gameObjects.pop(gameObject.name)
            
        tile = self.get_tile(gameObject.position[0], gameObject.position[1])  
        if (tile in self.ZOMB_MAP):
            self.ZOMB_MAP.pop(tile)

    def draw_circle_matrix(self):
        radius = 70
        for row in range(3):
            for col in range(3):
                # Draw the circle on the screen
                pygame.draw.circle(self.screen, (0, 0, 0), self.CIRCLE_COORDINATE[row][col], radius)
    def Draw(self):
        gameObjects = list(self.gameObjects.values())
        for gameObject in gameObjects:
            gameObject.Draw(self.screen)
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
            return (-1,-1)  # Outside the grid

        # Calculate the column and row based on the position inside the grid
        c = (x - margin_left_right) // tile_size
        r = (y - margin_top_bottom) // tile_size

        return (r, c)
        
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

            return True
        
        return False

        
        
if __name__ == '__main__':
    game = Game("setting.json")
    game.run_game()
    
        