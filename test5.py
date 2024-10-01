import json
from math import fabs
import time
from xml.etree.ElementTree import tostring
import pygame
import random
import pygame_gui
from CustomClasses import *

class Game:
    def __init__(self, settingsPath):
        settingFile = open(settingsPath)
        self.settingData = json.load(settingFile)
        
        #Pygame init
        pygame.init()
        pygame.display.set_caption("Game")
        pygame.time.Clock().tick(self.settingData["FPS"])
        
        #Screen init
        SCREEN_WIDTH = self.settingData["SCREEN_WIDTH"]
        SCREEN_HEIGHT = self.settingData["SCREEN_HEIGHT"]     
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Scenes
        self.sceneManager = SceneManager()
        
        scene1 = Scene("Gameplay", {})
        scene1.logic =  lambda: self.GameplaySceneLogic(scene1)
        
        scene2 = Scene("Restart", {})
        scene2.logic = lambda: self.RestartSceneLogic(scene2)
        
        self.sceneManager.AddScene(scene1)
        self.sceneManager.AddScene(scene2)

        self.sceneManager.LoadScene("Gameplay")

    def GameplaySceneLogic(self, scene):
        ###Scene variables
        CIRCLE_COORDINATE = [[(100, 150), (250, 150), (400, 150)], [(100, 300), (250, 300), (400, 300)], [(100, 450), (250, 450), (400, 450)]]
        
        ZOMB_MAP = {}
        for row in range(3):
            for col in range(3):
                ZOMB_MAP[(row, col)] = None
        
        hit = 0
        miss = 0
        
        #Circles matrix init
        radius = self.settingData["CIRCLE_RADIUS"]
        
        #Sound effect
        hit_sound = pygame.mixer.Sound("Assets\\SFX\\hit.wav")
        up_sound = pygame.mixer.Sound("Assets\\SFX\\up.wav")
        miss_sound = pygame.mixer.Sound("Assets\\SFX\\miss.wav")
        
        hit_sound.set_volume(2)
        up_sound.set_volume(2)
        miss_sound.set_volume(1)
        
        #Load all assets
        zombUpAnim = AnimationClip("Assets\\Sprites\\Zombie_Up", "Up", False, 500, 1)
        zombDownAnim = AnimationClip("Assets\\Sprites\\Zombie_down", "Down", False, 500, 1)
        zombIdleAnim = AnimationClip("Assets\\Sprites\\Zombie_idle", "Idle", True, 3000, 4.5)
        zombHitAnim = AnimationClip("Assets\\Sprites\\Zombie_hit", "Hit", False, 500, 1)
                
        zombPrefab = GameObject("prefab", (-100, -100), 0, (3, 3), [zombUpAnim, zombIdleAnim, zombHitAnim, zombDownAnim])
        
        flower1Anim = AnimationClip("Assets\\Sprites\\Flower1", "Flower1", True, 1000, 1)
        flower2Anim = AnimationClip("Assets\\Sprites\\Flower2", "Flower2", True, 1000, 1)
        flower3Anim = AnimationClip("Assets\\Sprites\\Flower3", "Flower3", True, 1000, 1)
        
        flowerPrefab = GameObject("flowerPrefab", (-100, -100), 0, (1, 1), [flower1Anim, flower2Anim, flower3Anim])
        
        
        last_random_time = pygame.time.get_ticks()
                
        ###Local methods
        def OnZombDestroy(gameObject):
            tile = get_tile(gameObject.position[0], gameObject.position[1])  
            if (ZOMB_MAP[tile] != None):
                ZOMB_MAP[tile] = None       
        
        def OnZombHitEnd(gameObject):
            self.Destroy(gameObject, scene)
            OnZombDestroy(gameObject)
                
        def OnZombEscape(gameObject):
            nonlocal miss
            
            miss_sound.play()
            self.Destroy(gameObject, scene)
            OnZombDestroy(gameObject)
            
            miss += 1
        
        def draw_circle_matrix():
            for row in range(3):
                for col in range(3):
                    # Draw the circle on the screen
                    pygame.draw.circle(self.screen, (0, 0, 0), CIRCLE_COORDINATE[row][col], radius)
                           
        def get_tile(x, y):
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
        
        #Only get available tiles
        def get_random_xy_every_5_seconds():
            nonlocal last_random_time
            
            current_time = pygame.time.get_ticks()  # Get current time in milliseconds
            # Check if 5 seconds (5000 ms) have passed since the last update
            if current_time - last_random_time < self.settingData["SPAWN_INTERVAL"]:
                return None
            
            # Cooldown passed, continue
            available_tiles = []
            for tile, value in ZOMB_MAP.items():
                if value is None:
                    available_tiles.append(tile)
        
            # Check if there are available tiles
            if len(available_tiles) <= 0:
                return None
            
            # Update last random time
            last_random_time = current_time
            return random.choice(available_tiles)

        #Spawn in random background flowers
        for i in range(self.settingData["FLOWER_COUNT"]):
            screenSize = self.screen.get_size()
            flowerPos = (random.randrange(0, screenSize[0]), random.randrange(0, screenSize[1]))
            
            newFlowerObject = GameObject.Instantiate("Flower"+str(i), flowerPrefab, flowerPos, 0)
            
            #Choose random sprite as single-frame animation
            newFlowerObject.animator.Play(random.choice(newFlowerObject.animator.GetAllClips()).name)

            scene.gameObjects[newFlowerObject.name] = newFlowerObject
        
        ###Main logic
        run = True
        while run:
            self.screen.fill(self.settingData["GAMEPLAY_BG_COLOR"])  # Fill the screen with white
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #Hit tile check
                    tile = get_tile(event.pos[0], event.pos[1])            
                            
                    if (tile == (-1,-1) 
                    or self.SquareDistance(event, CIRCLE_COORDINATE[tile[0]][tile[1]]) > radius * radius):
                        print("miss 1: clicked out side of circles")
                        miss += 1
                        miss_sound.play()
                    else:          
                        #Hit zomb check    
                        if (ZOMB_MAP[tile] == None):
                            print("miss 2: clicked empty tile")
                            miss += 1
                            miss_sound.play()
                        else:
                            #Zomb is hitable check
                            zom = ZOMB_MAP[tile]
                            #Hitable on UP or IDLE state
                            if zom.animator.GetClip("Down").isPlaying:
                                print("miss 3: clicked zomb late")
                                miss += 1
                                miss_sound.play()
                            elif zom.animator.GetClip("Hit").isPlaying:
                                print("no action: clicked on already hit zomb")
                                continue                               
                            else:
                                print("hit")
                                hit_sound.play()
                                zom.animator.Play("Hit")
                                hit += 1
            ###Lose condition interupt
            if (miss >= 3):
                run = False
                self.sceneManager.LoadScene("Restart")
                return True
            ###
            newObjectTile = get_random_xy_every_5_seconds()        
            if (newObjectTile != None):
                newObjectPos = CIRCLE_COORDINATE[newObjectTile[0]][newObjectTile[1]]
                
                if ZOMB_MAP[newObjectTile] == None:
                    newObjectName = "Zomb" + str(pygame.time.get_ticks())
                    newObject = GameObject.Instantiate(newObjectName, zombPrefab, newObjectPos, 0)
                    
                    newObject.animator.GetClip("Up").onComplete += lambda obj=newObject: obj.animator.Play("Idle")
                    newObject.animator.GetClip("Idle").onComplete += lambda obj=newObject: obj.animator.Play("Down")
                    newObject.animator.GetClip("Hit").onComplete += lambda obj=newObject: OnZombHitEnd(obj)
                    newObject.animator.GetClip("Down").onComplete += lambda obj=newObject: OnZombEscape(obj)
                    
                    scene.gameObjects[newObject.name] = newObject
                    ZOMB_MAP[newObjectTile] = newObject
                    
                    up_sound.play()

            # Update
            scene.Update()
            
            #Draw

            draw_circle_matrix()     # Draw the circle matrix
            
            ##self.draw_text_in_top_margin("Hit: " + str(hit)+" / Miss: "+str(miss), self.screen)
            
            scene.Draw(self.screen)
            self.draw_text_in_top_margin("Hit: " + str(hit)+" / Miss: "+str(miss), self.screen)
            
            pygame.display.update()
            
        #Stop the outer loop
        return False
    
    def RestartSceneLogic(self, scene):
        button_pos = self.screen.get_bounding_rect().center
        print("button pos: " + str(button_pos[0]) + " " + str(button_pos[1]))
        
        restart_icon_image = AnimationClip("Assets\\Sprites\\Restart_Icon", "Restart", False, 1, 1)
        restart_button = GameObject("RestartButton", button_pos, 0, (0.5, 0.5), [restart_icon_image])
               
        scene.gameObjects[restart_button.name] = restart_button
        
        def CheckButtonClick(button, pos):
            button_center = button.GetActualRect().center
            print("button pos: " + str(button_center[0]) + " " + str(button_center[1]))
            print("click: " + str(pos[0]) + " " + str(pos[1]))
            return button.CheckCollisionPoint(pos)
        
        run = True
        while run:
            self.screen.fill((255, 255, 255))  # Fill the screen with white
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.circle(self.screen, (0, 0, 0), event.pos, 10)
                    if CheckButtonClick(restart_button, event.pos):
                        run = False
                        self.sceneManager.LoadScene("Gameplay")
                        return True
                    
            scene.Update()
            

            self.draw_text_in_top_margin("Game Over", self.screen)
            
            scene.Draw(self.screen)
            
            pygame.display.update()
    
        return False

    def run_game(self):
               
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            run = self.sceneManager.RunScene()
        pygame.quit()

    def draw_text_in_top_margin(self, text, screen):
        # Define font and size
        font = pygame.font.SysFont(None, 40)  # Default font with size 40
    
        # Render the text
        text_surface = font.render(text, True, (255, 255, 255))  # White color text
    
        # Calculate the position to center the text horizontally
        screen_width = screen.get_width()
        margin_top_bottom = 100
        text_rect = text_surface.get_rect(center=(screen_width // 2, margin_top_bottom // 2))
    
        # Blit (draw) the text onto the screen
        screen.blit(text_surface, text_rect)

    def SquareDistance(self, pointA, pointB):
        return (pointA.pos[0]-pointB[0]) * (pointA.pos[0]-pointB[0])  + (pointA.pos[1]-pointB[1]) * (pointA.pos[1]-pointB[1])
            
    def Destroy(self, gameObject, scene):
        if (gameObject.name in scene.gameObjects):
            scene.gameObjects.pop(gameObject.name)
            return True
        return False 
        
        
if __name__ == '__main__':
    game = Game("setting.json")
    game.run_game()
    
        