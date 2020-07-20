import pygame
import Buttons
from text_reader import word_object
import time

def menu_select(Screen,Ctrl_Vars):
    if Ctrl_Vars.Start_Screen:
        Active_Menu = Start_Envelope(Screen,Ctrl_Vars)
        time.sleep(0.5)
    elif Ctrl_Vars.seed_menu:
        Active_Menu = Num_Pad(Screen,Ctrl_Vars)
        time.sleep(0.5)
    elif Ctrl_Vars.Pause:
        Active_Menu = Pause_Envelope(Screen,Ctrl_Vars)
    elif Ctrl_Vars.Game_Win:
        Active_Menu = Game_Win_Envelope(Screen,Ctrl_Vars)
        time.sleep(0.5)
    elif Ctrl_Vars.Game_Over:
        Active_Menu = Game_Over_Envelope(Screen,Ctrl_Vars)
        time.sleep(0.5)
    Ctrl_Vars.menu_select = False
    #let garbage collector take care of un-used menus
    return Active_Menu

#Envelope class that contrains all start menu options and graphics vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
class Start_Envelope():
    def __init__(self,Screen,Ctrl_Vars):
        """self.Background = background(Screen)
        self.GonGrid = gonGrid(Screen)
        self.LUX_STRIKE = lUX_STRIKE(Screen)"""
        self.Still = still(Screen)
        self.Menus = []
        #Main options
        pygame.mixer.music.load('Music/6 Solutions per Side.mp3')
        pygame.mixer.music.play(-1)
        """These are folders, each contain a few more options within them"""
        self.Menus.append(Buttons.Settings(Screen,1,1,Ctrl_Vars))
        self.Menus.append(Buttons.Extras(Screen,1,2,Ctrl_Vars))
        self.Menus.append(Buttons.Play(Screen,2,3,Ctrl_Vars))
        self.Menus.append(Buttons.Quit(Screen,9,0,Ctrl_Vars,True))

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
        pygame.mixer.music.load('Music/Think.mp3')
        pygame.mixer.music.play(-1)

        #Main options
        """These are folders, each contain a few more options within them"""
        self.Menus = []
        self.Menus.append(Buttons.Settings(Screen,1,1,Ctrl_Vars))
        self.Menus.append(Buttons.Quit_Folder(Screen,7,1,Ctrl_Vars))
        self.Menus.append(Buttons.Resume(Screen,4,3,Ctrl_Vars,True))
        self.Menus.append(Buttons.Retry(Screen,6,3,Ctrl_Vars,True))

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
        pygame.mixer.music.load('Music/Beach Ball.mp3')
        pygame.mixer.music.play(-1)

