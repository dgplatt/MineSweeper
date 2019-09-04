from tkinter import *
import tkinter
from tkinter import messagebox
import random

def create(int):
    num_blocks = int * 10
    num_bombs = int * 20
    board = [[0 for y in range(num_blocks)] for x in range(num_blocks)]
    j = 0
    while (j < num_bombs):
        x = random.randint(1, num_blocks - 1)
        y = random.randint(1, num_blocks - 1)
        if (board[x][y] != 9):
            board[x][y] = 9
            j += 1
    i = 0
    while (i < num_blocks):
        j = 0
        while(j < num_blocks):
            m = -1
            while(m <= 1 and board[i][j] != 9):
                n = -1
                while(n <= 1):
                    if(i + m < 0 or i + m >= num_blocks):
                        m += 1
                    elif (j + n < 0 or j + n >= num_blocks):
                        n += 1
                    elif(board[i + m][j + n] == 9):
                        board[i][j] += 1
                    n += 1
                m += 1
            j += 1
        i += 1
    return board


def play(x):
    game = Tk()
    game.title("MineSweeper")
    board = create(x)
    num_blocks = x * 10
    class counter:
        def __init__(self, x):
            self.c = (x * 10) ** 2 - x * 20
        def sub(self):
            self.c -= 1

    total_free = counter(x)

    class State:
        def __init__(self):
            self.b = False

        def switch(self):
            self.b = not self.b
    
    flagging = State()
    buttons = [[0 for y in range(num_blocks)] for x in range(num_blocks)]
    def new_game():
        game.destroy()
        difficulty()

    def reveal(i, j):
        if(buttons[i][j].cget('state') == 'disabled' or (buttons[i][j].cget('text') == 'X' and not flagging.b)):
            return
        if (flagging.b):
            if (buttons[i][j].cget('text') == 'X'):
                buttons[i][j].configure(text = '-')
            else:
                buttons[i][j].configure(text = 'X')
            return
        txt = str(board[i][j])
        print(txt)
        if (board[i][j] == 9):
            result = messagebox.askyesno ("GAMEOVER", "Play Again?")
            if (result):
                new_game()
            else:
                game.destroy()
                return
        if (board[i][j] == 0):
            txt = " "
        buttons[i][j].configure(state='disabled', text = txt)
        if (board[i][j] == 0):
            m = -1
            while(m <= 1 and board[i][j] != 9):
                n = -1
                while(n <= 1):
                    if(i + m < 0 or i + m >= num_blocks):
                        m += 1
                    elif (j + n < 0 or j + n >= num_blocks or (m == 0 and n == 0)):
                        n += 1
                    else:
                        reveal(i + m, j + n)
                        n += 1
                m += 1
        total_free.sub()
        if (total_free.c == 0):
            result = messagebox.askyesno ("WINNER", "Play Again?")
            if (result):
                new_game()
            else:
                game.destroy()
    
    menu = Menu(game)
    game.config(menu=menu)
    filemenu = Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="New Game", command=new_game)
    filemenu.add_command(label="Restart", command=game.quit)
    filemenu.add_command(label="Auto", command=game.quit)
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=game.quit)

    helpmenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="About...", command=lambda: print("about"))

    New_Game = Button(game, text = "New Game", command = new_game)
    New_Game.grid(column = 1, row = 0,columnspan = 4)
    Flag = Button(game, text = "Flag", command = lambda: flagging.switch())
    Flag.grid(column = 5, row = 0, columnspan = 2)
    for i in range (10 * x):
        for j in range(10 * x):
            button = Button(game, width=2, text = '-', bg = 'black')
            button.configure(command = lambda i=i, j=j: reveal(i, j))
            buttons[i][j] = button
            button.grid(column = i, row = j + 1)
    game.mainloop()

def difficulty():
    root = Tk()
    root.title("MineSweeper")
    lbl = Label(root, text="Choose difficulty")
    lbl.pack()
    def click(int):
        root.destroy()
        play(int)
    Easy = Button(root, text="Easy", width=8, command=lambda: click(1))
    Easy.pack()
    Medium = Button(root, text="Medium", width=8, command=lambda: click(2))
    Medium.pack()
    Hard = Button(root, text="Hard", width=8, command=lambda: click(3))
    Hard.pack()
    root.geometry('200x100')
    root.mainloop()

difficulty()
