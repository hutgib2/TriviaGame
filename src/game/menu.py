from game.settings import *
from game.support import *
from game.button import *
from game.trivia_game import TriviaGame
import asyncio

class Menu():
    def __init__(self):
        # surfs
        SCREENS['home'] = pygame.transform.smoothscale(SCREENS['home'], (WINDOW_WIDTH, WINDOW_HEIGHT))
        SCREENS['blank'] = pygame.transform.smoothscale(SCREENS['blank'], (WINDOW_WIDTH, WINDOW_HEIGHT))
        SCREENS['lose'] = pygame.transform.smoothscale(SCREENS['lose'], (WINDOW_WIDTH, WINDOW_HEIGHT))
        SCREENS['win'] = pygame.transform.smoothscale(SCREENS['win'], (WINDOW_WIDTH, WINDOW_HEIGHT))
        SCREENS['walk_away'] = pygame.transform.smoothscale(SCREENS['walk_away'], (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.menu_surf = SCREENS['home']
        self.menu_rect = self.menu_surf.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.running = True

        self.menu_sprites = pygame.sprite.Group()
        self.start_button = InteractiveButton(GAME_BUTTONS['SURFS'],  (WINDOW_WIDTH / 1.63, WINDOW_HEIGHT / 1.2), (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 6), (self.menu_sprites), self.start_game, 'Start')
        self.pending_game = None

    def start_game(self):
        self.pending_game = TriviaGame()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for menu_sprite in self.menu_sprites:
                    if menu_sprite.rect.collidepoint(event.pos):
                        menu_sprite.is_clicked()

    async def run(self):
        while self.running:
            await asyncio.sleep(0)
            
            self.handle_events()
            screen.blit(self.menu_surf, self.menu_rect)
            self.menu_sprites.update()
            pygame.display.update()

            if self.pending_game:
                await self.pending_game.run()
                self.pending_game = None