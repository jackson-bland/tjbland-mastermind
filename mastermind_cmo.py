import random
import pygame
import copy

class Board:
    def __init__(self):
        self.peg_width = 75
        self.peg_height = 75
        self.red = pygame.image.load('red.png').convert()
        self.blue = pygame.image.load('blue.png').convert()
        self.white = pygame.image.load('white.png').convert()
        self.black = pygame.image.load('black.png').convert()
        self.green = pygame.image.load('green.png').convert()
        self.yellow = pygame.image.load('yellow.png').convert()
        self.blank = pygame.image.load('blank.png').convert()
        self.blank_key = pygame.image.load('blank_key.png').convert()
        self.white_key = pygame.image.load('white_key.png').convert()
        self.black_key = pygame.image.load('black_key.png').convert()
        self.corners = pygame.image.load('corners.png').convert()
        self.submit = pygame.image.load('submit.png').convert()
        self.reset = pygame.image.load('reset.png').convert()
        self.guess_cover = pygame.image.load('guess_cover.png').convert()
        self.color_list = [self.red, self.blue, self.white, self.black, self.green, self.yellow]

    def create_board(self, display):
        display.blit(self.reset, (0,60))
        display.blit(self.submit, (0,260))
        display.blit(self.guess_cover, (60, 0))
        for x in range(2):
            self.x_pos = x*300
            display.blit(self.corners, (self.x_pos,0))
        for x in range(6):
            self.x_pos = x*60
            display.blit(self.color_list[x], (self.x_pos, 660))
        for x in range(4):
            for y in range(10):
                self.x_pos = (x)*60 + 60
                self.y_pos = (y)*60 + 60
                self.position = (self.x_pos, self.y_pos)
                display.blit(self.blank, self.position)
                for x_ in range(2):
                    for y_ in range(2):
                        self.xp = 300 + x_*30
                        self.yp = self.y_pos + y_*30
                        display.blit(self.blank_key, (self.xp, self.yp))


    def reset_board(self, display):
        Board.create_board(self, display)
    

    def peg_placement(self, color, slot, row, display, guess_):
        if slot == 4:
            pass
        else:
            if color == 'red': 
                peg = self.red
                guess[slot] = 'r'
            elif color == 'blue':
                peg = self.blue
                guess[slot] = 'b'
            elif color == 'black':
                peg = self.black
                guess[slot] = 'bk'
            elif color == 'white':
                peg = self.white
                guess[slot] = 'w'
            elif color == 'green':
                peg = self.green
                guess[slot] = 'g'
            elif color == 'yellow':
                peg = self.yellow
                guess[slot] = 'y'
            elif color == 'blank':
                peg = self.blank
                guess[slot] = '_'

            display.blit(peg, ((slot+1) * 60, 600 - row*60))


    def compare(self, display, computer_guess, player_guess, row):
        black_keys = 0
        white_keys = 0
        key_placement = [0,1,2,3]     
        copy_list = copy.deepcopy(computer_guess)  
        if player_guess == computer_guess:
            win = True
        else:
            win = False
            for peg in range(4):
                if player_guess[peg] == computer_guess[peg]:
                    player_guess[peg] = '_'
                    computer_guess[peg] = '_'
                    black_keys += 1
            for peg in range(4):
                if player_guess[peg] in computer_guess and player_guess[peg] != '_':
                    for i in range(4):
                        if player_guess[peg] == computer_guess[i] and player_guess[peg] != '_':
                            computer_guess[i] = '_'
                            break
                    player_guess[peg] = '_'
                    white_keys += 1
        for b in range(black_keys):
            placement_ = random.choice(key_placement)
            key_placement.remove(placement_)
            if placement_ == 0:
                self.x_pos = 300
                self.y_pos =  600 - row*60
            elif placement_ == 1:
                self.x_pos = 330
                self.y_pos = 600 - row*60
            elif placement_ == 2:
                self.x_pos = 300
                self.y_pos = 600 - row*60 + 30
            elif placement_ == 3:
                self.x_pos = 330
                self.y_pos = 600 - row*60 + 30
            display.blit(self.black_key, (self.x_pos, self.y_pos))
        for w in range(white_keys):
            placement_ = random.choice(key_placement)
            key_placement.remove(placement_)
            if placement_ == 0:
                self.x_pos = 300
                self.y_pos =  600 - row*60
            elif placement_ == 1:
                self.x_pos = 330
                self.y_pos = 600 - row*60
            elif placement_ == 2:
                self.x_pos = 300
                self.y_pos = 600 - row*60 + 30
            elif placement_ == 3:
                self.x_pos = 330
                self.y_pos = 600 - row*60 + 30
            display.blit(self.white_key, (self.x_pos, self.y_pos))
        return copy_list, win


    def reveal(self, display, comp_guess):
        for x in range(4):
            if comp_guess[x] == 'r':   display.blit(self.red, (60 + x*60, 0))
            elif comp_guess[x] == 'b':   display.blit(self.blue, (60 + x*60, 0))
            elif comp_guess[x] == 'bk':   display.blit(self.black, (60 + x*60, 0))            
            elif comp_guess[x] == 'w':   display.blit(self.white, (60 + x*60, 0))
            elif comp_guess[x] == 'y':   display.blit(self.yellow, (60 + x*60, 0))
            elif comp_guess[x] == 'g':   display.blit(self.green, (60 + x*60, 0))

