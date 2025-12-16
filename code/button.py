from settings import *
from support import split_string

class Button(pygame.sprite.Sprite):
    def __init__(self, surf, hover_surf, pos, size, groups):
        super().__init__(groups)
        self.text = ''
        self.image = pygame.transform.smoothscale(surf, size)
        self.image_hover = pygame.transform.smoothscale(hover_surf, size)
        self.size = size
        self.rect = self.image.get_frect(center=pos)
        self.is_active = True

    def deactivate(self, deactivated_surf):
        self.is_active = False
        self.image = pygame.transform.smoothscale(deactivated_surf, self.size)

    def reactivate(self, activated_surf):
        self.is_active = True
        self.image = pygame.transform.smoothscale(activated_surf, self.size)
    
    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and self.is_active:
            pygame.display.get_surface().blit(self.image_hover, self.rect)
        else:   
            pygame.display.get_surface().blit(self.image, self.rect)
