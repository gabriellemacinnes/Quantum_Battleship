import pygame

# general colours
BLACK = (0, 0, 0)
DARK_GREY = (70, 70, 70)
LIGHT_GREY = (210, 210, 210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
SPECIAL_RED = pygame.Color("#CC5C42")
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# heat map colours
BLUE1 = pygame.Color("#08519C")
BLUE2 = pygame.Color("#2270B5")
BLUE3 = pygame.Color("#4192C5")
BLUE4 = pygame.Color("#6AAED6")
BLUE5 = pygame.Color("#9ECAE1")
BLUE6 = pygame.Color("#C6DAEF")
ORANGE1 = pygame.Color("#FFFFE4")
ORANGE2 = pygame.Color("#FFF7BB")
ORANGE3 = pygame.Color("#FEE391")
ORANGE4 = pygame.Color("#FEC34F")
ORANGE5 = pygame.Color("#FE9928")
ORANGE6 = pygame.Color("#EB7013")

# background
BACKGROUND_COLOR = WHITE

# screen dimensions
SCREEN_WIDTH = 1214
SCREEN_HEIGHT = 687
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# grid configurations
GRID_ROWS = 8
GRID_COLS = 8
GRID_PADDING = 1

# button configurations
BUTTON_WIDTH = 50
BUTTON_HEIGHT = 50
BUTTON_SIZE = (BUTTON_WIDTH, BUTTON_HEIGHT)

# grid dimensions
GRID_WIDTH = BUTTON_WIDTH * GRID_COLS + GRID_PADDING * (GRID_COLS - 1)
GRID_HEIGHT = BUTTON_HEIGHT * GRID_ROWS + GRID_PADDING * (GRID_ROWS - 1)

# button states
BUTTON_NORMAL = 'normal'
BUTTON_CLICKED = 'clicked'

# offset for grid placement
GRID_OFFSET_X = 120
GRID_OFFSET_Y = 200

# offset for heat map placement
HEAT_MAP_OFFSET_X = SCREEN_WIDTH // 2 + 2 * GRID_OFFSET_X // 3
HEAT_MAP_OFFSET_Y = GRID_OFFSET_Y