from settings import *
from support import *
from button import *
from textSprite import TextSprite
from cup import Cup
import random
import json
import time
from timer import Timer

class TriviaGame():
    def __init__(self):
        # general
        self.running = True
        self.state = 'home'

        # surfs
        SCREENS['home'] = pygame.transform.smoothscale(SCREENS['home'], (WINDOW_WIDTH, WINDOW_HEIGHT))
        SCREENS['blank'] = pygame.transform.smoothscale(SCREENS['blank'], (WINDOW_WIDTH, WINDOW_HEIGHT))
        SCREENS['lose'] = pygame.transform.smoothscale(SCREENS['lose'], (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background = SCREENS['home']

        # groups
        self.game_buttons = pygame.sprite.Group()
        self.prize_buttons = pygame.sprite.Group()
        self.lifelines = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.magic_cups = pygame.sprite.Group()

        # game_buttons
        self.start_button = InteractiveButton(GAME_BUTTONS['SURFS'],  (WINDOW_WIDTH / 1.67, WINDOW_HEIGHT / 1.06), (412, 144), (self.game_buttons, self.all_sprites), self.start_game, 'play')
        self.correct_button = None

        # questions
        self.import_questions()
        self.current_question = None
        self.choice = None
        self.round_number = 0
        self.question_sprite = TextSprite('', (5*WINDOW_WIDTH / 8, WINDOW_HEIGHT / 8), "white", 2*WINDOW_WIDTH/3, WINDOW_WIDTH / 32, (self.all_sprites))
        
        # lifelines
        self.x2_active = False
        self.magic_cup_active = False
        self.magic_cup_timer = Timer(2000, lambda: {cup.kill() for cup in self.magic_cups})

    def create_prize_tree(self):
        # draw 15 increasing values of money on the far left of the screen from bottom to top
        for i in range(31, 1, -2):
            Button(PRIZE_BUTTONS,  (WINDOW_WIDTH / 10, (i*WINDOW_HEIGHT / 34)), (WINDOW_WIDTH / 13, WINDOW_HEIGHT / 18), (self.prize_buttons, self.all_sprites))
        for prize, button in zip(prize_money, self.prize_buttons):
            button.update_text(prize)

    # lifelines activation

    def activate_x2(self):
        self.x2_active = True

    def activate_revive(self):
        deactivated_lifelines = []
        for lifeline in self.lifelines:
            if lifeline.is_active == False:
                deactivated_lifelines.append(lifeline)
        reactivated_lifeline = random.choice(deactivated_lifelines)
        reactivated_lifeline.reactivate()

    def activate_switch(self):
        self.update_current_question(self.easy_questions.pop())

    def activate_magic_cup(self):
        self.magic_cup_active = True
        for game_button in self.game_buttons:
            game_button.deactivate()

        numbers = [0, 1, 2, 3]
        random.shuffle(numbers)

        Cup(MAGIC_CUPS['POS'][0], numbers.pop(), (self.magic_cups, self.all_sprites))
        Cup(MAGIC_CUPS['POS'][1], numbers.pop(), (self.magic_cups, self.all_sprites))
        Cup(MAGIC_CUPS['POS'][2], numbers.pop(), (self.magic_cups, self.all_sprites))
        Cup(MAGIC_CUPS['POS'][3], numbers.pop(), (self.magic_cups, self.all_sprites))

    def reactivate_game_buttons(self, cup_number):
        self.correct_button.reactivate()
        number_of_buttons_to_reactivate = 3 - cup_number

        for button in self.game_buttons:
            if number_of_buttons_to_reactivate == 0:
                break
            if button != self.correct_button:
                button.reactivate()
                number_of_buttons_to_reactivate -= 1


    def start_game(self):
        self.background = SCREENS['blank']
        self.start_button.kill()
        self.create_prize_tree()

        # game buttons
        InteractiveButton(GAME_BUTTONS['SURFS'], GAME_BUTTONS["POS"]["top_left"], GAME_BUTTONS["size"], (self.game_buttons, self.all_sprites), self.check_result)
        InteractiveButton(GAME_BUTTONS['SURFS'], GAME_BUTTONS["POS"]["top_right"], GAME_BUTTONS["size"], (self.game_buttons, self.all_sprites), self.check_result)
        InteractiveButton(GAME_BUTTONS['SURFS'], GAME_BUTTONS["POS"]["bottom_left"], GAME_BUTTONS["size"], (self.game_buttons, self.all_sprites), self.check_result)
        InteractiveButton(GAME_BUTTONS['SURFS'], GAME_BUTTONS["POS"]["bottom_right"], GAME_BUTTONS["size"], (self.game_buttons, self.all_sprites), self.check_result)

        # lifelines
        InteractiveButton(LIFELINES['SURFS'], LIFELINES["POS"][0], LIFELINES["size"], (self.lifelines, self.all_sprites), self.activate_x2, "X2")
        InteractiveButton(LIFELINES['SURFS'], LIFELINES["POS"][1], LIFELINES["size"], (self.lifelines, self.all_sprites), self.activate_revive, "Revive")
        InteractiveButton(LIFELINES['SURFS'], LIFELINES["POS"][2], LIFELINES["size"], (self.lifelines, self.all_sprites), self.activate_switch, "Switch")
        InteractiveButton(LIFELINES['SURFS'], LIFELINES["POS"][3], LIFELINES["size"], (self.lifelines, self.all_sprites), self.activate_magic_cup, "Magic Cup")
        self.update_current_question(self.questions[0])

    def update_current_question(self, question):
        self.current_question = question
        answers = [self.current_question["correct_answer"], self.current_question["incorrect_answers"][0], self.current_question["incorrect_answers"][1], self.current_question["incorrect_answers"][2]]
        random.shuffle(answers)
        self.question_sprite.kill()
        self.question_sprite = TextSprite(self.current_question["question"], (5*WINDOW_WIDTH / 8, WINDOW_HEIGHT / 8), "white", 2*WINDOW_WIDTH/3, WINDOW_WIDTH / 32, (self.all_sprites))
        
        for answer, button in zip(answers, self.game_buttons):
            button.update_text(answer)
            if answer == self.current_question['correct_answer']:
                self.correct_button = button

        
    def update_round(self):
        # update prize button colour
        list(self.prize_buttons)[self.round_number].deactivate()
        for game_button in self.game_buttons:
            if not game_button.is_active:
                game_button.reactivate()

        self.x2_active = False
        self.round_number += 1
        self.update_current_question(self.questions[self.round_number])

    def check_result(self):
        if self.choice.text == self.current_question["correct_answer"]:
            self.update_round()
        elif self.x2_active:
            self.choice.deactivate()
            self.x2_active = False
        else:
            self.background = SCREENS['lose']
            self.game_buttons.empty()
            self.all_sprites.empty()
            self.state = 'lose'
            self.running = False

    def import_questions(self):
        self.easy_questions = []
        medium_questions = []
        hard_questions = []
        with open('assets/trivia.json', 'r') as file:
            questions = json.load(file)
            for question in questions:
                if question["difficulty"] == "easy":
                    self.easy_questions.append(question)
                elif question["difficulty"] == "medium":
                    medium_questions.append(question)
                elif question["difficulty"] == "hard":
                    hard_questions.append(question)
        random.shuffle(self.easy_questions)
        self.questions = self.easy_questions[:5] + random.sample(medium_questions, k=5) + random.sample(hard_questions, k=5)
        self.easy_questions = self.easy_questions[5:]

    def run(self):
        while self.running:
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.game_buttons:
                        if button.rect.collidepoint(event.pos):
                            self.choice = button
                            button.is_clicked()
                    for button in self.lifelines:
                        if button.rect.collidepoint(event.pos) and button.is_active:
                            button.is_clicked()
                            button.deactivate()
                    if self.magic_cup_active == True:
                        for magic_cup in self.magic_cups:
                            if magic_cup.rect.collidepoint(event.pos):
                                self.reactivate_game_buttons(magic_cup.number)
                                magic_cup.hide()
                                self.magic_cup_timer.activate()
                                self.magic_cup_active = False


                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
            
            pygame.display.get_surface().blit(self.background, (0,0))
            self.all_sprites.update()
            pygame.display.update()
            self.magic_cup_timer.update()
            
        if self.state == 'lose':
            time.sleep(3)        
game = TriviaGame()
game.run()
pygame.quit()