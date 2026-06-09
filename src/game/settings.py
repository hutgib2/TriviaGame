import asyncio
import pygame
from os.path import join 
from os import walk
from game.support import folder_importer

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()

GAME_BUTTONS = {
    'POS' : {
        'top_left': ((WINDOW_WIDTH / 1.75), 5*WINDOW_HEIGHT / 8),
        'top_right': (WINDOW_WIDTH / 1.2, 5*WINDOW_HEIGHT / 8),
        'bottom_left': ((WINDOW_WIDTH / 1.75), 7*WINDOW_HEIGHT / 8),
        'bottom_right': (WINDOW_WIDTH / 1.2, 7*WINDOW_HEIGHT / 8)
    },
    'size' : (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 6),
    'SURFS' : folder_importer('src', 'assets', 'images', 'game_button')
}

LIFELINES = {
    'POS' : [
        (WINDOW_WIDTH / 4, 2.2*WINDOW_HEIGHT / 8),
        (WINDOW_WIDTH / 4, 3.3*WINDOW_HEIGHT / 8),
        (WINDOW_WIDTH / 4, 4.4*WINDOW_HEIGHT / 8),
        (WINDOW_WIDTH / 4, 5.5*WINDOW_HEIGHT / 8)
    ],
    'size' : (WINDOW_WIDTH / 5, WINDOW_HEIGHT / 8),
    'SURFS' : folder_importer('src', 'assets', 'images', 'lifelines'),
}

WALK_AWAY = {
    'pos' : (WINDOW_WIDTH / 4, 6.6*WINDOW_HEIGHT / 8),
    'size' : (WINDOW_WIDTH / 5, WINDOW_HEIGHT / 8),
    'SURFS' : folder_importer('src', 'assets', 'images', 'walk_away'),
}

SCREENS = folder_importer('src', 'assets', 'images', 'screens')
PRIZE_BUTTONS = folder_importer('src', 'assets', 'images', 'prize_button')

MAGIC_CUPS = {
    'POS' : [
        (14*WINDOW_WIDTH / 32, 3*WINDOW_HEIGHT / 8),
        (19*WINDOW_WIDTH / 32, 3*WINDOW_HEIGHT / 8),
        (24*WINDOW_WIDTH / 32, 3*WINDOW_HEIGHT / 8),
        (29*WINDOW_WIDTH / 32, 3*WINDOW_HEIGHT / 8)
    ],
    'size' : (WINDOW_WIDTH / 8,WINDOW_HEIGHT / 4),
    'SURFS': folder_importer('src', 'assets', 'images', 'magic_cup')
}
prize_money = [
    '£50', 
    '£100', 
    '£250',
    '£500',
    '£1,000',
    '£3,200',
    '£10,000',
    '32,000',
    '£100,000',
    '£250,000',
    '£500,000',
    '£1,000,000',
    '£2,500,000',
    '10,000,000',
    '£99,999,999'   
]