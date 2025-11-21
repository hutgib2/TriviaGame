from settings import *
from support import *
from button import Button
pygame.init()

class TriviaGame():
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.running = True
        self.surfs = folder_importer('assets', 'images')

        self.surfs['background'] = pygame.transform.smoothscale(self.surfs['background'], (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.buttons = pygame.sprite.Group()
        self.buttons.add(Button(self.surfs['button'], (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), (450, 160), "Play"))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            button.kill()
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.blit(self.surfs['background'], (0,0))
            self.buttons.update(self.screen)
            pygame.display.update()
                    
game = TriviaGame()
game.run()
pygame.quit()