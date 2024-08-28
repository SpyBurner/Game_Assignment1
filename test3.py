import pygame
import pygame_gui

size = (1280, 720)
SCREEN_HEIGHT, SCREEN_WIDTH = size

pygame.init()

screen = pygame.display.set_mode(size)

#Load static background and scale up to screen
bg = pygame.image.load("front_night_crop.gif").convert_alpha()
fake_screen = pygame.Surface((bg.get_width(), bg.get_height()))
fake_screen.blit(bg, (0, 0))
screen.blit(pygame.transform.scale(fake_screen, screen.get_rect().size), (0, 0))

tileCount = (9, 5)

tile_dimensions = (100, 120)
tile_top_left = (300, 93)
tile_bottom_right = (tile_dimensions[0] * (tileCount[0]) + tile_top_left[0], tile_dimensions[1] * (tileCount[1]) + tile_top_left[1])

print("Top left: ", tile_top_left)
print("Bottom right: ", tile_bottom_right)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
            tile_x = (event.pos[0] - tile_top_left[0]) // tile_dimensions[0]
            tile_y = (event.pos[1] - tile_top_left[1]) // tile_dimensions[1]
            print("Tile: ", tile_x, " ", tile_y)
    
    pygame.display.update()
    
pygame.quit()