class Game_Win_Envelope():
    def __init__(self,Screen,Ctrl_Vars):
        self.Screen = Screen
        self.Screen_rect = self.Screen.get_rect()
        #Main options
        """These are folders, each contain a few more options within them"""
        self.Menus = []
        self.Menus.append(Buttons.Settings(Screen,1,1,Ctrl_Vars))
        self.Menus.append(Buttons.Quit_Folder(Screen,7,1,Ctrl_Vars))
        self.Menus.append(Buttons.Campaign(Screen,4,3,Ctrl_Vars,True))
        self.Menus.append(Buttons.Retry(Screen,6,3,Ctrl_Vars,True))
        self.Menus.append(Buttons.Save_seed(Screen,4,1,Ctrl_Vars,True))
        self.init_background()
        self.init_animation()

    def init_animation(self):
        self.images = []
        for i in range(8):
            image = pygame.image.load('HUD/Victory{}.png'.format(i)).convert()
            image.set_colorkey((165,235,255))
            self.images.append(image)
        self.image_rect = self.images[0].get_rect()
        self.image_rect.centerx = self.Screen_rect.centerx
        self.image_rect.top += 25

        self.frame_count = 0
        self.frames = 64

        self.buffer_frames = 50
        self.buffer_frame_count = 0
        self.buffer = True
        self.direction = 1

    def init_background(self):
        self.background = pygame.Surface((self.Screen_rect.width,self.Screen_rect.height))
        self.background.convert()
        self.background.fill((0,0,0))
        self.alpha = 0
        self.background.set_alpha(self.alpha)

    def fade_background(self):
        if self.alpha <= 255:
            self.alpha += 1
            self.background.set_alpha(self.alpha)
        self.Screen.blit(self.background,self.Screen_rect)

    def animate(self):
        if self.buffer: 
            if self.buffer_frame_count >= self.buffer_frames:
                self.buffer_frame_count = 0
                self.buffer = False
            self.buffer_frame_count += 1
        else:
            if self.frame_count + 1 >= self.frames:
                self.frame_count = 8
                self.direction *= -1

            self.image_rect.centery += self.direction
            self.image = self.images[self.frame_count//8]
            self.Screen.blit(self.image,self.image_rect)
            self.frame_count += 1

    def draw(self):
        self.fade_background()
        self.animate()
        for i in range(len(self.Menus)):
            self.Menus[i].draw()

    def reset(self):
        self.frame_count = 0
        self.frames = 64

        self.buffer_frames = 40
        self.buffer_frame_count = 0
        self.buffer = True
        self.direction = 1

class Num_Pad():
    #TODO: Makes a number pad like on a phone for entering numbers. The functionality of this one can and should be generalized
    def __init__(self,Screen,Ctrl_Vars):
        self.Screen = Screen
        self.Ctrl_Vars = Ctrl_Vars
        self.seed = self.Ctrl_Vars.seed
        self.Screen = Screen
        self.Screen_rect = Screen.get_rect()
        self.text = "{}".format(self.seed)
        self.num = "~" + str(18 - len(self.seed))
        self.num_left = word_object(self.num,['$R'])
        self.init_text()
        self.Menus_init()

    def Menus_init(self):
        self.Menus = []
        x = 3 #column
        y = 3 #row
        for i in range(9): #arranging main 9 numbers not including 0
            self.Menus.append(Buttons.Key(self.Screen,x,y,self.Ctrl_Vars,i+1,True))
            x += 1
            if x >= 6:
                y -= 1
                x = 3
        #arranging 0 and functional keys by hand
        self.Menus.append(Buttons.Del_Key(self.Screen,3,0,self.Ctrl_Vars,True)) 
        self.Menus.append(Buttons.Key(self.Screen,4,0,self.Ctrl_Vars,0,True)) 
        self.Menus.append(Buttons.Enter_Key(self.Screen,5,0,self.Ctrl_Vars,True)) 
        self.Menus.append(Buttons.Clear(self.Screen,2,0,self.Ctrl_Vars,True))
        self.Menus.append(Buttons.Return_start(self.Screen,9,0,self.Ctrl_Vars,True))

    def init_text(self):
        self.font_size = 100
        self.text_color = ((255,255,255))
        self.font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",self.font_size)
        self.font.set_bold(True)

        self.font_image = self.font.render(self.text,True,self.text_color,None)
        self.font_rect = self.font_image.get_rect()
        self.font_rect.centerx = self.Screen_rect.centerx
        self.font_rect.centery = 250

    def update_text(self):
        self.seed = self.Ctrl_Vars.seed
        self.text = "{}".format(self.seed)
        self.init_text()
        self.num_left.text = "~" + str(18 - len(self.seed))
        self.num_left.init_text()

    def draw(self):
        self.Screen.fill((0,0,0))
        self.update_text()
        self.Screen.blit(self.font_image,self.font_rect)
        self.num_left.draw(self.Screen,(1550,285))
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

""" TODO: #Loading Screen object"""
class load_world_screen():
    def __init__(self,Screen,N):
        #loading screen variables
        self.Screen = Screen
        self.screen_rect = self.Screen.get_rect()

        self.bar_size = (self.screen_rect.width * 9) // 10
        self.bar_left = self.screen_rect.width/20 + 2
        self.bar_top = self.screen_rect.bottom * (9/10) - 100
        self.bar = pygame.image.load('HUD/Bar.png')

        self.N = N
        self.i = float(1/N) * 100 * 2
        self.requirement = self.bar_size/self.N


        self.count = 0 #dynamic
        self.bar_frame = pygame.image.load('HUD/Load_Bar.png').convert()
        self.bar_frame.set_colorkey((255,0,255))
        self.Screen.blit(self.bar_frame,(0,self.bar_top-9))
        self.init_text()

        pygame.display.flip()

    def Update(self):
        self.count += self.i
        if self.count >= self.requirement:
            self.count = 0
            self.bar_left += 2
            if self.bar_left <= (1826):
                self.Screen.blit(self.bar,(self.bar_left,self.bar_top))
            pygame.display.flip()
        
    def init_text(self):
        text = "Loading..."
        font_size = 45
        text_color = ((255,255,255))
        font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",font_size)
        font.set_bold(True)

        font_image = font.render(text,True,text_color,None)
        font_rect = font_image.get_rect()
        surface = pygame.Surface((font_rect.right,font_rect.bottom))
        font_rect.right = self.screen_rect.right - 50
        font_rect.centery = self.bar_top - 40

        surface_rect = surface.get_rect()

        surface.fill((0, 0, 0))
        surface.blit(font_image, surface_rect)
        surface.set_alpha(105)

        self.Screen.blit(surface,font_rect)