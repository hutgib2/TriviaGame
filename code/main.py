from settings import *
from support import *
pygame.init()

class TriviaGame():
    def __init__(self):
        WINDOW_WIDTH, WINDOW_HEIGHT = 2560, 1440
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.running = True
        self.surfs = folder_importer('assets')
        self.surfs['background'] = pygame.transform.smoothscale(self.surfs['background'], (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen.blit(self.surfs['background'], (0,0))
        pygame.display.update()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

game = TriviaGame()
game.run()
pygame.quit()