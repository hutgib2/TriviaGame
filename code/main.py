from settings import *
from support import *
from button import Button
pygame.init()

class TriviaGame():
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.running = True
        self.surfs = folder_importer('assets')

        self.surfs['background'] = pygame.transform.smoothscale(self.surfs['background'], (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen.blit(self.surfs['background'], (0,0))
        
        self.button = Button(self.surfs['button'], (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.screen.blit(self.button.image, self.button.rect.center)
        
        pygame.display.update()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
game = TriviaGame()
game.run()
pygame.quit()