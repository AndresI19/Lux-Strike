from Player import MOB
import pygame
from RNG import seed_random_bound_int

class ENEMIES():
    def __init__(self,Screen,Max_Parameters,World):
        self.Group = []
        self.max_enemies = 15
        self.Screen = Screen
        self.Max_Parameters = Max_Parameters
        self.spawn_random(World.seed)

    def spawn_random(self,seed):
        for i in range(self.max_enemies):
            Mx = (0,self.Max_Parameters[0]-1)
            My = (0,self.Max_Parameters[1]-1)
            x = seed_random_bound_int(seed,Mx,i)
            y = seed_random_bound_int(seed,My,i+1)
            Enemy = enemy(self.Screen,(y,x),self.Max_Parameters)
            self.Group.append(Enemy)

    def Draw(self):
        if len(self.Group) > 0:
            for i in range(len(self.Group)):
                self.Group[i].Draw()

    def update_player_location(self,x,y):
        for i in range(len(self.Group)):
            self.Group[i].update_player_location(x,y)

    def set_direction(self):
        for i in range(len(self.Group)):
            self.Group[i].set_direction()

    def translate(self,x,y):
        for i in range(len(self.Group)):
            self.Group[i].translate(x,y)

    def update_coordinates(self,World):
        for i in range(len(self.Group)):
            self.Group[i].update_coordinates(World)

class enemy(MOB):
    def __init__(self,Screen,coordinates,Max_Parameters):
        MOB.__init__(self,Screen,coordinates,Max_Parameters)
        self.MOB_image = pygame.image.load('Enemies/Swanzai.png').convert()
        self.MOB_image.set_colorkey((255,0,255))
        self.MOB_rect = self.MOB_image.get_rect()
        
        self.Player_location = (0,0)
        self.direction = 'S'

        self.aware = False

    def update_player_location(self,x,y):
        self.Player_location = (x,y)

    def set_direction(self):
        dx = self.Player_location[0] - self.x
        dy = self.Player_location[1] - self.y
        if dx == 0 and dy%2 == 0:
            if dy < 0:
                self.direction = 'S'
                self.dx = 0 
                self.dy = -2
            else:
                self.direction = 'N'
                self.dx = 0 
                self.dy = 2
        elif dx < 0:

            if dy < 0:
                self.direction = 'SW'
                self.dy = -1
            else:
                self.direction = 'NW'
                self.dy = 1
            if self.off_center == 1:
                self.dx = 0 
            else:
                self.dx = -1
        else:
            if dy < 0:
                self.direction = 'SE'
                self.dy = -1
            else:
                self.direction = 'NE'
                self.dy = 1
            if self.off_center == 1:
                self.dx = 1
            else:
                self.dx = 0
    
        