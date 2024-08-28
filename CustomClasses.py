import pygame
import os

class GameObject:
    ##
    #
    #@param name: The name of the GameObject
    #@param position: The position of the GameObject in the form of a tuple (x, y)
    #@param rotation: The rotation of the GameObject in the form of a float (Degrees along Z axis only)
    #@param scale: The scale of the GameObject in the form of a tuple (x, y)
    ##
    def __init__(self, name, position, rotation, scale, animPaths, animLoop):
        self.name = name
        
        #Transform
        self.position = position
        self.rotation = rotation
        self.scale = scale
        
        #Sprite
        self.sprite = pygame.sprite.Sprite()
        
        ##Load clips for animator
        clips = []
        for i in range(len(animPaths)):
            animPath = animPaths[i]
            clips.append(AnimationClip(animPath, os.path.basename(animPath), animLoop[i]))
        
        #Animator
        self.animator = Animator(self, clips)

    def Update(self):
        self.animator.Update()
        
    def Draw(self, screen):
        sprite_size = self.sprite.image.get_rect().size
        screen.blit(pygame.transform.scale(self.sprite.image, (sprite_size[0] * self.scale[0], sprite_size[1] * self.scale[1])), self.position)

class AnimationClip:
    
    def __init__(self, path, name, loop):
        self.path = path
        self.name = name
        self.speedScale = 1
        self.loop = loop
        
        self.sprites = self.GetSpritesFromPath(path)
        self.current_sprite = 0
    
    @staticmethod
    def GetSpritesFromPath(path):
        sprites = []
        for filename in os.listdir(path):
            sprites.append(pygame.image.load(os.path.join(path, filename)).convert_alpha())
        return sprites

class Animator:
    def __init__(self, gameObject, clips):
        self.gameObject = gameObject
        
        self.clips = {}
        for clip in clips:
            self.clips[clip.name] = clip
                    
        self.current_clip = self.clips[clips[0].name]
    
    def Play(self, clipName):
        self.current_clip = self.clips[clipName]
        self.current_clip.current_sprite = 0
        
    def Update(self):
        self.current_clip.current_sprite += 1
        if self.current_clip.current_sprite >= len(self.current_clip.sprites):
            if self.current_clip.loop:
                self.current_clip.current_sprite = 0
            else:
                self.current_clip.current_sprite = len(self.current_clip.sprites) - 1
        # self.gameObject.sprite = self.current_clip.sprites[self.current_clip.current_sprite]
        self.gameObject.sprite.image = self.current_clip.sprites[self.current_clip.current_sprite]