from settings import *
from support import *
from button import Button
import random
import json
import time
pygame.init()

class TriviaGame():
    def __init__(self):
        # general
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.running = True
        self.state = 'home'

        # surfs
        self.surfs = folder_importer('assets', 'images')
        self.surfs['home_screen'] = pygame.transform.smoothscale(self.surfs['home_screen'], (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.surfs['blank_screen'] = pygame.transform.smoothscale(self.surfs['blank_screen'], (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.surfs['ya_lose'] = pygame.transform.smoothscale(self.surfs['ya_lose'], (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background = self.surfs['home_screen']
        
        # buttons
        self.buttons = pygame.sprite.Group()
        self.start_button = Button(self.surfs['button'], self.surfs['button_hover'], (WINDOW_WIDTH / 1.67, WINDOW_HEIGHT / 1.06), (412, 144), "Play")
        self.buttons.add(self.start_button)
        
        # questions
        self.import_questions()
        self.current_question = None
        self.answers = None
        self.choice = None
        self.index = 0

    def start_game(self):
        self.background = self.surfs['blank_screen']
        self.start_button.kill()
        self.update_current_question()
        self.buttons.add(Button(self.surfs['button'], self.surfs['button_hover'], (WINDOW_WIDTH / 4, 5*WINDOW_HEIGHT / 8), (1000, 320), self.answers[0]))
        self.buttons.add(Button(self.surfs['button'], self.surfs['button_hover'], (3*WINDOW_WIDTH / 4, 5*WINDOW_HEIGHT / 8), (1000, 320), self.answers[1]))
        self.buttons.add(Button(self.surfs['button'], self.surfs['button_hover'], (WINDOW_WIDTH / 4, 7*WINDOW_HEIGHT / 8), (1000, 320), self.answers[2]))
        self.buttons.add(Button(self.surfs['button'], self.surfs['button_hover'], (3*WINDOW_WIDTH / 4, 7*WINDOW_HEIGHT / 8), (1000, 320), self.answers[3]))

    def update_current_question(self):
        self.current_question = self.questions[self.index]
        self.answers = [self.current_question["correct_answer"], self.current_question["incorrect_answers"][0], self.current_question["incorrect_answers"][1], self.current_question["incorrect_answers"][2]]
        random.shuffle(self.answers)

    def button_clicked(self):
        if (self.state == 'home'):
            self.start_game()
            self.state = 'game'
        elif (self.state == 'game'):
            self.check_result()
        
    def update_round(self):
        self.index += 1
        self.update_current_question()
        i = 0
        for button in self.buttons:
            button.update_text(self.answers[i])
            i += 1

    def check_result(self):
        if self.choice.text == self.current_question["correct_answer"]:
            self.update_round()
        else:
            self.background = self.surfs['ya_lose']
            self.buttons.empty()
            self.state = 'lose'
            self.running = False
        
    def display_question(self):
        if self.state == 'game':
            font = pygame.font.Font(None, 50)
            text_surf = font.render(self.current_question["question"], True, "white")
            text_rect = text_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 8))
            self.screen.blit(text_surf, text_rect)

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
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            self.choice = button
                            self.button_clicked()
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.blit(self.background, (0,0))
            self.display_question()
            self.buttons.update(self.screen)
            pygame.display.update()
        if self.state == 'lose':
            time.sleep(3)        
game = TriviaGame()
game.run()
pygame.quit()