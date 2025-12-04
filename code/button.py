from settings import *
from support import split_string
class Button(pygame.sprite.Sprite):
    def __init__(self, surf, hover_surf, pos, size, text):
        super().__init__()
        self.image = pygame.transform.smoothscale(surf, size)
        self.image_hover = pygame.transform.smoothscale(hover_surf, size)
        self.rect = self.image.get_frect(center=pos)
        
        # text
        self.font = pygame.font.Font(None, 50)
        self.update_text(text)

    def update_text(self, new_text):
        self.text = new_text
        self.text_surf = self.font.render(self.text, True, "darkcyan")
        if self.text_surf.get_width() > self.image.get_width():
            self.text = split_string(self.text)
            self.text_surf = self.font.render(self.text, True, "darkcyan")
        self.text_rect = self.text_surf.get_frect(center=self.rect.center)
    
    def update(self, screen):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(self.image_hover, self.rect)
        else:   
            screen.blit(self.image, self.rect)
        screen.blit(self.text_surf, self.text_rect)
