from settings import *
from support import *
from button import Button
import random
import json
pygame.init()

class TriviaGame():
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.running = True
        self.surfs = folder_importer('assets', 'images')
        self.surfs['home_screen'] = pygame.transform.smoothscale(self.surfs['home_screen'], (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.surfs['blank_screen'] = pygame.transform.smoothscale(self.surfs['blank_screen'], (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.surfs['ya_lose'] = pygame.transform.smoothscale(self.surfs['ya_lose'], (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.buttons = pygame.sprite.Group()
        self.start_button = Button(self.surfs['button'], self.surfs['button_hover'], (WINDOW_WIDTH / 1.67, WINDOW_HEIGHT / 1.06), (412, 144), "Play", self.start)
        self.buttons.add(self.start_button)
        self.current_question = None
        self.import_questions()
        self.background = self.surfs['home_screen']
        self.choice = None

    def start(self):
        self.background = self.surfs['blank_screen']
        self.start_button.kill()
        self.current_question = self.easy_questions[0]
        rand_choices = [self.current_question["correct_answer"], self.current_question["incorrect_answers"][0], self.current_question["incorrect_answers"][1], self.current_question["incorrect_answers"][2]]
        random.shuffle(rand_choices)
        self.buttons.add(Button(self.surfs['button'], self.surfs['button_hover'], (WINDOW_WIDTH / 4, 5*WINDOW_HEIGHT / 8), (1000, 320), rand_choices[0], self.check_result))
        self.buttons.add(Button(self.surfs['button'], self.surfs['button_hover'], (3*WINDOW_WIDTH / 4, 5*WINDOW_HEIGHT / 8), (1000, 320), rand_choices[1], self.check_result))
        self.buttons.add(Button(self.surfs['button'], self.surfs['button_hover'], (WINDOW_WIDTH / 4, 7*WINDOW_HEIGHT / 8), (1000, 320), rand_choices[2], self.check_result))
        self.buttons.add(Button(self.surfs['button'], self.surfs['button_hover'], (3*WINDOW_WIDTH / 4, 7*WINDOW_HEIGHT / 8), (1000, 320), rand_choices[3], self.check_result))

    def check_result(self):
        if self.choice.text == self.current_question["correct_answer"]:
            pass
        else:
            self.background = self.surfs['ya_lose']
            self.buttons.empty()
            self.current_question = None
        
    def display_question(self):
        if self.current_question:
            font = pygame.font.Font(None, 64)
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
        self.easy_questions = random.sample(easy_questions, k=10)
        self.medium_questions = random.sample(medium_questions, k=10)
        self.hard_questions = random.sample(hard_questions, k=10)

    def run(self):
        while self.running:
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            self.choice = button
                            button.clicked()
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.blit(self.background, (0,0))
            self.display_question()
            self.buttons.update(self.screen)
            pygame.display.update()
                    
game = TriviaGame()
game.run()
pygame.quit()