def computer_code():
    colors = ['r', 'bk', 'b', 'w', 'g', 'y']
    guess_ = []
    guess_copy = []
    for c in range(4):
        add_on = colors[random.randint(0, 5)]
        guess_.append(add_on)

    return guess_

# initialize
pygame.init()
pygame.display.set_caption('Mastermind')
window = pygame.display.set_mode([360,720])
board = Board()
board.create_board(window)
color = 'blank'
row = 0
slot = 4
timer = 0
clock = pygame.time.Clock()
FPS = 10
guess = ['_', '_', '_', '_']
comp_guess = computer_code()
win_cond = False

instructions = True
running = True
while running:

    if instructions:
        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, 20)
        instruc_message = font.render("Select Empty slot then peg color", True, (255,255,255))
        window.blit(instruc_message, (60,360))
        timer = timer + clock.tick(FPS)
        if timer > 3000:
            instructions = False
            board.create_board(window)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            placement = pygame.mouse.get_pos()

            # reset button
            if placement[0] <= 60 and placement[1] <= 260 and placement[1] >= 60:
                board.reset_board(window)
                guess = ['_', '_', '_', '_']
                row = 0 
                comp_guess = computer_code()
            # submit button
            elif placement[0] <=60 and placement[1] > 260 and placement[1] <= 660:
                submit_guess = guess
                guess = ['_', '_', '_', '_']
                
                if row == 10:
                        font_name = pygame.font.match_font('arial')
                        font = pygame.font.Font(font_name, 40)
                        lose_message = font.render("You lost", True, (255,255,255))
                        window.blit(lose_message, (100,360))
                else:
                    comp_guess, win_cond = board.compare(window, comp_guess, submit_guess, row)
                    if win_cond:
                        font_name = pygame.font.match_font('arial')
                        font = pygame.font.Font(font_name, 40)
                        win_message = font.render("YOU WON!!!!!", True, (255,255,255))
                        window.blit(win_message, (100,50))
                    else:
                        pass
                row += 1

            # color determination
            elif placement[0] <= 60 and placement[1] >= 660:
                color = 'red'
            elif placement[0] > 60 and placement[0] <= 120 and placement[1] >= 660:
                color = 'blue'
            elif placement[0] > 120 and placement[0] <= 180 and placement[1] >= 660:
                color = 'white'
            elif placement[0] > 180 and placement[0] <= 240 and placement[1] >= 660:
                color = 'black'
            elif placement[0] > 240 and placement[0] <= 300 and placement[1] >= 660:
                color = 'green'
            elif placement[0] > 300 and placement[1] >= 660:
                color = 'yellow'
            # slot determination
            elif placement[0] > 60 and placement[0] <= 120 and placement[1] < 660 and placement[1] >= 60:
                slot = 0
            elif placement[0] > 120 and placement[0] <= 180 and placement[1] < 660 and placement[1] >= 60:
                slot = 1
            elif placement[0] > 180 and placement[0] <= 240 and placement[1] < 660 and placement[1] >= 60:
                slot = 2
            elif placement[0] > 240 and placement[0] <= 300 and placement[1] < 660 and placement[1] >= 60:
                slot = 3
            elif placement[0] < 300 and placement[0] >= 60 and placement[1] < 60:
                board.reveal(window, comp_guess)
                font_name = pygame.font.match_font('arial')
                font = pygame.font.Font(font_name, 40)
                lose_message = font.render("You Gave Up", True, (255,255,255))
                window.blit(lose_message, (100,360))
            # peg placement
            board.peg_placement(color, slot, row, window, guess)
            color = 'blank'

    pygame.display.update()

pygame.quit()
