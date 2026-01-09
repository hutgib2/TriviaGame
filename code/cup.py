from settings import *
from textSprite import TextSprite

class Cup(pygame.sprite.Sprite):
    def __init__(self, pos, number, groups):
        super().__init__(groups)
        self.image = pygame.transform.smoothscale(MAGIC_CUPS['SURFS']['default'], MAGIC_CUPS['size'])
        self.image_hover = pygame.transform.smoothscale(MAGIC_CUPS['SURFS']['hover'], MAGIC_CUPS['size'])
        self.rect = self.image.get_frect(center=pos)
        self.number = number
        self.is_hidden = False
        self.text_sprite = TextSprite(str(number), self.rect.center, "darkcyan", self.rect.width, self.rect.width / 2, ())

    def hide(self):
        self.is_hidden = True
    
    def update(self):
        pygame.display.get_surface().blit(self.text_sprite.image, self.text_sprite.rect) # displaying number
        if self.is_hidden == False:
            if self.rect.collidepoint(pygame.mouse.get_pos()): # if mouse is touching cup
                pygame.display.get_surface().blit(self.image_hover, self.rect) # display hover image
            else:   
                pygame.display.get_surface().blit(self.image, self.rect) # display default image