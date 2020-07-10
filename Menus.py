import pygame
import Buttons

#Envelope class that contrains all start menu options and graphics vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
class Start_Envelope():
    def __init__(self,Screen,Ctrl_Vars):
        """self.Background = background(Screen)
        self.GonGrid = gonGrid(Screen)
        self.LUX_STRIKE = lUX_STRIKE(Screen)"""
        self.Still = still(Screen)
        self.Menus = []
        #Main options
        """These are folders, each contain a few more options within them"""
        self.Menus.append(Buttons.Settings(Screen,1,1,Ctrl_Vars))
        self.Menus.append(Buttons.Extras(Screen,1,2,Ctrl_Vars))
        self.Menus.append(Buttons.Play(Screen,2,3,Ctrl_Vars))

    def draw(self):
        """self.Background.draw()
        self.GonGrid.draw()
        self.LUX_STRIKE.draw()"""
        self.Still.draw()
        for i in range(len(self.Menus)):
            self.Menus[i].draw()

class Pause_Envelope():
    def __init__(self,Screen,Ctrl_Vars):
        self.Screen = Screen
        self.Screen_rect = self.Screen.get_rect()
        #Main options
        """These are folders, each contain a few more options within them"""
        self.Menus = []
        self.Menus.append(Buttons.Settings(Screen,1,1,Ctrl_Vars))
        self.Menus.append(Buttons.Extras(Screen,1,2,Ctrl_Vars))
        self.Menus.append(Buttons.Pause_play(Screen,2,3,Ctrl_Vars))

        self.text = "Paused"
        self.init_text(100)

    def init_text(self,size):
        self.text_color = ((255,255,255))
        self.font_size = size
        self.font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",self.font_size)
        self.font.set_bold(True)
        self.font_image = self.font.render(self.text,True,self.text_color,None)
        self.font_rect = self.font_image.get_rect()
        self.font_rect.centerx = self.Screen_rect.centerx
        self.font_rect.centery = 250

    def draw(self):
        self.Screen.fill((0,0,0))
        self.Screen.blit(self.font_image,self.font_rect)
        for i in range(len(self.Menus)):
            self.Menus[i].draw()
        
"""TODO: temporary use of a the pause screen as a mother class"""
class Game_Over_Envelope(Pause_Envelope):
    def __init__(self,Screen,Ctrl_Vars):
        Pause_Envelope.__init__(self,Screen,Ctrl_Vars)
        self.text = "Death"
        self.init_text(100)

class Game_Win_Envelope(Pause_Envelope):
    def __init__(self,Screen,Ctrl_Vars):
        Pause_Envelope.__init__(self,Screen,Ctrl_Vars)
        self.text = "Victory"
        self.init_text(100)

class Num_Pad():
    #TODO: Makes a number pad like on a phone for entering numbers. The functionality of this one can and should be generalized
    def __init__(self,Screen,Ctrl_Vars):
        self.Screen = Screen
        self.Ctrl_Vars = Ctrl_Vars
        self.seed = self.Ctrl_Vars.seed
        self.Screen = Screen
        self.Screen_rect = Screen.get_rect()
        self.text = "{}".format(self.seed)
        self.init_text(100)
        self.Menus_init()

    def Menus_init(self):
        self.Menus = []
        x = 3 #column
        y = 3 #row
        for i in range(9): #arranging main 9 numbers not including 0
            self.Menus.append(Buttons.Key(self.Screen,x,y,self.Ctrl_Vars,i+1))
            x += 1
            if x >= 6:
                y -= 1
                x = 3
        #arranging 0 and functional keys by hand
        self.Menus.append(Buttons.Del_Key(self.Screen,3,0,self.Ctrl_Vars)) 
        self.Menus.append(Buttons.Key(self.Screen,4,0,self.Ctrl_Vars,0)) 
        self.Menus.append(Buttons.Enter_Key(self.Screen,5,0,self.Ctrl_Vars)) 
        self.Menus.append(Buttons.Clear(self.Screen,2,0,self.Ctrl_Vars))
        for i in range(len(self.Menus)):
            self.Menus[i].hide = False
            self.Menus[i].active = True

    def init_text(self,size):
        self.text_color = ((255,255,255))
        self.font_size = size
        self.font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",self.font_size)
        self.font.set_bold(True)
        self.font_image = self.font.render(self.text,True,self.text_color,None)
        self.font_rect = self.font_image.get_rect()
        self.font_rect.centerx = self.Screen_rect.centerx
        self.font_rect.centery = 250

    def update_text(self):
        self.seed = self.Ctrl_Vars.seed
        self.text = "{}".format(self.seed)
        self.init_text(100)

    def draw(self):
        self.Screen.fill((0,0,0))
        self.update_text()
        self.Screen.blit(self.font_image,self.font_rect)
        for i in range(len(self.Menus)):
            self.Menus[i].draw()

#Envelope class that contrains all starft menue options ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""class background():
    def __init__(self,Screen):
        self.Screen = Screen
        self.image = pygame.image.load('Title/BK00.png')
        self.rect = self.image.get_rect()

    def draw(self):
        self.Screen.blit(self.image,self.rect)
    
class gonGrid():
    def __init__(self,Screen):
        self.Screen = Screen
        self.Screen_rect = self.Screen.get_rect()
        self.image = pygame.image.load('Title/GonGrid.png').convert()
        self.image.set_colorkey((255,0,255))
        self.rect = self.image.get_rect()
        self.rect.right = self.Screen_rect.right

    def draw(self):
        self.Screen.blit(self.image, self.rect)

class lUX_STRIKE():
    def __init__(self,Screen):
        self.Screen = Screen
        self.image = pygame.image.load('Title/LS21.png').convert()
        self.image.set_colorkey((255,0,255))

        self.rect = self.image.get_rect()

    def draw(self):
        self.Screen.blit(self.image, self.rect)"""

class still():
    #TODO: a still title screen image with no animations (placeholder) should be phased out with better graphics
    def __init__(self,Screen):
        self.Screen = Screen
        self.image = pygame.image.load('Title/Title Screen.png').convert()
        self.image.set_colorkey((255,0,255))

        self.rect = self.image.get_rect()
        self.Screen_rect = self.Screen.get_rect()
        self.rect.centerx = self.Screen_rect.centerx

    def draw(self):
        self.Screen.blit(self.image, self.rect)