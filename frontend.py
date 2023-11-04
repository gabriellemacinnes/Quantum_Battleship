import pygame
import sys
import config

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode(config.SCREEN_SIZE)
pygame.display.set_caption("Battleship Game")

# Font for the indices
font = pygame.font.Font(None, 24)

# Colors for button states
BUTTON_NORMAL = config.GREY
BUTTON_HOVER = config.BLUE
BUTTON_CLICKED = config.RED
BUTTON_BLINK = config.WHITE  # Define a blink color

# Function to draw buttons
def draw_button(surface, color, position, size):
    button_rect = pygame.Rect(position, size)
    pygame.draw.rect(surface, color, button_rect)
    return button_rect

def draw_indices(surface, offset_x, offset_y):
    # Draw X-axis indices (capital letters)
    for i in range(config.GRID_COLS):
        letter = chr(65 + i)  # Converts number to capital letter (A-J)
        text_surf = font.render(letter, True, config.WHITE)
        # Centering the letter in the middle of the block
        text_rect = text_surf.get_rect(center=(offset_x + i * (config.BUTTON_WIDTH + config.GRID_PADDING) + config.BUTTON_WIDTH / 2, offset_y + config.GRID_ROWS * (config.BUTTON_HEIGHT + config.GRID_PADDING) + 20))
        surface.blit(text_surf, text_rect.topleft)

    # Draw Y-axis indices (numbers)
    for i in range(config.GRID_ROWS):
        number = str(config.GRID_ROWS - i)
        text_surf = font.render(number, True, config.WHITE)
        # Centering the number at the start of the row
        text_rect = text_surf.get_rect(center=(offset_x - 20, offset_y + i * (config.BUTTON_HEIGHT + config.GRID_PADDING) + config.BUTTON_HEIGHT / 2))
        surface.blit(text_surf, text_rect.topleft)

# Function to create the grid and store button states
def create_grid(offset_x, offset_y):
    buttons = {}
    for row in range(config.GRID_ROWS):
        for col in range(config.GRID_COLS):
            button_pos = (offset_x + col * (config.BUTTON_WIDTH + config.GRID_PADDING),
                          offset_y + row * (config.BUTTON_HEIGHT + config.GRID_PADDING))
            buttons[(row, col)] = {
                'rect': pygame.Rect(button_pos, config.BUTTON_SIZE),
                'state': BUTTON_NORMAL
            }
    return buttons

# Main loop
def main():
    running = True

    # Create the grid of buttons
    grid_buttons = create_grid(config.GRID_OFFSET_X, config.GRID_OFFSET_Y)

    # Draw the indices for the grid
    draw_indices(screen, config.GRID_OFFSET_X, config.GRID_OFFSET_Y)

    current_pos = [0, 0]  # Start at the top-left of the grid
    blink_state = True  # State to make the button blink
    blink_timer = pygame.time.get_ticks()

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_pos[1] = max(current_pos[1] - 1, 0)
                elif event.key == pygame.K_RIGHT:
                    current_pos[1] = min(current_pos[1] + 1, config.GRID_COLS - 1)
                elif event.key == pygame.K_UP:
                    current_pos[0] = max(current_pos[0] - 1, 0)
                elif event.key == pygame.K_DOWN:
                    current_pos[0] = min(current_pos[0] + 1, config.GRID_ROWS - 1)
                elif event.key == pygame.K_RETURN:
                    button_data = grid_buttons[tuple(current_pos)]
                    if button_data['state'] == BUTTON_NORMAL:
                        button_data['state'] = BUTTON_CLICKED  # Set the button as clicked

        # Blinking logic
        current_time = pygame.time.get_ticks()
        if current_time - blink_timer > 500:  # Blink every half a second
            blink_timer = current_time
            blink_state = not blink_state

        # Drawing the grid
        for button_pos, button_data in grid_buttons.items():
            if button_data['state'] != BUTTON_CLICKED:
                if button_pos == tuple(current_pos) and blink_state:
                    draw_button(screen, BUTTON_BLINK, button_data['rect'].topleft, config.BUTTON_SIZE)
                else:
                    draw_button(screen, button_data['state'], button_data['rect'].topleft, config.BUTTON_SIZE)
            else:
                draw_button(screen, BUTTON_CLICKED, button_data['rect'].topleft, config.BUTTON_SIZE)

        # Redraw the screen
        pygame.display.update()

    pygame.quit()
    sys.exit()

# Run the game
if __name__ == "__main__":
    main()