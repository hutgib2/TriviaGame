import pygame
from os.path import join 
from os import walk

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()

def folder_importer(*path):
    surfs = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            full_path = join(folder_path, file_name)
            surfs[file_name.split('.')[0]] = pygame.image.load(full_path).convert_alpha()
    return surfs

def audio_importer(*path):
    audio_dict = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            audio_dict[file_name.split('.')[0]] = pygame.mixer.Sound(join(folder_path, file_name))
    return audio_dict

def split_string(string):
    i = int(len(string)/2)
    while string[i] != ' ':
        i += 1
    return string[:i] + '\n' + string[i+1:]


GAME_BUTTONS = {
    'pos' : {
        'top_left': ((WINDOW_WIDTH / 2)-32, 5*WINDOW_HEIGHT / 8),
        'top_right': (3*WINDOW_WIDTH / 4, 5*WINDOW_HEIGHT / 8),
        'bottom_left': ((WINDOW_WIDTH / 2)-32, 7*WINDOW_HEIGHT / 8),
        'bottom_right': (3*WINDOW_WIDTH / 4, 7*WINDOW_HEIGHT / 8)
    },
    'size' : (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 5),
    'surfs' : folder_importer('assets', 'images', 'game_button')
}

LIFELINES = {
    'pos' : [
        (WINDOW_WIDTH / 5, WINDOW_HEIGHT / 3),
        (WINDOW_WIDTH / 5, WINDOW_HEIGHT / 4),
        (WINDOW_WIDTH / 5, WINDOW_HEIGHT / 5),
        (WINDOW_WIDTH / 5, WINDOW_HEIGHT / 6)
    ],
    'size' : (WINDOW_WIDTH / 10, WINDOW_HEIGHT / 8),
}

SCREENS = folder_importer('assets', 'images', 'screens')
PRIZE_BUTTONS = folder_importer('assets', 'images', 'prize_button')
X2_LIFELINE = folder_importer('assets', 'images', 'x2_lifeline')

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