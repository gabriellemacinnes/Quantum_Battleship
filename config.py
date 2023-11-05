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
BACKGROUND_COLOUR = WHITE

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

# inventory of sayings
ENTANGLEMENT_HIT_MESSAGES = [
    "Yarrr! A double strike scored!",
    "Two for one! Sea's favour, mate!",
    "Shots twain, both hit the mark!",
    "Entangled foes meet their fate!",
    "Two scallywags down in a blink!",
    "Aye! Two ships to Davy Jones!",
    "Fortune smiles with a twin hit!",
    "Twin victories in the blue vast!",
    "Luck of the Kraken be ours!",
    "Poseidon graces with double hits!"
]
SHIP_HIT_MESSAGES = [
    "Hit confirmed! They're taking water!",
    "Cannon's roar brings a hit!",
    "Target down! They'll remember us!",
    "Aye, their fleet feels our sting!",
    "Another scurvy ship sleeps with fish!",
    "A hit! Their defeat looms nigh!",
    "A crippling blow to the foe!",
    "Send 'em to the abyss!",
    "They'll be leakin' now, captain!",
    "Strike true! They flounder!"
]
ENTANGLEMENT_MISS_MESSAGES = [
    "Missed, but the sea's vast with promise!",
    "Two misses, but fate's wheel turns!",
    "The waves claim our shot, but hope stays!",
    "Misses cast, but our luck's still in!",
    "The ocean swallows our fury, yet we sail on!",
    "Missed, yet the tides may yet turn!",
    "Sea swallows our bravado twice, but not our spirit!",
    "Twice the water, twice the resolve!",
    "Two shots astray, but our course holds true!",
    "The deep denies us, but we'll not waver!"
]
SHIP_MISS_MESSAGES = [
    "Shot to the sea, but our aim will true!",
    "Arrr, missed. Reload, mates!",
    "The deep blue hides them well!",
    "Missed by a whisker! Ready again!",
    "A miss, yet the fight's not done!",
    "We missed the mark! All hands, brace!",
    "Unscathed, but our resolve's ironclad!",
    "Our aim needs the hawk's eye!",
    "The enemy ship evades, not for long!",
    "The sea remains untamed. Fire!"
]
QUANTUM_MESSAGES = [
    "Quantum sight reveals the hidden!",
    "The threads of fate show their weave!",
    "What once was hidden, now is clear!",
    "Revealed! The sea yields her truths!",
    "Fortune's quantum tide favours us!",
    "The shrouded veil lifts with sight!",
    "Stars align, showing the hidden path!",
    "Into the quantum deep, insight's gleaned!",
    "Our path's clear as the fates unveil!",
    "Fate's whisper reveals the obscured!"
]