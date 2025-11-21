from settings import *

class Button(pygame.sprite.Sprite):
    def __init__(self, surf, pos, size, text, clicked):
        super().__init__()
        self.image = pygame.transform.smoothscale(surf, size)
        self.rect = self.image.get_frect(center=pos)
        self.clicked = clicked
        
        # text
        self.text = text
        self.font = pygame.font.Font(None, 128)
        self.text_surf = self.font.render(text, True, "darkcyan")
        self.text_rect = self.text_surf.get_frect(center=pos)
    
    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text_surf, self.text_rect)