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
        self.start_button = Button(self.surfs['button'], (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), (450, 160), "Play", self.start)
        self.buttons.add(self.start_button)

    def start(self):
        self.start_button.kill()
        self.buttons.add(Button(self.surfs['button'], (400, 400), (450, 160), "A", self.start))
        self.buttons.add(Button(self.surfs['button'], (800, 400), (450, 160), "B", self.start))
        self.buttons.add(Button(self.surfs['button'], (400, 800), (450, 160), "C", self.start))
        self.buttons.add(Button(self.surfs['button'], (800,800), (450, 160), "D", self.start))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            button.clicked()
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.blit(self.surfs['background'], (0,0))
            self.buttons.update(self.screen)
            pygame.display.update()
                    
game = TriviaGame()
game.run()
pygame.quit()