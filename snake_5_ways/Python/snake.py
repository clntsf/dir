import numpy as np

class Snake():

    def __init__(self, posx, posy, grid: np.ndarray, facing = 'r', length = 2, play_mode = 'human', walls_kill = True):
        
        self.directions = {
            'u': [-1,0],
            'd': [1,0],
            'r': [0,1],
            'l': [0,-1]
        }
        self.food_coords = (0,0)

        self.posx = posx-1
        self.posy = posy-1

        self.dir = self.directions[facing]
        self.facing = facing

        self.len = length
        self.grid = grid
        self.segments = [[self.posy, self.posx]]
        
        self.score = 0
        self.alive = True
        self.walls_kill = walls_kill
        self.play_mode = play_mode
        
        for i in range(1,self.len+1):
            self.segments.append([self.posy - i * self.dir[0], self.posx - i * self.dir[1]] )

    def turn(self, direction):
        self.dir = self.directions[direction]
        self.facing = direction
        
    def feed(self):
        
        is_empty = False
        
        while not is_empty:
            
            self.food_coords = self.food_x, self.food_y = np.random.randint(16), np.random.randint(14)
            if [self.food_y, self.food_x] not in self.segments: self.grid[self.food_y][self.food_x] = 3; is_empty = True
            
    def die(self):
        self.alive = False
          
    def update(self):
        
        if 0 <= self.posx + self.dir[1] < 17 and 0 <= self.posy + self.dir[0] < 15: 
            self.posy += self.dir[0]; self.posx += self.dir[1]
            
        elif  self.walls_kill: self.die()
        elif self.facing in 'rl': 
            self.posx = 16 - self.posx
                
        else:  
            self.posy = 14 - self.posy
            
        if self.alive:
            
            for i in range(1,len(self.segments)): 
                self.segments[-i] = self.segments[-(i + 1)]
                
            self.segments[0] = [self.posy, self.posx]
            if self.grid[self.posy][self.posx] == 3: self.segments.append(self.segments[-1]); self.len += 1; self.score += 1; self.feed()
            elif self.grid[self.posy][self.posx] == 1: self.die()
            self.grid = np.where(self.grid != 3, 0, self.grid)
            
            for i in range(self.len): self.grid[self.segments[i][0]][self.segments[i][1]] = 1
            self.grid[self.posy][self.posx] = 2