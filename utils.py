import random
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, transpile, execute, Aer, ClassicalRegister
import pygame
import config
from qiskit import BasicAer, IBMQ
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
import qiskit as qk
from pygame.locals import *

def load_images():
    """Loads and transforms images to be used in the game."""
    target_image = pygame.image.load("assets/images/target.png")
    sea_image_width = (config.BUTTON_WIDTH * config.GRID_COLS) + (config.GRID_PADDING * (config.GRID_COLS - 1))
    sea_image_height = (config.BUTTON_HEIGHT * config.GRID_ROWS) + (config.GRID_PADDING * (config.GRID_ROWS - 1))
    sea_image = pygame.transform.scale(pygame.image.load("assets/images/sea.png"), (sea_image_width, sea_image_height))
    background_image = pygame.image.load("assets/images/background.png")
    background_image = pygame.transform.scale(background_image, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    scroll_image = pygame.image.load("assets/images/scroll.png")
    scroll_image_rect = scroll_image.get_rect()
    scroll_image_width = int(scroll_image_rect.width * 1.7)
    scroll_image_height = int(scroll_image_rect.height * 1.2)
    scroll_image = pygame.transform.scale(scroll_image, (scroll_image_width, scroll_image_height))
    quote_image = pygame.image.load("assets/images/quote.png")
    quote_image = pygame.transform.scale(quote_image, (config.GRID_WIDTH, config.GRID_HEIGHT))
    fire_image = pygame.image.load("assets/images/fire.png")
    wreck_image = pygame.image.load("assets/images/wreck.png")
    return target_image, sea_image, background_image, scroll_image, quote_image, fire_image, wreck_image

def load_sounds():
    """Loads sound effects to be used in the game"""
    click_sound = pygame.mixer.Sound('assets/sounds/menu.mp3')
    explosion_sound = pygame.mixer.Sound('assets/sounds/explosion.mp3')
    explosion_sound.set_volume(0.50)
    splash_sound = pygame.mixer.Sound('assets/sounds/splash.mp3')
    return click_sound, explosion_sound, splash_sound

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
        text_rect = text_surf.get_rect(center=(offset_x + i * (config.BUTTON_WIDTH + config.GRID_PADDING) + config.BUTTON_WIDTH / 2, offset_y - 19))
        surface.blit(text_surf, text_rect.topleft)

    # Draw Y-axis indices (numbers)
    for i in range(config.GRID_ROWS):
        number = str(i + 1)
        text_surf = font.render(number, True, config.BLACK)
        # Centering the number at the start of the row
        text_rect = text_surf.get_rect(center=(offset_x - 21, offset_y + i * (config.BUTTON_HEIGHT + config.GRID_PADDING) + config.BUTTON_HEIGHT / 2))
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

def generate_board(dim, ships, boards):
    """Returns a generated board of qubits."""
    target = ships*boards
    current = 0
    m = []
    for i in range(dim*dim):
        random_number = random.uniform(0, min(boards - boards/3 , target - current ))
        if i == 1:
            random_number = 0
        m.append(random_number / boards)
        current += random_number
    b = m[:2]
    a = m[2:]
    random.shuffle(a)
    m = b + a
    board = []

    for i in range(dim):
        qr = QuantumRegister(dim, 'q')
        cr = ClassicalRegister(dim, 'c')
        circuit = QuantumCircuit(qr, cr)
        for j in range(dim):
            prob_0 = m[i*dim + j]
            amplitude_0 = np.sqrt(1 - prob_0)
            amplitude_1 = np.sqrt(prob_0)
            circuit.initialize([amplitude_0, amplitude_1], qr[j])
        board.append(circuit)
             
    return board

def get_heat_map_color(probability):
    if 1 < probability < 9:
        return config.BLUE2
    elif 10 < probability < 19:
        return config.BLUE3
    elif 20 < probability < 29:
        return config.BLUE4
    elif 30 < probability < 39:
        return config.BLUE5
    elif 40 < probability < 49:
        return config.BLUE6
    elif 50 < probability < 59:
        return config.ORANGE1
    elif 60 < probability < 69:
        return config.ORANGE2
    elif 70 < probability < 79:
        return config.ORANGE3
    elif 80 < probability < 89:
        return config.ORANGE4
    elif 90 < probability < 99:
        return config.ORANGE5
    elif probability == 100:
        return config.ORANGE6
    else:
        return config.BLUE1

def draw_heat_map(screen, probabilities, font):
    # Iterate over the grid positions to create the heat map
    for y in range(8):
        for x in range(8):
            # Calculate the heat map position symmetrically to the grid
            pos_x = config.HEAT_MAP_OFFSET_X + x * (config.BUTTON_WIDTH + config.GRID_PADDING)
            pos_y = config.HEAT_MAP_OFFSET_Y + y * (config.BUTTON_HEIGHT + config.GRID_PADDING)
            
            # Get the current probability for this position
            probability = int(probabilities[y][x])
            
            # Get the color for this probability
            heat_map_color = get_heat_map_color(probability)
            
            # Draw the heat map square
            heat_map_rect = pygame.Rect(pos_x, pos_y, config.BUTTON_WIDTH, config.BUTTON_HEIGHT)
            pygame.draw.rect(screen, heat_map_color, heat_map_rect)
            
            # Optionally, draw the probability text over the heat map
            if probability != -1:
                text = font.render(f"{probability}%", True, config.BLACK)
                text_rect = text.get_rect(center=(pos_x + config.BUTTON_WIDTH // 2, pos_y + config.BUTTON_HEIGHT // 2))
                screen.blit(text, text_rect)