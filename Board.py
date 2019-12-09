from State import *
from tkinter import *
from tkinter import ttk
import random

class Board:
    def __init__(self, tk, difficulty):
        self.tk = tk
        self.difficulty = difficulty
        self.flagging = False
        self.WINNER = False
        self.setup()

    def setup(self):
        self.num_blocks = self.difficulty * 10
        self.num_bombs = int(self.num_blocks**2 * (0.1 + 0.04*self.difficulty))
        self.bomb_unknown = self.num_bombs
        self.unrevealed_blocks = self.num_blocks ** 2
        self.board = [[0 for y in range(self.num_blocks)] for x in range(self.num_blocks)]
        self.states = [[State() for y in range(self.num_blocks)] for x in range(self.num_blocks)]

        #Place bombs on field
        for j in range(self.num_bombs):
            x = random.randint(0, self.num_blocks - 1)
            y = random.randint(0, self.num_blocks - 1)
            while (self.board[x][y] == -1 or (x == 0 and y  == 0)):
                x = random.randint(0, self.num_blocks - 1)
                y = random.randint(0, self.num_blocks - 1)

            self.board[x][y] = -1
            for m in range(-1,2):
                if(x + m < 0 or x + m >= self.num_blocks):
                    continue
                for n in range(-1,2):
                    if (y + n < 0 or y + n >= self.num_blocks):
                        continue
                    if(self.board[x + m][y + n] != -1):
                        self.board[x + m][y + n] += 1

        #Setup the buttons
        self.buttons = [[0 for y in range(self.num_blocks)] for x in range(self.num_blocks)]
        for i in range (self.num_blocks):
            for j in range(self.num_blocks):
                button = ttk.Button(self.tk, width=2, text = " ", command = lambda i=i, j=j: self.click([i, j]))
                button.grid(column = i, row = j + 1)
                self.buttons[i][j] = button

    def flag(self, i, j):
        state = self.states[i][j].get()
        if (state == 0):
            self.bomb_unknown -= 1
            self.buttons[i][j].configure(text = "X")
        elif(state == 2):
            self.bomb_unknown += 1
            self.buttons[i][j].configure(text = " ")
        self.states[i][j].flag()

    def end_game(self, ind = None):
        self.tk.update()
        
        Header = ["LOSER", "WINNER"]
        Info_1 = ["LOST", "WON"]
        Info_2 = ["EASY", "MEDIUM", "HARD"]
        messagebox.showinfo(Header[int(self.WINNER)], "You " + Info_1[int(self.WINNER)] + " in " + Info_2[self.difficulty - 1] + " mode!!!")
        self.tk.destroy()

    def click(self, ind):
        i, j  = ind
        clicked = []
        self.num_blocks = self.difficulty * 10
        state = self.states[i][j].get()
        if (self.flagging):
            clicked = [ind]
            self.flag(i, j)
        elif(state == 0):
            clicked = [ind]
            self.states[i][j].reveal()
            if (self.board[i][j] == -1):
                self.buttons[i][j].configure(style="bomb.TButton", text = 'X')
                self.buttons[i][j].state(["disabled"])
                self.end_game()
            else:
                txt = str(self.board[i][j])
                if (self.board[i][j] == 0):
                    txt = " "
                    for m in range(-1,2):
                        if(i + m < 0 or i + m >= self.num_blocks):
                            continue
                        for n in range(-1,2):
                            if (j + n < 0 or j + n >= self.num_blocks):
                                continue
                            next_clicked = Board.click(self, [i + m, j + n])
                            if(len(next_clicked) > 0):
                                clicked.extend(next_clicked)
                self.buttons[i][j].configure(style="flat.TButton", text = txt)
                self.buttons[i][j].state(["disabled"])
                self.unrevealed_blocks -= 1
                if (self.unrevealed_blocks - self.num_bombs == 0):
                    self.WINNER = True
                    self.end_game()
        return clicked
        
