import pygame
import numpy as np
from snake import Snake
from math import floor
import pygame.freetype

pygame.init()
pygame.freetype.init()

black = (0,0,0)
white = (255,255,255)
green = (255,0,0)
blue = (0,0,255)

class text():

    def __init__(self, txt, font, fg_color, bg_color, parent, under = None, ymargin = 10):
        self.text = txt
        self.font = font
        self.fg = fg_color
        self.bg = bg_color
        self.parent = parent
        self.under = under

        self.img, self.textRect = self.font.render(self.text, self.fg, self.bg)
        if self.under is not None:
            self.pos_under(self.under, ymargin)
        
    def pos_under(self, obj, ymargin = 10):
        
        self.textRect.midtop = obj.textRect.midbottom
        self.textRect.y += ymargin
        self.under = obj
        
    def update(self, newtxt = None):
        
        self.text = newtxt
        self.img, self.textRect = self.font.render(self.text, self.fg, self.bg)

        if self.under is not None:
            self.pos_under(self.under)
        
    def display(self):
        self.parent.blit(self.img, self.textRect)
        
class death_screen():
    
    def __init__(self, parent: "game_of_snake"):
        
        self.parent = parent
        self.screen = parent.screen
        self.bg = parent.bg_color
        self.fg = parent.tile_color

        self.width = int(self.parent.width / 2)
        self.height = int(self.parent.height / 3); 
        self.surface = pygame.Surface([self.width, self.height]); self.surface.fill(self.bg)
        
    def draw(self):
        
        self.score = self.parent.snake.score
        self.hs = self.parent.hs
        
        self.died_text = text('You Died', self.parent.header, self.fg, self.bg, self.surface)
        self.died_text.textRect.center = (int(self.width / 2), 25)
        self.died_text.display()

        self.score_text = text(f'Your Score: {self.score}', self.parent.body, self.fg, self.bg, self.surface, under = self.died_text, ymargin = 15)
        self.score_text.display()

        self.hs_text = text(f'High Score: {self.hs}', self.parent.body, self.fg, self.bg, self.surface, under = self.score_text, ymargin = 10)
        self.hs_text.display()

        self.playagain_text = text('Press "R" to play again', self.parent.body, self.fg, self.bg, self.surface, under = self.hs_text, ymargin = 15)
        self.playagain_text.display()
        
        self.rect = self.surface.get_rect(center = (self.width, self.height))
        self.borders = (
            (0,0),
            (0,self.height),
            (self.width,self.height),
            (self.width,0),(0,0)
        )
        
        for i,bd in enumerate(self.borders[:-1]):
            pygame.draw.line(self.surface, self.fg, bd,self.borders[i + 1], 5)
            
        self.screen.blit(self.surface,self.rect)
        

class game_of_snake():

    def __init__(self, margins = [30,30,60,50], size = 20, walls_kill = True, play_mode = 'human', fps = 5,
                        snake_color = green, bg_color = black, tile_color = white, food_color = blue):    
        
        self.bg_color = bg_color
        self.snake_color = snake_color
        self.food_color = food_color
        self.tile_color = tile_color
        self.FPS = fps
        self.walls_kill = walls_kill
        self.hs = 0

        if play_mode == 'AI':
            self.FPS = 60

        (self.xmargin_l, self.xmargin_r, self.ymargin_t, self.ymargin_b) = margins
        self.size = size

        self.xmargin = (self.xmargin_l + self.xmargin_r)
        self.ymargin = (self.ymargin_t + self.ymargin_b)
        self.margins = (
                        (self.xmargin_l - 5,self.ymargin_t - 5), (self.xmargin_l - 5,self.ymargin_t + 15*self.size + 5),
                        (self.xmargin_l + 17*self.size + 5,self.ymargin_t + 15*self.size + 5),
                        (self.xmargin_l + 17*self.size + 5,self.ymargin_t - 5), (self.xmargin_l - 5,self.ymargin_t - 5)
                        )

        self.header = pygame.freetype.SysFont('freesansbold.ttf',24)
        self.body = pygame.freetype.SysFont('freesansbold.ttf',16)
        
        self.screen = pygame.display.set_mode(
            (17*self.size+self.xmargin,15*self.size + self.ymargin),
            0,32
        )
        self.dims = (self.screen.get_height(), self.screen.get_width())
        self.height, self.width = self.dims

        self.screen.fill(bg_color)
        pygame.display.set_caption('Snake')
        self.death_screen = death_screen(self)
 
    def play_game(self):  
        # resets snake, food, and score
        self.game_tiles = np.zeros((15,17))
        self.game_tiles[7][11] = 3 

        self.snake = Snake(5,8, self.game_tiles,length = 3,walls_kill = self.walls_kill); self.snake.food_coords = (7,11)
        self.score_text = text('Score: 0', self.header, self.tile_color, self.bg_color, self.screen)  
        self.gameclock = pygame.time.Clock()
        self.CarryOn = True   
        
        while self.CarryOn:
        
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    self.CarryOn = False
                    
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and self.snake.facing != 'd' and self.long_enough:
                        self.snake.turn('u')
                        self.long_enough = False

                    elif (event.key  == pygame.K_RIGHT or event.key == pygame.K_d) and self.snake.facing != 'l' and self.long_enough:
                        self.snake.turn('r')
                        self.long_enough = False

                    elif (event.key  == pygame.K_DOWN or event.key == pygame.K_s) and self.snake.facing != 'u' and self.long_enough:
                        self.snake.turn('d')
                        self.long_enough = False

                    elif (event.key  == pygame.K_LEFT or event.key == pygame.K_a) and self.snake.facing != 'r' and self.long_enough:
                        self.snake.turn('l')
                        self.long_enough = False

                    elif event.key == pygame.K_r and not self.snake.alive:
                        self.play_game()
                   
            self.screen.fill((0,0,0))
            self.snake.update()
            
            for i in range(len(self.margins)-1):
                pygame.draw.line(self.screen, self.tile_color, self.margins[i], self.margins[i + 1], 5)

            for i in range(17):
                for j in range(15):
                    pygame.draw.rect(
                        self.screen,
                        [self.tile_color,self.snake_color,self.snake_color,self.food_color][int(self.snake.grid[j,i])],
                                                (self.xmargin_l + i*self.size + 2, self.ymargin_t + j*self.size + 2,16,16))
            
            self.score_text.update(f'Score: {self.snake.score}'); self.score_text.textRect.topleft = (self.xmargin_l - 5, self.ymargin_t - 40); self.score_text.display()
            if not self.snake.alive:
                self.hs = max(self.hs, self.snake.score)
                self.death_screen.draw()

            pygame.display.flip(); 
            self.long_enough = True
            self.gameclock.tick(self.FPS + floor(self.snake.score / 10))

if __name__ == '__main__':
    game1 = game_of_snake(fps=5)
    game1.play_game()