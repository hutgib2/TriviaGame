from settings import *
from support import *
from button import Button
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
        self.text_static = pygame.sprite.Group()
        self.text_buttons = pygame.sprite.Group()

        # buttons
        self.buttons = pygame.sprite.Group()
        self.prize_buttons = pygame.sprite.Group()
        self.start_button = Button(self.surfs['button'], self.surfs['button_hover'], (WINDOW_WIDTH / 1.67, WINDOW_HEIGHT / 1.06), (412, 144))
        self.text_buttons.add(TextSprite('play', self.start_button.rect.center, "darkcyan", self.start_button.rect.width, self.start_button.rect.width / 8))
        self.buttons.add(self.start_button)
        
        # questions
        self.import_questions()
        self.current_question = None
        self.choice = None
        self.round_number = 0

    def create_prize_tree(self):
        # draw 15 increasing values of money on the far left of the screen from bottom to left
        for i in range(29, 0, -2):
            self.prize_buttons.add(Button(self.surfs['button'], self.surfs['button_hover'], (WINDOW_WIDTH / 10, (i*WINDOW_HEIGHT / 30)), (WINDOW_WIDTH / 13, WINDOW_HEIGHT / 16)))
        
        for prize, button in zip(prize_money, self.prize_buttons):
            self.text_static.add(TextSprite(prize, button.rect.center, "darkgreen", button.rect.width, button.rect.width / 8))

    def start_game(self):
        self.background = self.surfs['blank_screen']
        self.start_button.kill()
        self.create_prize_tree()
        self.buttons.add(Button(self.surfs['button'], self.surfs['button_hover'], ((WINDOW_WIDTH / 2)-32, 5*WINDOW_HEIGHT / 8), (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 5), True))
        self.buttons.add(Button(self.surfs['button'], self.surfs['button_hover'], (3*WINDOW_WIDTH / 4, 5*WINDOW_HEIGHT / 8), (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 5), True))
        self.buttons.add(Button(self.surfs['button'], self.surfs['button_hover'], ((WINDOW_WIDTH / 2)-32, 7*WINDOW_HEIGHT / 8), (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 5), True))
        self.buttons.add(Button(self.surfs['button'], self.surfs['button_hover'], (3*WINDOW_WIDTH / 4, 7*WINDOW_HEIGHT / 8), (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 5), True))
        self.update_current_question()

    def update_current_question(self):
        self.current_question = self.questions[self.round_number]
        answers = [self.current_question["correct_answer"], self.current_question["incorrect_answers"][0], self.current_question["incorrect_answers"][1], self.current_question["incorrect_answers"][2]]
        random.shuffle(answers)
        
        self.text_buttons.empty()
        self.text_buttons.add(TextSprite(self.current_question["question"], (5*WINDOW_WIDTH / 8, WINDOW_HEIGHT / 8), "white", 2*WINDOW_WIDTH/3, WINDOW_WIDTH / 32))
        for answer, button in zip(answers, self.buttons):
            self.text_buttons.add(TextSprite(answer, button.rect.center, "darkcyan", button.rect.width, button.rect.width / 8))
            button.text = answer

    def button_clicked(self):
        if (self.state == 'home'):
            self.start_game()
            self.state = 'game'
        elif (self.state == 'game'):
            self.check_result()
        
    def update_round(self):
        # update prize button colour
        list(self.prize_buttons)[self.round_number].image = list(self.prize_buttons)[self.round_number].image_hover
        self.round_number += 1
        self.update_current_question()

    def check_result(self):
        if self.choice.text == self.current_question["correct_answer"]:
            self.update_round()
        else:
            self.background = self.surfs['ya_lose']
            self.buttons.empty()
            self.prize_buttons.empty()
            self.text_buttons.empty()
            self.text_static.empty()
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
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            self.choice = button
                            self.button_clicked()
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
            
            screen.blit(self.background, (0,0))
            self.buttons.update(screen)
            self.prize_buttons.update(screen)
            self.text_buttons.update(screen)
            self.text_static.update(screen)
            pygame.display.update()
        if self.state == 'lose':
            time.sleep(3)        
game = TriviaGame()
game.run()
pygame.quit()