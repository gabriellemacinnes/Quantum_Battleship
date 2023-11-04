import pygame
import sys
import config

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode(config.SCREEN_SIZE)
pygame.display.set_caption("Battleship Game")

# Colors for button states
BUTTON_NORMAL = config.GREY
BUTTON_HOVER = config.BLUE
BUTTON_CLICKED = config.RED

# Function to draw buttons
def draw_button(surface, color, position, size):
    button_rect = pygame.Rect(position, size)
    pygame.draw.rect(surface, color, button_rect)
    return button_rect

# Main loop
def main():
    running = True
    buttons = {}

    # Create a grid of buttons
    for row in range(config.GRID_ROWS):
        for col in range(config.GRID_COLS):
            button_pos = (config.GRID_OFFSET_X + col * (config.BUTTON_WIDTH + config.GRID_PADDING),
                          config.GRID_OFFSET_Y + row * (config.BUTTON_HEIGHT + config.GRID_PADDING))
            buttons[(row, col)] = draw_button(screen, BUTTON_NORMAL, button_pos, config.BUTTON_SIZE)

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for button_pos, button_rect in buttons.items():
                    if button_rect.collidepoint(mouse_pos):
                        # Change button color to show it's been clicked
                        draw_button(screen, BUTTON_CLICKED, button_rect.topleft, config.BUTTON_SIZE)

        # Redraw the screen
        pygame.display.update()

    pygame.quit()
    sys.exit()

# Run the game
if __name__ == "__main__":
    main()