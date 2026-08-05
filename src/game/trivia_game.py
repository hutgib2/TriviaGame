from game.settings import *
from game.support import *
from game.button import *
from game.textSprite import TextSprite
from game.cup import Cup
from game.timer import Timer
from game.async_clock import AsyncClock
from game.api import fetchTriviaQuestions
import random
import json

class TriviaGame():
    def __init__(self):
        # general
        self.clock = AsyncClock()
        self.running = True
        self.state = 'game'
        self.background = SCREENS['blank']

        # groups
        self.game_buttons = pygame.sprite.Group()
        self.prize_buttons = pygame.sprite.Group()
        self.lifelines = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.magic_cups = pygame.sprite.Group()

        # questions
        self.load_backup_questions()
        self.current_question = None
        self.choice = None
        self.round_number = 0
        self.question_sprite = TextSprite('', (5*WINDOW_WIDTH / 8, WINDOW_HEIGHT / 8), "white", 2*WINDOW_WIDTH/3, WINDOW_WIDTH / 32, (self.all_sprites))
        self.correct_button = None
        
        # lifelines
        self.x2_active = False
        self.magic_cup_active = False
        self.magic_cup_timer = Timer(2000, lambda: {cup.kill() for cup in self.magic_cups})

    def load_backup_questions(self):
        with open('assets/backup_questions.json', 'r') as file:
            backup_questions = json.load(file)
        
        self.easy_backup_qs = []
        self.medium_backup_qs = []
        self.hard_backup_qs = []

        for question in backup_questions:
            if question["difficulty"] == "easy":
                self.easy_backup_qs.append(question)
            elif question["difficulty"] == "medium":
                self.medium_backup_qs.append(question)
            elif question["difficulty"] == "hard":
                self.hard_backup_qs.append(question)
        
    async def fetch_questions(self):
        questions = await fetchTriviaQuestions(50)
        self.easy_questions = []
        medium_questions = []
        hard_questions = []

        # organise each question by difficulty
        for question in questions:
            if question["difficulty"] == "easy":
                self.easy_questions.append(question)
            elif question["difficulty"] == "medium":
                medium_questions.append(question)
            elif question["difficulty"] == "hard":
                hard_questions.append(question)

        # print(f'easy amount: {len(self.easy_questions)}')
        # print(f'medium amount: {len(medium_questions)}')
        # print(f'hard amount: {len(hard_questions)}')

        # because we cant control how many easy medium and hard qs we recieve, we need to check we have enough
        # we need to check that we have at least 7 easy, 5 medium and 5 hard question,
        # if not, we need to pull some from the local backup db
        if len(self.easy_questions) < 7:
            self.easy_questions.append(random.sample(self.easy_backup_qs, k=(7-len(self.easy_questions))))
        if len(medium_questions) < 5:
            self.medium_questions.append(random.sample(self.medium_backup_qs, k=(5-len(self.medium_questions))))
        if len(hard_questions) < 5:
            self.hard_questions.append(random.sample(self.hard_backup_qs, k=(5-len(self.hard_questions))))
            
        self.questions = self.easy_questions[:5] + random.sample(medium_questions, k=5) + random.sample(hard_questions, k=5)

        # backup easy questions for switch lifeline
        self.easy_questions = self.easy_questions[5:]

    # lifelines activation
    def activate_x2(self):
        self.x2_active = True

    def activate_revive(self):
        deactivated_lifelines = []
        for lifeline in self.lifelines:
            if lifeline.is_active == False:
                deactivated_lifelines.append(lifeline)
        if len(deactivated_lifelines) == 0:
            return

        random.choice(deactivated_lifelines).reactivate()

    def activate_switch(self):
        self.update_current_question(self.easy_questions.pop())
        for button in self.game_buttons:
            if not button.is_active:
                button.reactivate()

    def activate_magic_cup(self):
        self.magic_cup_active = True
        self.activated_buttons = []

        for game_button in self.game_buttons:
            if game_button.is_active:
                self.activated_buttons.append(game_button)
                game_button.deactivate()

        numbers = []
        for i in range(len(self.activated_buttons)):
            numbers.append(i)
        random.shuffle(numbers)
        
        for i in range(len(self.activated_buttons)):
            Cup(MAGIC_CUPS['POS'][i], numbers.pop(), (self.magic_cups, self.all_sprites))

    def reactivate_game_buttons(self, cup_number):
        self.correct_button.reactivate()
        number_of_buttons_to_reactivate = len(self.activated_buttons) - cup_number - 1

        for button in self.activated_buttons:
            if number_of_buttons_to_reactivate == 0:
                break
            if button != self.correct_button:
                button.reactivate()
                number_of_buttons_to_reactivate -= 1


    def create_prize_tree(self):
        # draw 15 increasing values of money on the far left of the screen from bottom to top
        for i in range(70, 1, -5):
            Button(PRIZE_BUTTONS,  (WINDOW_WIDTH / 10, (i*WINDOW_HEIGHT / 75)), (WINDOW_WIDTH / 11, WINDOW_HEIGHT / 15), (self.prize_buttons, self.all_sprites))
        for prize, button in zip(prize_money, self.prize_buttons):
            button.update_text(prize)

    def start_game(self):
        # self.background = SCREENS['blank']
        # self.start_button.kill()
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

        InteractiveButton(WALK_AWAY['SURFS'], WALK_AWAY["pos"], WALK_AWAY["size"], (self.lifelines, self.all_sprites), lambda: self.end_game("walk_away"), "")
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

    def end_game(self, state):
        self.background = SCREENS[state]
        self.game_buttons.empty()
        self.all_sprites.empty()
        self.state = state
        self.running = False
        
    def update_round(self):
        # update prize button colour
        list(self.prize_buttons)[self.round_number].deactivate()
        for game_button in self.game_buttons:
            if not game_button.is_active:
                game_button.reactivate()

        self.x2_active = False
        self.round_number += 1
        if self.round_number >= len(self.questions):
            self.end_game('win')
        else:
            self.update_current_question(self.questions[self.round_number])

    def check_result(self):
        if self.choice.text == self.current_question["correct_answer"]:
            self.update_round()
        elif self.x2_active:
            self.choice.deactivate()
            self.x2_active = False
        else:
            self.end_game('lose')

    async def run(self):
        await self.fetch_questions()
        self.start_game()

        while self.running:
            await self.clock.tick()
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    self.running = False
                    self.state = 'quit'
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
            
            pygame.display.get_surface().blit(self.background, (0,0))
            self.all_sprites.update()
            pygame.display.update()
            self.magic_cup_timer.update()
        
        await asyncio.sleep(3)