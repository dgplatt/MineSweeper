from Board import *
import numpy as np

class Auto_Board(Board):
    def __init__(self, tk, difficulty):
        super().__init__(tk, difficulty)
        self.num_unknowns = [[3 if ((x % (self.num_blocks - 1) == 0) and (y % (self.num_blocks - 1) == 0)) 
                                else 5 if ((x % (self.num_blocks - 1) == 0) or (y % (self.num_blocks - 1) == 0)) 
                                else 8 
                                for x in range(self.num_blocks)] 
                                for y in range(self.num_blocks)]
        self.bombs_around = [[None for x in range(self.num_blocks)] for y in range(self.num_blocks)]
        self.probs = [[None for x in range(self.num_blocks)] for y in range(self.num_blocks)]
        self.probs[0][0] = 0.0
        self.to_click_list = [([0,0], False)]
   
    def to_click(self):
        if (len(self.to_click_list) > 0):
            return self.to_click_list.pop()

        min_ind = [0,0]
        min_num = 1.0
        for i in range(self.num_blocks):
            for j in range(self.num_blocks):
                if (self.states[i][j].get() != 0):
                    continue
                if (self.probs[i][j] == None):
                    if (self.bomb_unknown/self.unrevealed_blocks < min_num):
                        min_ind = [i ,j]
                        min_num = self.num_bombs/self.unrevealed_blocks
                else:
                    if (self.probs[i][j] < min_num):
                        min_ind = [i ,j]
                        min_num = self.probs[i][j]
                    elif(self.probs[i][j] == 1.0):
                        return [i, j], True
        print(min_ind, min_num)
        return min_ind, False

    def add_prob(self, to_use):
        i, j, bombs_around, num_unknowns, sum_prob, fixed = to_use.pop()

        assign_prob = (bombs_around - sum_prob)/(num_unknowns - fixed)
        for m in range(-1,2):
            if(i + m < 0 or i + m >= self.num_blocks):
                continue
            for n in range(-1,2):
                if (j + n < 0 or j + n >= self.num_blocks or (m == 0 and n == 0) or self.probs[i + m][j + n] != None):
                    continue
                self.probs[i + m][j + n] = assign_prob
                if (assign_prob == 1.0):
                    self.to_click_list.append(([i + m, j + n], True))
                elif (assign_prob == 0.0):
                    self.to_click_list.append(([i + m, j + n], False))
    
    def end_game(self):
        if(not self.WINNER):
            for i in range(self.num_blocks):
                print(["%.1f" % self.probs[j][i] if self.probs[j][i] != None else " ? " for j in range(self.num_blocks)])
            print("***********************************")
        super().end_game()
        
    def click(self, ind = None):
        if(ind == None):
            ind, self.flagging = self.to_click()
        clicked = super().click(ind)
        #Adjust the number of bombs and the number of unknowns for the blocks around the clicked blocks
        for i, j in clicked:
            self.probs[i][j] = 0.0
            if (not self.flagging):
                self.bombs_around[i][j] = self.board[i][j]
            for m in range(-1,2):
                if(i + m < 0 or i + m >= self.num_blocks):
                    continue
                for n in range(-1,2):
                    if (j + n < 0 or j + n >= self.num_blocks or (m == 0 and n == 0)):
                        continue
                    self.num_unknowns[i + m][j + n] -= 1
                    if (self.flagging):
                        if(self.bombs_around[i + m][j + n] != None):
                            self.bombs_around[i + m][j + n] -= self.states[i][j].get() - 1
                    elif(self.states[i + m][j + n].get() == 2):
                        self.bombs_around[i][j] -= 1

        if (len(self.to_click_list) != 0):
            return clicked
        #Store info of all blocks that have an effect on the probablities on the board 
        # and reset probabilities
        to_use = []
        to_sort = []
        for i in range(self.num_blocks):
            for j in range(self.num_blocks):
                if(self.states[i][j].get() == 0):
                    self.probs[i][j] = None
                elif(self.states[i][j].get() == 1 and self.num_unknowns[i][j] != 0):
                    val = self.bombs_around[i][j]/self.num_unknowns[i][j]
                    if (val == 1 or val == 0):
                        to_use.append([i, j, self.bombs_around[i][j], self.num_unknowns[i][j], 0.0, 0])
                    else:
                        to_sort.append([i, j, self.bombs_around[i][j], self.num_unknowns[i][j], 0.0, 0])

        #Sort by the ones that have the most effect
        while(len(to_use) > 0):
            self.add_prob(to_use)

        if (len(self.to_click_list) != 0):
            return clicked
        while(len(to_sort) > 0 and len(to_use) == 0):
            to_keep = []
            for p in range(len(to_sort)):
                to_sort[p][4] = 0
                to_sort[p][5] = 0
                i, j, bombs_around, num_unknowns, sum_prob, fixed = to_sort[p]
                for m in range(-1,2):
                    if(i + m < 0 or i + m >= self.num_blocks):
                        continue
                    for n in range(-1,2):
                        if (j + n < 0 or j + n >= self.num_blocks or (m == 0 and n == 0) 
                            or self.probs[i + m][j + n] == None or self.states[i + m][j + n].get() != 0):
                            continue
                        to_sort[p][4] += self.probs[i + m][j + n]
                        to_sort[p][5] += 1
                if (to_sort[p][3] - to_sort[p][5] == 0):
                    continue
                val = (bombs_around - to_sort[p][4])/(num_unknowns - to_sort[p][5])
                if(val == 0.0):
                    to_use.append(to_sort[p])
                elif(val == 1.0):
                    to_use.insert(0,to_sort[p])
                else:
                    to_keep.append(p)

            while(len(to_use) > 0):
                self.add_prob(to_use)

            to_sort = [to_sort[i] for i in to_keep]
            if (len(self.to_click_list) != 0):
                break
            to_sort.sort(key = lambda to_sort: (-(to_sort[3] - to_sort[5]), (to_sort[2] - to_sort[4])/(to_sort[3] - to_sort[5])))
            if(len(to_sort) > 0):
                self.add_prob(to_sort)

        return clicked
        
    