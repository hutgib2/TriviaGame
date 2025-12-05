from settings import *
from support import split_string

class TextSprite(pygame.sprite.Sprite):
    def __init__(self, text, pos, color, max_width, size):
        super().__init__()
        self.text = text
        self.font = pygame.font.Font(None, int(size))
        self.surf = self.font.render(text, True, color)
        if self.surf.get_width() > max_width:
            self.surf = self.font.render(split_string(self.text), True, color)
        self.rect = self.surf.get_frect(center=pos)

    def update(self, screen):
        screen.blit(self.surf, self.rect)
