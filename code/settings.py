import pygame
from os.path import join 
from os import walk
from support import folder_importer

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()

GAME_BUTTONS = {
    'POS' : {
        'top_left': ((WINDOW_WIDTH / 2)-32, 5*WINDOW_HEIGHT / 8),
        'top_right': (3*WINDOW_WIDTH / 4, 5*WINDOW_HEIGHT / 8),
        'bottom_left': ((WINDOW_WIDTH / 2)-32, 7*WINDOW_HEIGHT / 8),
        'bottom_right': (3*WINDOW_WIDTH / 4, 7*WINDOW_HEIGHT / 8)
    },
    'size' : (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 5),
    'SURFS' : folder_importer('assets', 'images', 'game_button')
}

LIFELINES = {
    'POS' : [
        (WINDOW_WIDTH / 5, 2*WINDOW_HEIGHT / 8),
        (WINDOW_WIDTH / 5, 3*WINDOW_HEIGHT / 8),
        (WINDOW_WIDTH / 5, 4*WINDOW_HEIGHT / 8),
        (WINDOW_WIDTH / 5, 5*WINDOW_HEIGHT / 8)
    ],
    'size' : (WINDOW_WIDTH / 10, WINDOW_HEIGHT / 9),
    'SURFS' : folder_importer('assets', 'images', 'lifelines'),
}

WALK_AWAY = {
    'pos' : (WINDOW_WIDTH / 4, 7*WINDOW_HEIGHT / 8),
    'size' : (WINDOW_WIDTH / 5, WINDOW_HEIGHT / 6),
    'SURFS' : folder_importer('assets', 'images', 'walk_away'),
}

SCREENS = folder_importer('assets', 'images', 'screens')
PRIZE_BUTTONS = folder_importer('assets', 'images', 'prize_button')

MAGIC_CUPS = {
    'POS' : [
        (11*WINDOW_WIDTH / 32, 3*WINDOW_HEIGHT / 8),
        (17*WINDOW_WIDTH / 32, 3*WINDOW_HEIGHT / 8),
        (23*WINDOW_WIDTH / 32, 3*WINDOW_HEIGHT / 8),
        (29*WINDOW_WIDTH / 32, 3*WINDOW_HEIGHT / 8)
    ],
    'size' : (3*WINDOW_WIDTH / 32,WINDOW_HEIGHT / 4),
    'SURFS': folder_importer('assets', 'images', 'magic_cup')
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