from settings import *
from support import *
from button import *
from textSprite import TextSprite
import random
import json
import time
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()

class TriviaGame():
    def __init__(self):
        # general
        self.running = True
        self.state = 'home'

        # surfs
        self.surfs = folder_importer('assets', 'images')
        self.surfs['home_screen'] = pygame.transform.smoothscale(self.surfs['home_screen'], (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.surfs['blank_screen'] = pygame.transform.smoothscale(self.surfs['blank_screen'], (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.surfs['ya_lose'] = pygame.transform.smoothscale(self.surfs['ya_lose'], (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background = self.surfs['home_screen']

        # groups
        self.text_static = pygame.sprite.Group()
        self.game_buttons = pygame.sprite.Group()
        self.prize_buttons = pygame.sprite.Group()
        self.lifelines = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        # game_buttons
        self.start_button = InteractiveButton(self.surfs['button'], self.surfs['button_hover'], self.surfs['button_hover'],  (WINDOW_WIDTH / 1.67, WINDOW_HEIGHT / 1.06), (412, 144), (self.game_buttons, self.all_sprites))
        self.start_button.update_text('play')
        
        # questions
        self.import_questions()
        self.current_question = None
        self.choice = None
        self.round_number = 0
        self.question_sprite = TextSprite('', (5*WINDOW_WIDTH / 8, WINDOW_HEIGHT / 8), "white", 2*WINDOW_WIDTH/3, WINDOW_WIDTH / 32, (self.all_sprites))
        
        # lifelines
        self.x2_lifeline_active = False

    def create_prize_tree(self):
        # draw 15 increasing values of money on the far left of the screen from bottom to top
        for i in range(31, 1, -2):
            Button(self.surfs['prize_button'], self.surfs['prize_won'],  (WINDOW_WIDTH / 10, (i*WINDOW_HEIGHT / 34)), (WINDOW_WIDTH / 13, WINDOW_HEIGHT / 18), (self.prize_buttons, self.all_sprites))
        for prize, button in zip(prize_money, self.prize_buttons):
            button.update_text(prize)

    def start_game(self):
        self.background = self.surfs['blank_screen']
        self.start_button.kill()
        self.create_prize_tree()
        InteractiveButton(self.surfs['button'], self.surfs['button_hover'], self.surfs['button_disabled'], ((WINDOW_WIDTH / 2)-32, 5*WINDOW_HEIGHT / 8), (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 5), (self.game_buttons, self.all_sprites))
        InteractiveButton(self.surfs['button'], self.surfs['button_hover'], self.surfs['button_disabled'], (3*WINDOW_WIDTH / 4, 5*WINDOW_HEIGHT / 8), (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 5), (self.game_buttons, self.all_sprites))
        InteractiveButton(self.surfs['button'], self.surfs['button_hover'], self.surfs['button_disabled'], ((WINDOW_WIDTH / 2)-32, 7*WINDOW_HEIGHT / 8), (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 5), (self.game_buttons, self.all_sprites))
        InteractiveButton(self.surfs['button'], self.surfs['button_hover'], self.surfs['button_disabled'], (3*WINDOW_WIDTH / 4, 7*WINDOW_HEIGHT / 8), (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 5), (self.game_buttons, self.all_sprites))
        InteractiveButton(self.surfs['x2_lifeline'], self.surfs['x2_hover'], self.surfs['x2_disabled'], (WINDOW_WIDTH / 5, WINDOW_HEIGHT / 3), (WINDOW_WIDTH / 10, WINDOW_HEIGHT / 8), (self.lifelines, self.all_sprites))
        self.update_current_question()

    def update_current_question(self):
        self.current_question = self.questions[self.round_number]
        answers = [self.current_question["correct_answer"], self.current_question["incorrect_answers"][0], self.current_question["incorrect_answers"][1], self.current_question["incorrect_answers"][2]]
        random.shuffle(answers)
        self.question_sprite.kill()
        self.question_sprite = TextSprite(self.current_question["question"], (5*WINDOW_WIDTH / 8, WINDOW_HEIGHT / 8), "white", 2*WINDOW_WIDTH/3, WINDOW_WIDTH / 32, (self.all_sprites))
        
        for answer, button in zip(answers, self.game_buttons):
            button.update_text(answer)

    def button_clicked(self):
        if (self.state == 'home'):
            self.state = 'game'
            self.start_game()
        elif (self.state == 'game'):
            self.check_result()
        
    def update_round(self):
        # update prize button colour
        list(self.prize_buttons)[self.round_number].deactivate()
        for game_button in self.game_buttons:
            if not game_button.is_active:
                game_button.reactivate()

        self.round_number += 1
        self.update_current_question()

    def check_result(self):
        if self.choice.text == self.current_question["correct_answer"]:
            self.update_round()
        elif self.x2_lifeline_active:
            self.x2_lifeline_active = False
            self.choice.deactivate()

        else:
            self.background = self.surfs['ya_lose']
            self.game_buttons.empty()
            self.all_sprites.empty()
            self.state = 'lose'
            self.running = False

    def import_questions(self):
        easy_questions = []
        medium_questions = []
        hard_questions = []
        with open('assets/trivia.json', 'r') as file:
            questions = json.load(file)
            for question in questions:
                if question["difficulty"] == "easy":
                    easy_questions.append(question)
                elif question["difficulty"] == "medium":
                    medium_questions.append(question)
                elif question["difficulty"] == "hard":
                    hard_questions.append(question)
        self.questions = random.sample(easy_questions, k=5) + random.sample(medium_questions, k=5) + random.sample(hard_questions, k=5)

    def run(self):
        while self.running:
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.game_buttons:
                        if button.rect.collidepoint(event.pos):
                            self.choice = button
                            self.button_clicked()
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
            
            pygame.display.get_surface().blit(self.background, (0,0))
            self.all_sprites.update()
            self.text_static.draw(screen)
            pygame.display.update()
        if self.state == 'lose':
            time.sleep(3)        
game = TriviaGame()
game.run()
pygame.quit()