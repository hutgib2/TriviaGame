from settings import *
from support import split_string

class Button(pygame.sprite.Sprite):
    def __init__(self, surf, hover_surf, pos, size, groups):
        super().__init__(groups)
        self.text = ''
        self.image = pygame.transform.smoothscale(surf, size)
        self.image_hover = pygame.transform.smoothscale(hover_surf, size)
        self.rect = self.image.get_frect(center=pos)
    
    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.display.get_surface().blit(self.image_hover, self.rect)
        else:   
            pygame.display.get_surface().blit(self.image, self.rect)
