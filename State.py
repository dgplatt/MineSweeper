class State():
    def __init__(self):
        self.state = 0

    def get(self):
        return self.state

    def reveal(self):
        if(self.state == 0):
            self.state = 1
    
    def flag(self):
        if(self.state == 0):
            self.state = 2
        elif (self.state == 2):
            self.state = 0