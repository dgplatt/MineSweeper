from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from Board import *
from Auto_Board import *

class MineSweeper:
    def __init__(self):
        self.games_won = 0
        self.play = False
        self.setup()

    def setup(self):
        self.play = False
        self.set_difficulty()
        if (not self.play):
            return
        self.Tk = Tk()
        self.Tk.title("MineSweeper")

        #Setup File Menu
        menu = Menu(self.Tk)
        self.Tk.config(menu=menu)
        s = ttk.Style(self.Tk)
        s.theme_use('default')
        s.map("flat.TButton",
            foreground=[('disabled', 'black')],
            background=[('disabled', 'white')],
            relief =[('disabled', 'flat')]
            )
        s.map("bomb.TButton",
            foreground=[('disabled', 'white')],
            background=[('disabled', 'black')],
            relief =[('disabled', 'flat')]
            )    
        filemenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New Game", command=self.new_game)
        filemenu.add_command(label="Auto", command=self.Tk.quit)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=self.end_game)

        #Setup Help Menu
        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=lambda: print("about"))

        #Setup On-Screen Buttons
        New_Game = Radiobutton(self.Tk, text = "New Game", width=16, indicatoron = 0, command = lambda: self.new_game(), value = 2)
        New_Game.grid(column = 0, row = 0, columnspan = 6)
        Flag = Radiobutton(self.Tk, text = "Flag", indicatoron = 0, value = 1, width = 10)
        def flag():
            if(self.board.flagging):
                Flag.deselect()
            else:
                Flag.select()
            self.board.flagging = not self.board.flagging

        Flag.config(command = lambda: flag())
        Flag.grid(column = 6, row = 0, columnspan = 4)

        #setup board
        self.board = Auto_Board(self.Tk, self.difficulty)
        while(True):
            self.board.click()
            try:
                self.Tk.update()
            except:
                break
        #Setup Loop
        self.Tk.mainloop()

        if(self.board.WINNER):
            self.games_won += 1

        #End Game or New Game
        self.setup()
            

    def set_difficulty(self):
        root = Tk()
        s = ttk.Style(root)
        s.theme_use('default')
        root.title("MineSweeper")
        lbl = Label(root, text="Choose difficulty")
        lbl.pack()

        def click(x):
            self.play = True
            root.destroy()
            self.difficulty = x

        def close():
            root.destroy()

        Easy = ttk.Button(root, text="Easy", width=22, command=lambda: click(1))
        Easy.pack()
        Medium = ttk.Button(root, text="Medium",  width=22, command=lambda: click(2))
        Medium.pack()
        Hard = ttk.Button(root, text="Hard", width=22, command=lambda: click(3))
        Hard.pack()
        Close = ttk.Button(root, text="Close", width=22, command=lambda: close())
        Close.pack()
        root.mainloop()

    def new_game(self):
        self.Tk.destroy()
        self.setup()
    
    def end_game(self):
        self.Tk.destroy()

if __name__ == "__main__":
    game = MineSweeper()

