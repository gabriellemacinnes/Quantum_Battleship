import random
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, transpile, execute, Aer, ClassicalRegister
import pygame
import config
from qiskit import BasicAer, IBMQ
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
import qiskit as qk
from pygame.locals import *
from utils import *

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
    scroll_image_width = int(scroll_image_rect.width * 1.8)
    scroll_image_height = int(scroll_image_rect.height * 1.2)
    scroll_image = pygame.transform.scale(scroll_image, (scroll_image_width, scroll_image_height))
    return target_image, sea_image, background_image, scroll_image

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


#returns a generated board of qubits
def generate_board(dim, ships, boards):
    b = [[0 for _ in range(dim)] for _ in range(dim)]
    target = ships*boards
    current = 0
    m = []
    for i in range(dim*dim):
        random_number = random.uniform(0, min(boards - boards/3 , target - current ))
        m.append(random_number / boards)
        current += random_number
    random.shuffle(m)
    for i in range(dim):
        for j in range(dim):
            prob_0 = m[i*dim + j]
            amplitude_0 = np.sqrt(1 - prob_0)
            amplitude_1 = np.sqrt(prob_0)
            qr = QuantumRegister(1, 'q')
            cr = ClassicalRegister(1, 'c')
            circuit = QuantumCircuit(qr, cr)
            circuit.initialize([amplitude_0, amplitude_1], qr[0])
            b[i][j] = circuit
    return b