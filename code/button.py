from settings import *

class Button(pygame.sprite.Sprite):
    def __init__(self, surf, pos, size, text):
        super().__init__()
        self.image = pygame.transform.smoothscale(surf, size)
        self.rect = self.image.get_frect(center=pos)
        self.text = text
