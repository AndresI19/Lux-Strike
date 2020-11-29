import pygame
from math import floor
from random import randint
from Control_variables import Screen,ScreenRect
#drops
"""We all knew we would get here one day"""
##new file, early comments and refactorying
class Drop_envelope():
    def __init__(self,HUD,Stats,DATA = None):
        self.Group = []
        self.Money_Group = []
        self.HUD = HUD
        self.Stats = Stats
        if DATA != None:
            for data in DATA['Drops']:
                ID,coords,position,value = data
                if ID == 0:
                    drop = Money_drop(coords,position,None,value)
                elif ID == 1:
                    drop = Key(coords,position)
                self.Group.append(drop)

    def enemy_drop(self,Enemy,coords):
        if Enemy.key == True:
            drop = Key(
                coords,[Enemy.MOB_rect.centerx,Enemy.MOB_rect.bottom]
            )
            self.Group.append(drop)
        else:
            self.build_money(coords,[Enemy.MOB_rect.centerx,Enemy.MOB_rect.bottom])

    def build_money(self,coords,position):
        col,row = coords
        for drop in self.Group:
            if drop.value > 0:
                if  drop.col == col and drop.row == row:
                    value = drop.value + 10 * (self.Stats.combo + 1)
                    new_drop = Money_drop(coords,position,None,value)
                    self.Group.remove(drop)
                    self.Group.append(new_drop)
                    return
        new_drop = Money_drop(coords,position,self.Stats.combo)
        self.Group.append(new_drop)

    def check_pick_up(self,Player):
        for drop in self.Group:
            if Player.col == drop.col and Player.row == drop.row:
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
    def __init__(self,coords,position):
        self.col = 0
        self.row = 0
        self.render = True

    def image_init(self):
        colorkey = (255,0,255)
        self.image.set_colorkey(colorkey)
        self.rect = self.image.get_rect()
    
    def position(self,coords,position):
        self.col,self.row = coords
        self.rect.centerx = position[0]
        self.rect.bottom = position[1]

    def draw(self):
        if self.render:
            Screen.blit(self.image,self.rect)

    def translate(self,x,y):
        self.rect.centerx += x
        self.rect.bottom += y
        self.check_render()

    def check_render(self):
        self.render = False
        if self.rect.bottom >= 0 and self.rect.top <= ScreenRect.bottom:
            if self.rect.right >= 0 and self.rect.left <= ScreenRect.right:
                self.render = True

    def SFX(self):
        choice = randint(0,2)
        sound = pygame.mixer.Sound('SFX/Money{}.wav'.format(choice)
            )
        pygame.mixer.Sound.play(sound)

class Money_drop(Drops):
    def __init__(self,coords,position,combo = None,value = None):
        Drops.__init__(self,coords,position)
        self.ID = 0
        if value == None:
            self.value = 10 * (combo + 1)
            x = combo + 1
        else:
            self.value = value
            x = value//10 
        if x >= 16:
            x = 16
        self.image = pygame.image.load('Drops/Money{}.png'.format(x)
        ).convert()
        self.image_init()
        self.position(coords,position)

    def functionality(self,Player):
        Player.Stats.Money += self.value

class Key(Drops):
    def __init__(self,coords,position):
        Drops.__init__(self,coords,position)
        self.ID = 1
        self.image = pygame.image.load('Drops/Key.png').convert()
        self.image_init()
        self.position(coords,position)
        self.value = 0

    def functionality(self,Player):
        Player.Stats.keys = 1

    def SFX(self):
        sound = pygame.mixer.Sound('SFX/key got.wav')
        pygame.mixer.Sound.play(sound)