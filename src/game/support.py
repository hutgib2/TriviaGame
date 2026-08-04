from os.path import join 
from os import walk
from game.settings import pygame


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

def split_string(s):
    mid = len(s) // 2
    left = s.rfind(' ', 0, mid)   # last space before mid, or -1
    right = s.find(' ', mid)      # first space at/after mid, or -1

    if left == -1 and right == -1: # only 1 word
        return s
    elif left == -1:
        i = right
    elif right == -1:
        i = left
    else:
        i = left if (mid - left) <= (right - mid) else right

    return s[:i] + '\n' + s[i+1:]