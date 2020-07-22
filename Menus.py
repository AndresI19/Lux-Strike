import pygame
import Buttons
from text_reader import word_object
import time

def menu_select(Screen,Ctrl_Vars,Settings):
    if Ctrl_Vars.Start_Screen:
        Active_Menu = Start_Envelope(Screen,Ctrl_Vars,Settings)
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
    def __init__(self,Screen,Ctrl_Vars,Settings):
        self.Ctrl_Vars = Ctrl_Vars
        self.Screen = Screen
        #Main options
        self.Still = Background(Screen)
        self.Start_vars = Internal_vars()
        pygame.mixer.music.load('Music/6 Solutions per Side.mp3')
        pygame.mixer.music.play(-1)

        self.Title_Screen = Title_Screen(Screen,Ctrl_Vars,self.Start_vars)
        self.Volume_Screen = Settings_Envelope(Screen,Ctrl_Vars,Settings,self.Start_vars)
        self.Num_Pad = Num_Pad(Screen,Ctrl_Vars,self.Start_vars)
        self.Sub_menu_select()

    def Sub_menu_select(self):
        if self.Start_vars.load_menu:
            if self.Start_vars.Title:
                self.Active_Menu = self.Title_Screen
                time.sleep(0.5)
            elif self.Start_vars.Settings:
                self.Active_Menu = self.Volume_Screen
                time.sleep(0.5)
            elif self.Start_vars.Num_pad:
                self.Active_Menu = self.Num_Pad
                time.sleep(0.5)          
            self.Start_vars.load_menu = False
            self.Menus = self.Active_Menu.Menus
        
    def draw(self):
        self.Sub_menu_select()
        self.Still.draw()
        self.Active_Menu.draw()

class Title_Screen():
    def __init__(self,Screen,Ctrl_Vars,Start_vars):
        self.Menus = []
        """These are folders, each contain a few more options within them"""
        self.Menus.append(Buttons.Settings(Screen,4,1,Ctrl_Vars,Start_vars)) #Settings
        self.Menus.append(Buttons.Extras(Screen,4,2,Ctrl_Vars))
        self.Menus.append(Buttons.Play(Screen,4,3,Ctrl_Vars,Start_vars))
        self.Menus.append(Buttons.Quit(Screen,9,0,Ctrl_Vars,True))

    def draw(self):
        for i in range(len(self.Menus)):
            self.Menus[i].draw()

class Settings_Envelope():
    def __init__(self,Screen,Ctrl_Vars,Settings,Start_Vars):
        self.Settings = Settings
        self.Screen = Screen
        Screen_rect = Screen.get_rect()
        self.curtain = pygame.Surface((Screen_rect.right,Screen_rect.bottom))
        self.curtain.fill((0,0,0))
        self.curtain.set_alpha(120)
        x = Screen_rect.centerx - 120
        y = Screen_rect.top + 450
        self.Menus = []
        #Buttons
        self.Menus.append(Buttons.Back(Screen,9,0,Ctrl_Vars,Start_Vars,True)) #back button
        self.Menus.append(Buttons.Save_Settings(Screen,9,1,Ctrl_Vars,Settings,True)) #commit
        self.Default = Buttons.Default(Screen,9,2,Ctrl_Vars,Settings,True)
        self.Menus.append(self.Default) #return default
        #Sliders
        i = 175
        self.MasterV_Slider = Buttons.Slider_Bar(Screen,Ctrl_Vars,x,y,"Master Volume")
        self.MusicV_slider = Buttons.Slider_Bar(Screen,Ctrl_Vars,x,y + i,"Music Volume")
        self.SFX_slider = Buttons.Slider_Bar(Screen,Ctrl_Vars,x,y + i*2,"SFX Volume")
        self.Voice_slider = Buttons.Slider_Bar(Screen,Ctrl_Vars,x,y + i*3,"Voice Volume")
        self.Menus.append(self.MasterV_Slider)
        self.Menus.append(self.MusicV_slider)
        self.Menus.append(self.SFX_slider)
        self.Menus.append(self.Voice_slider)
        self.init_slider_values()

    def init_slider_values(self):
        self.MasterV_Slider.value = self.Settings.master_volume
        self.MasterV_Slider.set_Knob()
        self.MusicV_slider.value = self.Settings.music_volume
        self.MusicV_slider.set_Knob()
        self.SFX_slider.value = self.Settings.SFX_volume
        self.SFX_slider.set_Knob()
        self.Voice_slider.value = self.Settings.voice_volume
        self.Voice_slider.set_Knob()

    def update(self):
        if self.Default.value:
            self.Settings.set_default_settings()
            self.init_slider_values()
        self.Settings.master_volume = self.MasterV_Slider.value
        self.Settings.music_volume = self.MusicV_slider.value
        self.Settings.SFX_volume = self.SFX_slider.value
        self.Settings.voice_volume = self.Voice_slider.value
        pygame.mixer.music.set_volume(self.Settings.master_volume/100)

    def draw(self):
        self.update()
        self.Screen.blit(self.curtain,(0,0))
        for i in range(len(self.Menus)):
            self.Menus[i].draw()

