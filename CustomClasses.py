import copy
import pygame
import os

class GameObject:
    ##
    #
    #@param name: The name of the GameObject
    #@param position: The position of the GameObject in the form of a tuple (x, y)
    #@param rotation: The rotation of the GameObject in the form of a float (Degrees along Z axis only)
    #@param scale: The scale of the GameObject in the form of a tuple (x, y)
    #@param animClips: List of AnimationClips
    ##
    def __init__(self, name, position, rotation, scale, animClips):
        self.name = name
        
        #Transform
        self.position = position
        self.rotation = rotation
        self.scale = scale
        
        #Sprite
        self.sprite = pygame.sprite.Sprite()
        #Animator
        self.animator = Animator(self, animClips)

    def Update(self):
        self.animator.Update()
        
    def Draw(self, screen):
        sprite_size = self.sprite.image.get_rect().size
        
        #Apply scale
        transformed_sprite = pygame.transform.scale(self.sprite.image, (int(sprite_size[0] * self.scale[0]), int(sprite_size[1] * self.scale[1])))
        
        #Apply rotation
        transformed_sprite = pygame.transform.rotate(transformed_sprite, self.rotation)
        
        offset_x = transformed_sprite.get_rect().size[0] / 2
        offset_y = transformed_sprite.get_rect().size[1] / 2
        
        actualPos = (self.position[0] - offset_x, self.position[1] - offset_y)
        
        screen.blit(transformed_sprite, actualPos)
        
    @staticmethod
    def Instantiate(name, original, position, rotation):
        return GameObject(name, position, rotation, original.scale, copy.deepcopy(original.animator.GetAllClips()))
    
class AnimationClip:
    
    def __init__(self, path, name, loop, length, speedScale):
        self.path = path
        self.name = name
        self.loop = loop
        self.length = length
        self.isPlaying = False
        
        self.sprites = self.GetSpritesFromPath(path)
        self.current_sprite = 0
        
        self.speedScale = speedScale
        self.animCooldown = length/len(self.sprites)
        self.lastFrameTime = pygame.time.get_ticks()
        self.startTime = pygame.time.get_ticks()
        
        #For transition
        self.onComplete = Event()
        
    def AdvanceFrame(self):
        #Cooldown check
        if not self.isPlaying or (self.lastFrameTime + self.animCooldown / self.speedScale) > pygame.time.get_ticks():
            return
        
        #Animation length check
        if (self.startTime + self.length) < pygame.time.get_ticks():
            self.isPlaying = False
            self.onComplete()
            return
        
        #Advance frame logic
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            if self.loop:
                #Loop enabled
                self.current_sprite = 0
            else:
                #Loop disabled
                self.current_sprite = len(self.sprites) - 1
                self.isPlaying = False
                self.onComplete()
        
        #Set new last frame time
        self.lastFrameTime = pygame.time.get_ticks()
    
    @staticmethod
    def GetSpritesFromPath(path):
        sprites = []
        for filename in os.listdir(path):
            sprites.append(pygame.image.load(os.path.join(path, filename)).convert_alpha())
        return sprites
    
    def Ready(self):
        self.current_sprite = 0
        self.isPlaying = True
        self.startTime = pygame.time.get_ticks()
        self.lastFrameTime = pygame.time.get_ticks() - self.animCooldown * self.speedScale
        

class Animator:
    def __init__(self, gameObject, clips):
        self.gameObject = gameObject
        
        self.clips = {}
        if (len(clips) > 0):
            for clip in clips:
                self.clips[clip.name] = clip
            
            #Fail safe assignment
            self.current_clip = clips[0]
            self.Play(clips[0].name)
    
    def GetCurrentClip(self):
        return self.current_clip
    
    def GetClip(self, clipName):
        return self.clips[clipName]
    
    def GetAllClips(self):
        return list(self.clips.values())
    
    def Play(self, clipName):
        #Stop previous clip
        self.current_clip.isPlaying = False
        
        #Play new clip
        self.current_clip = self.clips[clipName]
        self.current_clip.Ready()
        
    def Update(self):
        self.current_clip.AdvanceFrame()
        self.gameObject.sprite.image = self.current_clip.sprites[self.current_clip.current_sprite]

#Copilot :))
class Event:
    def __init__(self):
        self.handlers = []

    def __iadd__(self, handler):
        self.handlers.append(handler)
        return self

    def __call__(self, *args, **kwargs):
        for handler in self.handlers:
            handler(*args, **kwargs)