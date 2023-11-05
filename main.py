import pygame
import sys
import config
import random
import qiskit as qk
from pygame.locals import *
from utils import *

qc = generate_board(8, 15, 1)
shots = 1024


def init_pygame():
    """Initializes Pygame and creates the game screen."""
    pygame.init()
    screen = pygame.display.set_mode(config.SCREEN_SIZE)
    pygame.display.set_caption("Battleship Game")
    return screen

def classic(pos):
    x, y = pos
    circ = qc[x]
    circ.measure(y, y)
    simulator = qk.Aer.get_backend('qasm_simulator')
    result = qk.execute(circ, simulator, shots=1).result()
    counts = result.get_counts(circ)
    for key in counts:
        return int(key[y])
 
def get_prob(row):
    circuit = qc[row]
    circuit.measure_all()
    simulator = qk.Aer.get_backend('qasm_simulator')
    result = qk.execute(circuit, simulator, shots=1024).result()
    counts = result.get_counts(circuit)
    prob = [0 for _ in range(8)]
    for key in counts:
        for k in range(8):
            if int(key[k]) == 1:
                prob[k] += counts[key]
    for k in range(8):

        prob[k] = str(round(100 * prob[k]/shots))
    return prob

def create_window(screen):
    """Opens a modal window atop the game displaying some text."""
    instructions_surface = pygame.Surface((1175, 500))
    instructions_surface.fill(config.LIGHT_GREY)  # Set the background color
    font = pygame.font.Font(None, 36)
    text_lines = [
        "Ahoy, Quantum Commander! Prepare to set sail on a mind-bending ",
        "voyage through the fabric of spacetime as we engage in Quantum Battleship,",
        "where uncertainty and strategy collide in an epic duel across the quantum realm.",
        "Ready your fleet and navigate the uncertain waters of superposition as we embark on a journey ",
        "that defies the laws of classical warfare!",
        "Your mission, valiant commander, is to lay waste to a fleet of 10 enemy battleships", 
        "using the enigmatic weaponry of classical and quantum cannons." ,
        "Take heed, for these are not regular battleships. ",
        "They exist in states of superposition across the vast ocean.",
        "Use the space bar to toggle between classical cannons and enigmatic quantum cannons, "
        "and press enter to unleash their fury.",
        "Classical cannons, unveil the true nature of a single square",
        "Quantum cannons shall illuminate the probabilities of four adjacent grid squares. ",
        "Beware of the entangled battleships, for firing upon one shall unveil the destiny of its counterpart." ,
        "To gain further insights, toggle the image on the right to reveal the ",
        "intricate heat map of probabilities. ",
        "Best of luck, intrepid commander,"
        "may your valor and determination guide you to triumph on these tumultuous quantum seas. "
        "Press any key to close this window and return to the game."
    ]
    text_y = 30

    for line in text_lines:
        text = font.render(line, True, config.DARK_GREY)
        text_rect = text.get_rect(center=(instructions_surface.get_width() // 2, text_y))
        instructions_surface.blit(text, text_rect)
        text_y += 40

    # Create a clock to control frame rate
    clock = pygame.time.Clock()
    is_open = True

    while is_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                main_menu(screen)

        screen.blit(instructions_surface, (20, 20))  # Position the window on the screen
        pygame.display.flip()
        clock.tick(60)

    # Clear the window's contents
    instructions_surface.fill(config.LIGHT_GREY)

            

def main_menu(screen):
    """Displays the main menu with custom buttons for starting the game or viewing instructions."""
    # Load images and sounds
    _, _, background_image, scroll_image, _, _, _ = load_images()
    click_sound, _, _ = load_sounds()
    
    # Define the fonts
    title_font = pygame.font.Font("assets/fonts/OpenSans-VariableFont_wdth,wght.ttf", 70)
    title_font.set_bold(True)
    subtitle_font = pygame.font.Font("assets/fonts/OpenSans-VariableFont_wdth,wght.ttf", 30)
    button_font = pygame.font.Font("assets/fonts/OpenSans-VariableFont_wdth,wght.ttf", 20)

    # Create the title and subtitle surfaces with the specified color
    title_surface = title_font.render('Quantum Battleships', True, config.SPECIAL_RED)
    subtitle_surface = subtitle_font.render('Presented by Team BREAD', True, config.DARK_GREY)

    # Position the scroll image and get its rect
    scroll_rect = scroll_image.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 3.5))

    # Position the title and subtitle on the scroll
    title_rect = title_surface.get_rect(center=(scroll_rect.centerx, scroll_rect.centery - 25))
    subtitle_rect = subtitle_surface.get_rect(center=(scroll_rect.centerx, scroll_rect.centery + 30))

    # Calculate the position of the buttons to be below the scroll image
    button_y = scroll_rect.bottom + 50  # Position buttons 50 pixels below the scroll
    button_size = (200, 60)

    # Define buttons with their colors and initial positions
    buttons = {
        'start': {
            'color': config.DARK_GREY,
            'rect': pygame.Rect((config.SCREEN_WIDTH // 2 - button_size[0] // 2, button_y), button_size),
            'text': 'Start Game',
            'action': lambda: main(screen),
        },
        'instructions': {
            'color': config.DARK_GREY,
            'rect': pygame.Rect((config.SCREEN_WIDTH // 2 - button_size[0] // 2, button_y + button_size[1] + 10), button_size),
            'text': 'Instructions',
            'action': lambda: create_window(screen),  # Placeholder for instructions logic
        }
    }

    


    # Initialize the clock for controlling frame rate
    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                click_sound.play()
                mouse_pos = event.pos
                for button_key, button_props in buttons.items():
                    if button_props['rect'].collidepoint(mouse_pos):
                        button_props['action']()  # Call the button's action
                        is_running = False  # Assume that we want to close the menu after a button press

        # Drawing the background
        screen.blit(background_image, (0, 0))
        # Drawing the scroll
        screen.blit(scroll_image, scroll_rect)
        # Drawing the title and subtitle on top of the scroll
        screen.blit(title_surface, title_rect)
        screen.blit(subtitle_surface, subtitle_rect)

        # Draw custom buttons
        for button_key, button_props in buttons.items():
            draw_button(screen, button_props['color'], button_props['rect'].topleft, button_props['rect'].size)
            text_surf = button_font.render(button_props['text'], True, config.LIGHT_GREY)
            text_rect = text_surf.get_rect(center=button_props['rect'].center)
            screen.blit(text_surf, text_rect)

        # Update the screen
        pygame.display.update()

    pygame.quit()
    sys.exit()

def main(screen):
   # Set up the display, load images, and create the grid
    target_image, sea_image, background_image, _, quote_image, fire_image, wreck_image = load_images()
    click_sound, explosion_sound, splash_sound = load_sounds()
    target_image_rect = target_image.get_rect()
    font = pygame.font.Font("assets/fonts/OpenSans-VariableFont_wdth,wght.ttf", 16)
    font.set_bold(True)

    # Create overlays
    event_string_background = create_overlay((config.GRID_WIDTH + 80, 40), 150, config.LIGHT_GREY)
    heat_map_toggle_background = create_overlay((config.GRID_WIDTH + 80, 40), 150, config.LIGHT_GREY)
    counts_background = create_overlay((config.GRID_WIDTH + 80, 40), 150, config.LIGHT_GREY)
    settings_background = create_overlay((config.GRID_WIDTH + 80, 40), 150, config.LIGHT_GREY)
    grid_background = create_overlay((config.GRID_WIDTH + 80, config.GRID_HEIGHT + 80), 150, config.LIGHT_GREY)
    heat_map_background = create_overlay((config.GRID_WIDTH + 80, config.GRID_HEIGHT + 80), 150, config.LIGHT_GREY)
    button_overlay = create_overlay(config.BUTTON_SIZE, 175, config.BLACK)

    # Create grid buttons
    grid_buttons = create_grid_buttons(config.GRID_OFFSET_X, config.GRID_OFFSET_Y)

    probabilities = [get_prob(y) for y in range(8)]

    entangled = set()
    while len(entangled) < 16:
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        entangled.add((x, y))
    
    entangled = list(entangled)
    a = entangled[:8]
    b = entangled[8:]
    lookup1 = dict(zip(a, b))
    lookup2 = dict(zip(b, a))
    for key in lookup1:
        val = lookup1[key]
        k1, k2 = key
        v1, v2 = val
        p = int(0.5 * (int(probabilities[k1][k2]) + int(probabilities[v1][v2])))
        probabilities[k1][k2] = p
        probabilities[v1][v2] = p

    running = True
    display_heat_map = True
    current_pos = [0, 0]
    discovered = set()  # Keep track of discovered squares
    cannon = 0  # classic = 0, quantum = 1
    prob_display = [[False for x in range(8)] for y in range(8)]
    shots_fired, ships_sunk = 0, 0
    ship_state = [[[-1, 0] for _ in range(8)] for _ in range(8)]

    while running:
         # Blit images and overlays
        screen.blit(background_image, (0, 0))
        screen.blit(event_string_background, (config.GRID_OFFSET_X - 40, config.GRID_OFFSET_Y - 120))
        screen.blit(heat_map_toggle_background, (config.HEAT_MAP_OFFSET_X - 40, config.HEAT_MAP_OFFSET_Y - 120))
        screen.blit(counts_background, (config.GRID_OFFSET_X - 40, config.GRID_OFFSET_Y - 160))
        screen.blit(settings_background, (config.HEAT_MAP_OFFSET_X - 40, config.HEAT_MAP_OFFSET_Y - 160))
        screen.blit(grid_background, (config.GRID_OFFSET_X - 40, config.GRID_OFFSET_Y - 40))
        screen.blit(heat_map_background, (config.HEAT_MAP_OFFSET_X - 40, config.HEAT_MAP_OFFSET_Y - 40))
        screen.blit(sea_image, (config.GRID_OFFSET_X, config.GRID_OFFSET_Y))

        # Draw the home and reset toggles
        # Define the scale factor and spacing
        scale_factor = 2.05
        button_spacing = 10

        # Get the original home button dimensions and text
        home_toggle_text = font.render('HOME', True, config.LIGHT_GREY)
        home_toggle_rect_original = home_toggle_text.get_rect(center=(config.HEAT_MAP_OFFSET_X + 80, config.HEAT_MAP_OFFSET_Y - 142))

        # Inflate the original rect for visual padding and get its size for reference
        home_toggle_rect_padded = home_toggle_rect_original.inflate(20, 8)
        original_width, original_height = home_toggle_rect_padded.size

        # Calculate new width using the scale factor, keeping the height the same
        new_width = original_width * scale_factor

        # Create new rects for the buttons, keeping the height of the original rect
        home_toggle_rect = pygame.Rect(home_toggle_rect_original.left, home_toggle_rect_original.top, new_width, original_height)
        reset_toggle_rect = pygame.Rect(home_toggle_rect.right + button_spacing, home_toggle_rect.top, new_width, original_height)

        # Create and position the reset button text
        reset_toggle_text = font.render('RESET', True, config.LIGHT_GREY)
        reset_toggle_rect.center = reset_toggle_rect.center  # Re-center the text in the new rect

        # Draw the HOME button
        pygame.draw.rect(screen, config.DARK_GREY, home_toggle_rect, border_radius=8)
        # Calculate the top left position for the home text to be centered within its button
        home_text_x = home_toggle_rect.x + (home_toggle_rect.width - home_toggle_text.get_width()) // 2
        home_text_y = home_toggle_rect.y + (home_toggle_rect.height - home_toggle_text.get_height()) // 2
        screen.blit(home_toggle_text, (home_text_x, home_text_y - 1))

        # Draw the RESET button
        pygame.draw.rect(screen, config.DARK_GREY, reset_toggle_rect, border_radius=8)
        # Calculate the top left position for the reset text to be centered within its button
        reset_text_x = reset_toggle_rect.x + (reset_toggle_rect.width - reset_toggle_text.get_width()) // 2
        reset_text_y = reset_toggle_rect.y + (reset_toggle_rect.height - reset_toggle_text.get_height()) // 2
        screen.blit(reset_toggle_text, (reset_text_x, reset_text_y - 1))

        # Draw the "Probability Heat Map Display:" text
        heat_map_text = font.render('Probability Heat Map Display:', True, config.SPECIAL_RED)
        screen.blit(heat_map_text, (config.HEAT_MAP_OFFSET_X + 57, config.HEAT_MAP_OFFSET_Y - 114))

        # Draw the heat map toggle
        heat_map_toggle_text = font.render('ON' if display_heat_map else 'OFF', True, config.LIGHT_GREY)
        heat_map_toggle_rect = heat_map_toggle_text.get_rect(center=(config.HEAT_MAP_OFFSET_X + 3 * config.GRID_WIDTH // 4 + 15, config.HEAT_MAP_OFFSET_Y - 102))
        pygame.draw.rect(screen, config.DARK_GREY, heat_map_toggle_rect.inflate(20, 8), border_radius=8)  # Inflating the rect for visual padding
        screen.blit(heat_map_toggle_text, (heat_map_toggle_rect.topleft[0], heat_map_toggle_rect.topleft[1] - 1))

        # Draw the "Shots Fired:" text
        shots_fired_text = font.render('Shots Fired:', True, config.BLACK)
        screen.blit(shots_fired_text, (config.GRID_OFFSET_X, config.GRID_OFFSET_Y - 152))

        # Draw the "Ships Sunk:" text
        ships_sunk_text = font.render('Ships Sunk:', True, config.BLACK)
        screen.blit(ships_sunk_text, (config.GRID_OFFSET_X + 140, config.GRID_OFFSET_Y - 152))

        # Draw the "ESR Range:" text
        esr_range_text = font.render('ESR Range:', True, config.BLACK)
        screen.blit(esr_range_text, (config.GRID_OFFSET_X + 280, config.GRID_OFFSET_Y - 152))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_pos[1] = max(current_pos[1] - 1, 0)
                elif event.key == pygame.K_RIGHT:
                    current_pos[1] = min(current_pos[1] + 1, config.GRID_COLS - 1 - cannon)
                elif event.key == pygame.K_UP:
                    current_pos[0] = max(current_pos[0] - 1, 0)
                elif event.key == pygame.K_DOWN:
                    current_pos[0] = min(current_pos[0] + 1, config.GRID_ROWS - 1 - cannon)
                elif event.key == pygame.K_RETURN:
                    if cannon == 1:
                        shots_fired += 1
                        x, y = current_pos
                        squares = [(x, y), (x+1, y), (x, y+1), (x+1, y+1)]
                        for s in squares:
                            x1, y1 = s
                            if grid_buttons[s]['state'] == config.BUTTON_NORMAL:
                                prob_display[x1][y1] = True
                    else:
                        # Convert the current position to a tuple for set operations and dict key
                        pos_key = tuple(current_pos)
                        x, y = pos_key
                        if pos_key not in discovered:
                            shots_fired += 1
                            discovered.add(pos_key)
                            grid_buttons[pos_key]['state'] = config.BUTTON_CLICKED
                            prob_display[x][y] = False
                            state = classic(pos_key)
                            twin = None
                            if (x, y) in lookup1.keys():
                                twin = lookup1[(x, y)]
                            elif (x, y) in lookup2.keys():
                                twin = lookup2[(x, y)]
                            if state == 1: #hit
                                explosion_sound.play()
                                if twin:
                                    tx, ty = twin
                                    ships_sunk += 1
                                    probabilities[tx][ty] = 100 
                                    ship_state[tx][ty] = (1, pygame.time.get_ticks())
                                    discovered.add(twin)
                                    grid_buttons[twin]['state'] = config.BUTTON_CLICKED
                                    prob_display[tx][ty] = False

                                ships_sunk += 1
                                probabilities[x][y] = 100 
                                ship_state[x][y] = (1, pygame.time.get_ticks())
                            else: #miss
                                splash_sound.play()
                                if twin:
                                    tx, ty = twin
                                    probabilities[tx][ty] = 0
                                    ship_state[tx][ty][0] = 0
                                    discovered.add(twin)
                                    grid_buttons[twin]['state'] = config.BUTTON_CLICKED
                                    prob_display[tx][ty] = False
                                probabilities[x][y] = 0
                                ship_state[x][y][0] = 0
                elif event.key == pygame.K_SPACE:
                    if cannon == 0:
                        # update position to allow for expansion of target
                        if current_pos[0] == config.GRID_ROWS - 1:
                            current_pos[0] -= 1
                        if current_pos[1] == config.GRID_COLS - 1:
                            current_pos[1] -= 1
                        new_width = target_image.get_width() * 2
                        new_height = target_image.get_height() * 2
                        target_image = pygame.transform.scale(target_image, (new_width, new_height))
                        cannon = 1
                    else:
                        new_width = target_image.get_width() / 2
                        new_height = target_image.get_height() / 2
                        target_image = pygame.transform.scale(target_image, (new_width, new_height))
                        cannon = 0
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_sound.play()
                if heat_map_toggle_rect.collidepoint(event.pos):
                    display_heat_map = not display_heat_map  # Toggle the heat map display
                elif home_toggle_rect.collidepoint(event.pos):
                    main_menu(screen)
                elif reset_toggle_rect.collidepoint(event.pos):
                    main(screen)

        # Draw heat map or quote image based on the toggle
        if display_heat_map:
            # Your existing code to draw the heat map
            draw_heat_map(screen, probabilities, font)
            draw_indices(screen, config.HEAT_MAP_OFFSET_X, config.HEAT_MAP_OFFSET_Y, font)
        else:
            # If the heat map is toggled off, draw the quote image instead
            screen.blit(quote_image, (config.HEAT_MAP_OFFSET_X, config.HEAT_MAP_OFFSET_Y))

        # Draw fire images
        for i in range(8):
            for j in range(8):
                if ship_state[j][i][0] == 1:  # Check if a ship has been hit
                    time_since_hit = pygame.time.get_ticks() - ship_state[j][i][1]
                    pos = (config.GRID_OFFSET_X + 51*i, config.GRID_OFFSET_Y + 51*j)  # Position for blitting images

                    if time_since_hit < 2000:
                        # Ensure the fire image is fully visible initially
                        fire_image.set_alpha(255)
                        screen.blit(fire_image, pos)
                    else:
                        fade_duration = 2500  # Duration of the fade in milliseconds
                        if time_since_hit - 2000 < fade_duration:
                            # Fade out fire image
                            fire_alpha = max(0, min(255, int(255 - ((time_since_hit - 2000) / fade_duration) * 255)))
                            fire_image.set_alpha(fire_alpha)
                            screen.blit(fire_image, pos)

                            # Fade in wreck image
                            wreck_alpha = max(0, min(255, int(((time_since_hit - 2000) / fade_duration) * 255)))
                            wreck_image.set_alpha(wreck_alpha)
                            screen.blit(wreck_image, pos)
                        else:
                            # Once fade is complete, display wreck image normally
                            wreck_image.set_alpha(255)
                            screen.blit(wreck_image, pos)

        # Draw the indices for the grid and heat map
        draw_indices(screen, config.GRID_OFFSET_X, config.GRID_OFFSET_Y, font)

        # Draw the grid buttons
        for pos_key, button_data in grid_buttons.items():
            button_rect = button_data['rect']
            if pos_key not in discovered:
                # If the button has not been discovered, draw the button overlay
                screen.blit(button_overlay, button_rect.topleft)

        # Iterate over the grid positions
        for x in range(8):
            for y in range(8):
                pos = (config.GRID_OFFSET_X + y * (config.BUTTON_WIDTH + config.GRID_PADDING),
                        config.GRID_OFFSET_Y + x * (config.BUTTON_HEIGHT + config.GRID_PADDING))

                # Check if the probability is not -1
                probability = probabilities[x][y]
                if prob_display[x][y]:
                    # Create a text surface with the probability
                    text = font.render(str(probability) + "%", True, config.LIGHT_GREY)
                    text_rect = text.get_rect()
                    center_x = pos[0] + config.BUTTON_WIDTH // 2
                    center_y = pos[1] + config.BUTTON_HEIGHT // 2
                    # Position the text in the center of the box
                    text_rect.center = (center_x, center_y)

                    # Display the text on the screen
                    screen.blit(text, text_rect.topleft)

        # Update the position of the target image and draw it
        target_image_rect.topleft = grid_buttons[tuple(current_pos)]['rect'].topleft
        screen.blit(target_image, target_image_rect.topleft)

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Run the game
if __name__ == "__main__":
    screen = init_pygame()
    theme_song = pygame.mixer.init()
    pygame.mixer.music.load('assets/sounds/theme_song.mp3')
    pygame.mixer.music.set_volume(0.25)
    pygame.mixer.music.play(-1)
    main_menu(screen)