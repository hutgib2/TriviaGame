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
        self.start_button = Button(self.surfs['button'], self.surfs['button_hover'], (WINDOW_WIDTH / 1.67, WINDOW_HEIGHT / 1.06), (412, 144), "Play", self.start)
        self.buttons.add(self.start_button)

    def start(self):
        self.start_button.kill()
        self.buttons.add(Button(self.surfs['button'], self.surfs['button_hover'], (WINDOW_WIDTH / 4, 5*WINDOW_HEIGHT / 8), (425, 155), "A", self.start))
        self.buttons.add(Button(self.surfs['button'], self.surfs['button_hover'], (3*WINDOW_WIDTH / 4, 5*WINDOW_HEIGHT / 8), (425, 155), "B", self.start))
        self.buttons.add(Button(self.surfs['button'], self.surfs['button_hover'], (WINDOW_WIDTH / 4, 7*WINDOW_HEIGHT / 8), (425, 155), "C", self.start))
        self.buttons.add(Button(self.surfs['button'], self.surfs['button_hover'], (3*WINDOW_WIDTH / 4, 7*WINDOW_HEIGHT / 8), (425, 155), "D", self.start))

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