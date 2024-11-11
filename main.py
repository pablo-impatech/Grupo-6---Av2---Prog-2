import pygame

from math import floor
from forest_fire.model import ForestFire

# pygame setup
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

SPRITES = {
    "Fine": "forest_fire/resources/fine_tree.png",
    "On Fire": "forest_fire/resources/fire.png",
    "Burned Out": "forest_fire/resources/burned_tree.png"
}

# Grid proportions
GRID_HEIGHT = 25
CELL_SIZE = SCREEN_HEIGHT/GRID_HEIGHT
GRID_WIDTH = floor(SCREEN_WIDTH/CELL_SIZE)

# Start model
model = ForestFire(GRID_WIDTH, GRID_HEIGHT, 0.4, True, 0.005)

fine_tree_img = pygame.image.load(SPRITES["Fine"])
fine_tree_img = pygame.transform.scale(fine_tree_img, (CELL_SIZE, CELL_SIZE))

fire_img = pygame.image.load(SPRITES["On Fire"])
fire_img = pygame.transform.scale(fire_img, (CELL_SIZE, CELL_SIZE))

burned_tree_img = pygame.image.load(SPRITES["Burned Out"])
burned_tree_img = pygame.transform.scale(burned_tree_img, (CELL_SIZE, CELL_SIZE))

# Events
TIMEREVENTFIRE = pygame.USEREVENT + 1
pygame.time.set_timer(TIMEREVENTFIRE, 1000) # Fire iterations by milliseconds

def draw_scene():
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            tree = model.grid[i][j]
            if tree:
                if tree.condition == "Fine":
                    img = fine_tree_img
                elif tree.condition == "On Fire":
                    img = fire_img
                elif tree.condition == "Burned Out":
                    img = burned_tree_img

                screen.blit(img, (i * CELL_SIZE, j * CELL_SIZE))

while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == TIMEREVENTFIRE:
            model.step()

    # Screen background color
    screen.fill("white")

    # Draw scene
    draw_scene()
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60) # limits FPS to 60

pygame.quit()
