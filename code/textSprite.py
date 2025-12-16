from settings import *
from support import split_string

class TextSprite(pygame.sprite.Sprite):
    def __init__(self, text, pos, color, max_width, size, groups):
        super().__init__(groups)
        self.text = text
        self.font = pygame.font.Font(None, int(size))
        self.image = self.font.render(text, True, color)
        if self.image.get_width() > max_width:
            self.image = self.font.render(split_string(self.text), True, color)
        self.rect = self.image.get_frect(center=pos)
        
