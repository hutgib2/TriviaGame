from settings import *

class Button(pygame.sprite.Sprite):
    def __init__(self, surf, pos):
        super().__init__()
        self.image = surf
        self.rect = self.image.get_frect(center=pos)