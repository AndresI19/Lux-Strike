import pygame
#drops
"""We all knew we would get here one day"""
##new file, early comments and refactorying
class Drop_envelope():
    def __init__(self):
        self.Group = []

    def check_pick_up(self,Player):
        for drop in self.Group:
            if Player.x == drop.x and Player.y == drop.y:
                drop.functionality()
                self.Group.remove(drop)

    def translate(self,x,y):
        for drop in self.Group:
            drop.translate(x,y)

class Drops():
    def __init__(self,Screen,coords,position):
        self.Screen = Screen #needed for graphics
        self.x = 0
        self.y = 0

    def image_init(self):
        colorkey = (255,0,255)
        self.image.set_colorkey(colorkey)
        self.rect = self.image.get_rect()
    
    def position(self,coords,position):
        self.x = coords[0]
        self.y = coords[1]
        self.rect.centerx = position[0]
        self.rect.bottom = position[1]

    def draw(self):
        self.Screen.blit(self.image,self.rect)

    def translate(self,x,y):
        self.rect.centerx += x
        self.rect.bottom += y

class Money_drop(Drops):
    def __init__(self,Screen,Ctrl_Vars,coords,position):
        Drops.__init__(self,Screen,coords,position)
        self.Ctrl_Vars = Ctrl_Vars
        self.value = 1000
        self.image = pygame.image.load('Drops/Money.png').convert()
        self.image_init()
        self.position(coords,position)

    def functionality(self):
        self.Ctrl_Vars.wallet += self.value

class Key(Drops):
    def __init__(self,Screen,Ctrl_Vars,coords,position):
        Drops.__init__(self,Screen,coords,position)
        self.Ctrl_Vars = Ctrl_Vars
        self.image = pygame.image.load('Drops/Key.png').convert()
        self.position(coords,position)

    def functionality(self):
        self.Ctrl_Vars.keys = 1