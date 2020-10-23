import pygame
from math import floor
from random import randint
#drops
"""We all knew we would get here one day"""
##new file, early comments and refactorying
class Drop_envelope():
    def __init__(self,HUD):
        self.Group = []
        self.HUD = HUD

    def check_pick_up(self,Player):
        for drop in self.Group:
            if Player.x == drop.x and Player.y == drop.y:
                drop.functionality(Player)
                self.Group.remove(drop)
                #Player.Stats.Money += round(drop.value * (1 + Player.Stats.combo/2))
                self.HUD.Money_bar.queue()
                self.HUD.Keys.update()
                drop.SFX()

    def translate(self,x,y):
        for drop in self.Group:
            drop.translate(x,y)

class Drops():
    def __init__(self,Screen,coords,position):
        self.Screen = Screen #needed for graphics
        self.Screen_rect = Screen.get_rect()
        self.x = 0
        self.y = 0
        self.render = True

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
        if self.render:
            self.Screen.blit(self.image,self.rect)

    def translate(self,x,y):
        self.rect.centerx += x
        self.rect.bottom += y
        self.check_render()

    def check_render(self):
        self.render = False
        if self.rect.top >= 0 and self.rect.top <= self.Screen_rect.bottom:
            if self.rect.right >= 0 and self.rect.left <= self.Screen_rect.right:
                self.render = True

    def SFX(self):
        choice = randint(0,2)
        sound = pygame.mixer.Sound('SFX/Money{}.wav'.format(choice)
            )
        pygame.mixer.Sound.play(sound)

class Money_drop(Drops):
    def __init__(self,Screen,Ctrl_Vars,coords,position):
        Drops.__init__(self,Screen,coords,position)
        self.Ctrl_Vars = Ctrl_Vars
        self.value = 1000
        self.image = pygame.image.load('Drops/Money.png').convert()
        self.image_init()
        self.position(coords,position)

    def functionality(self,Player):
        #self.Ctrl_Vars.wallet += self.value
        Player.Stats.Money += round(self.value * (1 + Player.Stats.combo/2))

class Key(Drops):
    def __init__(self,Screen,Ctrl_Vars,coords,position):
        Drops.__init__(self,Screen,coords,position)
        self.Ctrl_Vars = Ctrl_Vars
        self.image = pygame.image.load('Drops/Key.png').convert()
        self.image_init()
        self.position(coords,position)
        self.value = 0

    def functionality(self,Player):
        Player.Stats.keys = 1

    def SFX(self):
        sound = pygame.mixer.Sound('SFX/key got.wav')
        pygame.mixer.Sound.play(sound)