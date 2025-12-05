from settings import *
from support import split_string

class Button(pygame.sprite.Sprite):
    def __init__(self, surf, hover_surf, pos, size):
        super().__init__()
        self.text = ''
        self.image = pygame.transform.smoothscale(surf, size)
        self.image_hover = pygame.transform.smoothscale(hover_surf, size)
        self.rect = self.image.get_frect(center=pos)
    
    def update(self, screen):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(self.image_hover, self.rect)
        else:   
            screen.blit(self.image, self.rect)