"""TODO: temporary use of a the pause screen as a mother class"""
class Pause_Envelope():
    def __init__(self,Screen,Ctrl_Vars):
        self.Screen = Screen
        self.Screen_rect = self.Screen.get_rect()
        pygame.mixer.music.load('Music/Think.mp3')
        pygame.mixer.music.play(-1)

        #Main options
        """These are folders, each contain a few more options within them"""
        self.Menus = []
        #self.Menus.append(Buttons.Settings(Screen,1,1,Ctrl_Vars))
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

class Game_Over_Envelope(Pause_Envelope):
    def __init__(self,Screen,Ctrl_Vars):
        Pause_Envelope.__init__(self,Screen,Ctrl_Vars)
        self.text = "Death"
        self.init_text(100)
        pygame.mixer.music.load('Music/Approach.mp3')
        pygame.mixer.music.play(-1)

class Game_Win_Envelope():
    def __init__(self,Screen,Ctrl_Vars):
        self.Screen = Screen
        self.Screen_rect = self.Screen.get_rect()
        #Main options
        """These are folders, each contain a few more options within them"""
        self.Menus = []
        #self.Menus.append(Buttons.Settings(Screen,1,1,Ctrl_Vars))
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
    def __init__(self,Screen,Ctrl_Vars,Start_Vars):
        self.Screen = Screen
        self.Ctrl_Vars = Ctrl_Vars
        self.Start_Vars = Start_Vars
        self.seed = self.Ctrl_Vars.seed
        self.Screen = Screen
        self.Screen_rect = Screen.get_rect()
        self.text = "{}".format(self.seed)
        self.num = "~" + str(18 - len(self.seed))
        self.num_left = word_object(self.num,['$R'])
        self.init_text()
        self.Menus_init()
        #Screen_rect = Screen.get_rect()
        self.curtain = pygame.Surface((1350,125))
        self.curtain.fill((0,0,0))
        self.curtain.set_alpha(185)
        self.curtain_rect = self.curtain.get_rect()
        self.curtain_rect.centerx = self.Screen_rect.centerx
        self.curtain_rect.centery = 270

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
        self.Menus.append(Buttons.Back(self.Screen,9,0,self.Ctrl_Vars,self.Start_Vars,True)) #back button

    def init_text(self):
        self.font_size = 100
        self.text_color = ((255,255,255))
        self.font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",self.font_size)
        self.font.set_bold(True)

        self.font_image = self.font.render(self.text,True,self.text_color,None)
        self.font_rect = self.font_image.get_rect()
        self.font_rect.centerx = self.Screen_rect.centerx
        self.font_rect.centery = 270

    def update_text(self):
        self.seed = self.Ctrl_Vars.seed
        self.text = "{}".format(self.seed)
        self.init_text()
        self.num_left.text = "~" + str(18 - len(self.seed))
        self.num_left.init_text()

    def draw(self):
        self.Screen.blit(self.curtain,self.curtain_rect)
        self.update_text()
        self.Screen.blit(self.font_image,self.font_rect)
        self.num_left.draw(self.Screen,(1550,285))
        for i in range(len(self.Menus)):
            self.Menus[i].draw()

class Background():
    def __init__(self,Screen):
        self.Screen = Screen

        self.images = []
        self.init_images()
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.Screen_rect = self.Screen.get_rect()
        self.rect.centerx = self.Screen_rect.centerx

    def init_images(self):
        N = 36
        for i in range(N):
            image = pygame.image.load(
                'Title/Title{}.png'.format(i)
                ).convert()
            image.set_colorkey((255,0,255))
            self.images.append(image)
        for i in range(N):
            image = pygame.image.load(
                'Title/Title{}.png'.format(N-1)
                ).convert()
            image.set_colorkey((255,0,255))
            self.images.append(image)

        self.rate = 4
        self.Frames = N * 2 * self.rate
        self.frame = 0

    def draw(self):
        self.clock()
        self.Screen.blit(self.image, self.rect)

    def clock(self):
        if self.frame + 1 >= self.Frames:
            self.frame = 0
        else:
            self.frame += 1
        self.image = self.images[self.frame//self.rate]

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

class Internal_vars():
    def __init__(self):
        self.load_menu = True
        self.Title = True
        self.Settings = False
        self.Num_pad = False