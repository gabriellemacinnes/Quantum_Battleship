import pygame
import sys
import config

def init_pygame():
    """Initializes Pygame and creates the game screen."""
    pygame.init()
    screen = pygame.display.set_mode(config.SCREEN_SIZE)
    pygame.display.set_caption("Battleship Game")
    return screen

def load_images():
    """Loads and transforms images to be used in the game."""
    target_image = pygame.image.load("assets/images/target.png")
    sea_image_width = (config.BUTTON_WIDTH * config.GRID_COLS) + (config.GRID_PADDING * (config.GRID_COLS - 1))
    sea_image_height = (config.BUTTON_HEIGHT * config.GRID_ROWS) + (config.GRID_PADDING * (config.GRID_ROWS - 1))
    sea_image = pygame.transform.scale(pygame.image.load("assets/images/sea.png"), (sea_image_width, sea_image_height))
    background_image = pygame.image.load("assets/images/background.png")
    background_image = pygame.transform.scale(background_image, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    return target_image, sea_image, background_image

def create_overlay(size, alpha, colour):
    """Creates a translucent overlay surface."""
    overlay = pygame.Surface(size)
    overlay.set_alpha(alpha)
    overlay.fill(colour)
    return overlay

def draw_button(surface, color, position, size):
    """Draws a button on the surface."""
    button_rect = pygame.Rect(position, size)
    pygame.draw.rect(surface, color, button_rect)
    return button_rect

def draw_indices(surface, offset_x, offset_y, font):
    """Draws the grid indices on the surface."""

    # Draw X-axis indices (capital letters)
    for i in range(config.GRID_COLS):
        letter = chr(65 + i)  # Converts number to capital letter (A-J)
        text_surf = font.render(letter, True, config.BLACK)
        # Centering the letter in the middle of the block
        text_rect = text_surf.get_rect(center=(offset_x + i * (config.BUTTON_WIDTH + config.GRID_PADDING) + config.BUTTON_WIDTH / 2, offset_y + config.GRID_ROWS * (config.BUTTON_HEIGHT + config.GRID_PADDING) + 20))
        surface.blit(text_surf, text_rect.topleft)

    # Draw Y-axis indices (numbers)
    for i in range(config.GRID_ROWS):
        number = str(config.GRID_ROWS - i)
        text_surf = font.render(number, True, config.BLACK)
        # Centering the number at the start of the row
        text_rect = text_surf.get_rect(center=(offset_x - 20, offset_y + i * (config.BUTTON_HEIGHT + config.GRID_PADDING) + config.BUTTON_HEIGHT / 2))
        surface.blit(text_surf, text_rect.topleft)

def create_grid_buttons(offset_x, offset_y):
    """Creates a grid of buttons for the game."""
    buttons = {}
    for row in range(config.GRID_ROWS):
        for col in range(config.GRID_COLS):
            button_pos = (offset_x + col * (config.BUTTON_WIDTH + config.GRID_PADDING),
                          offset_y + row * (config.BUTTON_HEIGHT + config.GRID_PADDING))
            buttons[(row, col)] = {
                'rect': pygame.Rect(button_pos, config.BUTTON_SIZE),
                'state': config.BUTTON_NORMAL  # Use the 'normal' state as default
            }
    return buttons

def main():
    # Set up the display, load images, and create the grid
    screen = init_pygame()
    target_image, sea_image, background_image = load_images()
    target_image_rect = target_image.get_rect()
    font = pygame.font.Font(None, 24)

    # Create a translucent grey overlay for the grid
    grid_background = create_overlay((config.GRID_WIDTH + 80, config.GRID_HEIGHT + 80), 150, config.LIGHT_GREY)

    # Create a translucent white overlay for the buttons
    button_overlay = create_overlay(config.BUTTON_SIZE, 175, config.BLACK)

    # Create grid buttons
    grid_buttons = create_grid_buttons(config.GRID_OFFSET_X, config.GRID_OFFSET_Y)

    running = True
    current_pos = [0, 0]
    discovered = set()  # Keep track of discovered squares

    while running:
        # Blit the full background image
        screen.blit(background_image, (0, 0))

        # Blit the translucent grey background for the grid onto the screen
        screen.blit(grid_background, (config.GRID_OFFSET_X - 40, config.GRID_OFFSET_Y - 40))

        # Blit the full sea image on the grid area
        screen.blit(sea_image, (config.GRID_OFFSET_X, config.GRID_OFFSET_Y))

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
                    # Convert the current position to a tuple for set operations and dict key
                    pos_key = tuple(current_pos)
                    if pos_key not in discovered:
                        discovered.add(pos_key)
                        grid_buttons[pos_key]['state'] = config.BUTTON_CLICKED

        # Draw the indices for the grid
        draw_indices(screen, config.GRID_OFFSET_X, config.GRID_OFFSET_Y, font)

        # Draw the grid buttons
        for pos_key, button_data in grid_buttons.items():
            button_rect = button_data['rect']
            if pos_key not in discovered:
                # If the button has not been discovered, draw the button overlay
                screen.blit(button_overlay, button_rect.topleft)

        # Update the position of the target image and draw it
        target_image_rect.topleft = grid_buttons[tuple(current_pos)]['rect'].topleft
        screen.blit(target_image, target_image_rect.topleft)

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Run the game
if __name__ == "__main__":
    main()