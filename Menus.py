import pygame
import Buttons
from Graphics import word_object
import time
from Graphics import Animation
import json

def menu_select(Screen,Window,Ctrl_Vars,Settings):
    if Ctrl_Vars.GameNav.Start_Screen:
        Active_Menu = Start_Envelope(Screen,Window,Ctrl_Vars,Settings)
        time.sleep(0.5)
    elif Ctrl_Vars.GameNav.Pause:
        Active_Menu = Pause_Envelope(Screen,Ctrl_Vars)
    elif Ctrl_Vars.WC_Tools.Pause:
        Active_Menu = WC_Pause_Envelope(Screen,Ctrl_Vars)
    elif Ctrl_Vars.GameNav.Game_Win:
        Active_Menu = Game_Win_Envelope(Screen,Ctrl_Vars)
        time.sleep(0.5)
    elif Ctrl_Vars.GameNav.Game_Over:
        Active_Menu = Game_Over_Envelope(Screen,Ctrl_Vars)
        time.sleep(0.5)

    Ctrl_Vars.GameNav.menu_select = False
    #let garbage collector take care of un-used menus
    return Active_Menu

#Envelope class that contrains all start menu options and graphics vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
class Start_Envelope():
    def __init__(self,Screen,Window,Ctrl_Vars,Settings):
        self.Ctrl_Vars = Ctrl_Vars
        self.Screen = Screen
        self.Start_vars = Ctrl_Vars.Start_Vars
        self.Start_vars.load_menu = True
        self.Start_vars.Title = True
        self.Background = self.init_background()
        pygame.mixer.music.load('Music/6 Solutions per Side.mp3')
        pygame.mixer.music.play(-1)

        #Main options
        self.UI = []
        self.sub_menus = {
            'Title Screen': Title_Menu(Screen,Ctrl_Vars,Settings),
            'Volume': Sound_Menu(Screen,Ctrl_Vars,Settings), 
            'Jukebox': Jukebox_Menu(Screen,Ctrl_Vars),
            'Display': Display_Menu(Screen,Window,Ctrl_Vars,Settings),
            'Seed': Num_Pad(Screen,Ctrl_Vars),
            'Load World': World_load(Settings,Screen,Ctrl_Vars)
            }
        self.Sub_menu_select()

    def init_background(self):
        images = []
        N = 36
        for i in range(N):
            image = pygame.image.load(
                'Title/Title{}.png'.format(i)
                ).convert()
            image.set_colorkey((255,0,255))
            images.append(image)
        return Animation(self.Screen,images,3,1)

    def Sub_menu_select(self):
        if self.Start_vars.load_menu:
            self.Active_Menu = self.sub_menus[self.Start_vars.key]
            self.UI = self.Active_Menu.Menus
            if self.Start_vars.key == 'Volume':
                pygame.mixer.music.load('Music/Bad KpR.mp3')
                pygame.mixer.music.play(-1)
            time.sleep(0.5)
            self.Start_vars.load_menu = False

    def draw(self):
        self.Sub_menu_select()
        self.Background.clock()
        self.Background.draw((0,0))
        self.Active_Menu.draw()

class Title_Menu():
    def __init__(self,Screen,Ctrl_Vars,Settings):
        """These are folders, each contain a few more options within them"""
        self.Menus = [
            Buttons.Settings(Screen,[4,1],Ctrl_Vars,Settings),
            Buttons.Extras(Screen,[4,2],Ctrl_Vars),
            Buttons.Play(Screen,[4,3],Ctrl_Vars),
            Buttons.Quit(Screen,[9,0],Ctrl_Vars,True)
        ]

    def draw(self):
        for i in range(len(self.Menus)):
            self.Menus[i].draw()

class Sound_Menu():
    def __init__(self,Screen,Ctrl_Vars,Settings):
        self.Settings = Settings
        self.Screen = Screen
        self.Screen_rect = self.Screen.get_rect()
        self.Ctrl_Vars = Ctrl_Vars
        self.init_curtain()

        #Buttons
        self.Menus = []
        self.init_sliders()
        self.init_buttons()

    ##init *******************************************************************************
    def init_curtain(self):
        self.curtain = pygame.Surface((self.Screen_rect.right,self.Screen_rect.bottom))
        self.curtain.fill((0,0,0))
        self.curtain.set_alpha(120)

    def init_sliders(self):
        #Sliders
        spacing = 175
        x = self.Screen_rect.centerx - 120
        y = self.Screen_rect.top + 450
        self.slider_names = ["Master volume","Music volume","SFX volume","Voice volume"]
        self.sliders = []
        for i in range(len(self.slider_names)):
            name = self.slider_names[i]
            self.sliders.append(
                Buttons.Slider_Bar(
                    self.Screen,self.Ctrl_Vars,x,y + spacing * i,name
                    )
            )
        self.init_slider_values()
        self.Menus.extend(self.sliders)

    def init_slider_values(self):
        count = 0
        for slider in self.sliders:
            slider.value = self.Settings.settings[self.slider_names[count]]
            slider.set_Knob()
            count += 1

    def init_buttons(self):
        buttons = [
            Buttons.Start_Navigation(self.Screen,[9,0],self.Ctrl_Vars,"Title Screen"),
            Buttons.Save_Settings(self.Screen,[9,1],self.Ctrl_Vars,self.Settings)
        ]
        self.Default = Buttons.Default_Sound(self.Screen,[9,2],self.Ctrl_Vars,self.Settings)
        buttons.append(self.Default)
        self.Menus.extend(buttons)

    ##Standard
    def update(self):
        if self.Default.value:
            self.init_slider_values()
            self.Default.value = False
        count = 0
        for slider in self.sliders:
            key = self.slider_names[count]
            self.Settings.settings[key] = slider.value
            count += 1
        pygame.mixer.music.set_volume(self.Settings.settings["Master volume"]/100)

    def draw(self):
        self.update()
        self.Screen.blit(self.curtain,(0,0))
        for i in range(len(self.Menus)):
            self.Menus[i].draw()

class Display_Menu():
    def __init__(self,Screen,Window,Ctrl_Vars,Settings):
        self.Settings = Settings
        self.Screen = Screen
        self.Ctrl_Vars = Ctrl_Vars
        self.Window = Window
        self.init_curtain()
        self.Menus = [
            Buttons.Save_Settings(self.Screen,[9,1],self.Ctrl_Vars,self.Settings),
            Buttons.Start_Navigation(self.Screen,[9,0],self.Ctrl_Vars,"Title Screen",True),
            Buttons.Full_Screen(self.Screen,[4,2],self.Ctrl_Vars,self.Settings,True),
            Buttons.Resolution(self.Window,self.Screen,[3,1],self.Ctrl_Vars,self.Settings,[1920,1080],"1920X1080"),
            Buttons.Resolution(self.Window,self.Screen,[4,1],self.Ctrl_Vars,self.Settings,[1600,900],"1600X900"),
            Buttons.Resolution(self.Window,self.Screen,[5,1],self.Ctrl_Vars,self.Settings,[1280,720],"1280X720"),
            Buttons.Resolution(self.Window,self.Screen,[6,1],self.Ctrl_Vars,self.Settings,[640,480],"640X480")
        ]

    def init_curtain(self):
        Screen_rect = self.Screen.get_rect()
        self.curtain = pygame.Surface((Screen_rect.right,Screen_rect.bottom))
        self.curtain.fill((0,0,0))
        self.curtain.set_alpha(120)

    def draw(self):
        self.Screen.blit(self.curtain,(0,0))
        for i in range(len(self.Menus)):
            self.Menus[i].draw()

class Jukebox_Menu():
    def __init__(self,Screen,Ctrl_Vars):
        self.Screen = Screen
        self.Ctrl_Vars = Ctrl_Vars
        self.Menus = [
            Buttons.Start_Navigation(self.Screen,[9,0],self.Ctrl_Vars,"Title Screen")
        ]
        self.init_buttons()
        self.init_curtain()

    def init_buttons(self):
        count = 0
        for i in range(1,8):
            for j in range(0,5):
                button = Buttons.Music_Button(self.Screen,[i,j],count,self.Ctrl_Vars)
                self.Menus.append(button)
                count += 1

    def init_curtain(self):
        Screen_rect = self.Screen.get_rect()
        self.curtain = pygame.Surface((Screen_rect.right,Screen_rect.bottom))
        self.curtain.fill((0,0,0))
        self.curtain.set_alpha(120)

    def draw(self):
        for i in range(len(self.Menus)):
            self.Menus[i].draw()

"""TODO: temporary use of a the pause screen as a mother class, make all independent"""
class Pause_Envelope():
    def __init__(self,Screen,Ctrl_Vars):
        self.Screen = Screen
        self.Screen_rect = self.Screen.get_rect()
        self.text = "Paused"
        self.init_text(100)
        pygame.mixer.music.load('Music/Think.mp3')
        pygame.mixer.music.play(-1)

        #Main options
        """These are folders, each contain a few more options within them"""
        self.UI = [
            Buttons.Quit_Folder(Screen,[7,1],Ctrl_Vars),
            Buttons.Resume(Screen,[4,3],Ctrl_Vars),
            Buttons.Retry(Screen,[6,3],Ctrl_Vars)
        ]

    def init_text(self,size):
        text_color = ((255,255,255))
        font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",size)
        font.set_bold(True)
        self.font_image = font.render(self.text,True,text_color,None)
        self.font_rect = self.font_image.get_rect()
        self.font_rect.centerx = self.Screen_rect.centerx
        self.font_rect.centery = 250

    def draw(self):
        self.Screen.fill((0,0,0))
        self.Screen.blit(self.font_image,self.font_rect)
        for item in self.UI:
            item.draw()

class Game_Over_Envelope(Pause_Envelope):
    def __init__(self,Screen,Ctrl_Vars):
        self.Screen = Screen
        self.Ctrl_Vars = Ctrl_Vars
        self.Screen_rect = self.Screen.get_rect()
        self.text = "Death"
        self.init_text(100)
        pygame.mixer.music.load('Music/Beach Ball.mp3')
        pygame.mixer.music.play(-1)
        self.init_image()
        self.UI = [
            Buttons.Quit_Folder(self.Screen,[6,3],self.Ctrl_Vars),
            Buttons.Retry(self.Screen,[4,3],self.Ctrl_Vars)
        ]

    def init_image(self):
        self.image = pygame.image.load('HUD/Death.png')
        self.image.set_colorkey((255,0,255))
        self.image_rect = self.image.get_rect()
        self.image_rect.bottom = self.Screen_rect.bottom - 100
        self.image_rect.centerx = self.Screen_rect.centerx

    def init_text(self,size):
        text_color = ((255,255,255))
        font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",size)
        font.set_bold(True)
        self.font_image = font.render(self.text,True,text_color,None)
        self.font_rect = self.font_image.get_rect()
        self.font_rect.centerx = self.Screen_rect.centerx
        self.font_rect.centery = 250

    def draw(self):
        self.Screen.fill((0,0,0))
        self.Screen.blit(self.image,self.image_rect)
        self.Screen.blit(self.font_image,self.font_rect)
        for item in self.UI:
            item.draw()

class Game_Win_Envelope():
    def __init__(self,Screen,Ctrl_Vars):
        self.Screen = Screen
        self.Screen_rect = self.Screen.get_rect()
        self.UI = [
            Buttons.Quit_Folder(Screen,[7,1],Ctrl_Vars),
            Buttons.Menu_Navagation(Screen,[4,3],Ctrl_Vars,"Random","Random"),
            Buttons.Retry(Screen,[6,3],Ctrl_Vars),
            Buttons.Save_seed(Screen,[4,1],Ctrl_Vars)
        ]
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

        self.buffer_frames = 30
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
            self.alpha += 2
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
        for item in self.UI:
            item.draw()

class Num_Pad():
    #Makes a number pad like on a phone for entering numbers. The functionality of this one can and should be generalized
    def __init__(self,Screen,Ctrl_Vars):
        self.Screen = Screen
        self.Ctrl_Vars = Ctrl_Vars
        self.Screen = Screen
        self.Screen_rect = Screen.get_rect()
        self.init_curtain()

        seed = self.Ctrl_Vars.seed
        self.text = "{}".format(seed)
        num = "~" + str(18 - len(seed))
        self.num_left = word_object(num,['$R'])
        self.init_text()
        self.Menus_init()

    def init_curtain(self):
        self.curtain = pygame.Surface((1350,125))
        self.curtain.fill((0,0,0))
        self.curtain.set_alpha(185)
        self.curtain_rect = self.curtain.get_rect()
        self.curtain_rect.centerx = self.Screen_rect.centerx
        self.curtain_rect.centery = 270

    def Menus_init(self):
        self.Menus = [
            Buttons.Del_Key(self.Screen,[3,0],self.Ctrl_Vars),
            Buttons.Key(self.Screen,[4,0],self.Ctrl_Vars,0),
            Buttons.Menu_Navagation(self.Screen,[5,0],self.Ctrl_Vars,"Custom","Enter"),
            Buttons.Clear(self.Screen,[2,0],self.Ctrl_Vars),
            Buttons.Start_Navigation(self.Screen,[9,0],self.Ctrl_Vars,"Title","Back")
        ]
        x = 3 #column
        y = 3 #row
        for i in range(9): #arranging main 9 numbers not including 0
            self.Menus.append(Buttons.Key(self.Screen,[x,y],self.Ctrl_Vars,i+1))
            x += 1
            if x >= 6:
                y -= 1
                x = 3

    def init_text(self):
        font_size = 100
        text_color = ((255,255,255))
        font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",font_size)
        font.set_bold(True)

        self.font_image = font.render(self.text,True,text_color,None)
        self.font_rect = self.font_image.get_rect()
        self.font_rect.centerx = self.Screen_rect.centerx
        self.font_rect.centery = 270

    def update_text(self):
        seed = self.Ctrl_Vars.seed
        self.text = "{}".format(seed)
        self.init_text()
        self.num_left.text = "~" + str(18 - len(seed))
        self.num_left.init_text()

    def draw(self):
        self.Screen.blit(self.curtain,self.curtain_rect)
        self.update_text()
        self.Screen.blit(self.font_image,self.font_rect)
        self.num_left.draw(self.Screen,(1550,285))
        for i in range(len(self.Menus)):
            self.Menus[i].draw()

#TODO: WORLD_LOADING
class World_load():
    def __init__(self,Settings,Screen,Ctrl_Vars):
        self.Screen = Screen
        self.Ctrl_Vars = Ctrl_Vars
        self.Screen = Screen
        self.Settings = Settings
        self.Screen_rect = Screen.get_rect()

        self.Menus = [
            Buttons.Start_Navigation(self.Screen,[9,0],self.Ctrl_Vars,"Title Screen")
        ]
        self.World_list = world_list(Screen)

    def navigation(self):
        self.Ctrl_Vars.GameNav.Menu_reset()
        self.Ctrl_Vars.GameNav.load_world = True
        self.Ctrl_Vars.GameNav.menu_select = False
        self.Ctrl_Vars.GameNav.Load = True

    def collision(self):
        x,y = pygame.mouse.get_pos()
        x *= self.Settings.mouseX_scaling
        y *= self.Settings.mouseY_scaling
        value = self.World_list.collision(x,y)
        if value != False:
            if self.Ctrl_Vars.Left_MouseDown:
                self.Ctrl_Vars.seed = value
                self.navigation()

    def draw(self):
        self.collision()
        for i in range(len(self.Menus)):
            self.Menus[i].draw()
        self.World_list.draw()

"""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
~~~~~~~~~~~~~~~ WORLD CREATOR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
class WC_Pause_Envelope():
    def __init__(self,Screen,Ctrl_Vars):
        self.Screen = Screen
        self.Screen_rect = self.Screen.get_rect()
        self.text = "Paused"
        self.init_text(100)
        self.UI = [
            Buttons.Quit_Folder(Screen,[7,1],Ctrl_Vars),
            Buttons.Resume(Screen,[4,3],Ctrl_Vars)
        ]

        self.Curtain()

    def Curtain(self):
        self.curtain = pygame.Surface((self.Screen_rect.right,self.Screen_rect.bottom))
        self.curtain.fill((0,0,0))
        self.curtain.set_alpha(255)

    def init_text(self,size):
        text_color = ((255,255,255))
        font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",size)
        font.set_bold(True)
        self.font_image = font.render(self.text,True,text_color,None)
        self.font_rect = self.font_image.get_rect()
        self.font_rect.centerx = self.Screen_rect.centerx
        self.font_rect.centery = 250

    def draw(self):
        self.Screen.blit(self.curtain,self.Screen_rect)
        self.Screen.blit(self.font_image,self.font_rect)
        for i in range(len(self.UI)):
            self.UI[i].draw()

class world_list():
    def __init__(self,Screen):
        self.world_names = []
        with open('Saved_Worlds/Saves.json','r') as File:
            data = json.load(File)
            count = 0
            for name in data:
                world_name = list_item(Screen,name,count)
                self.world_names.append(world_name)
                count += 1
        File.close()

    def collision(self,x,y):
        for item in self.world_names:
            value = item.collision(x,y)
            if value != False:
                return value
        return False
        
    def draw(self):
        for item in self.world_names:
            item.draw()

class list_item():
    def __init__(self,Screen,name,order):
        self.name = name
        self.Screen = Screen

        font_size = 65
        font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",font_size)
        font.set_bold(True)
        text = font.render(self.name,True,(0,0,0),None)
        text_rect = text.get_rect()

        self.images = [pygame.image.load('HUD/WorldName0.png'),pygame.image.load('HUD/WorldName1.png')]
        self.rect = self.images[0].get_rect()

        text_rect.centerx = self.rect.centerx
        text_rect.centery = self.rect.centery

        self.images[0].blit(text,text_rect)
        text = font.render(self.name,True,(255,255,255),None)
        self.images[1].blit(text,text_rect)
        self.image = self.images[0]

        Screen_rect = self.Screen.get_rect()
        self.rect.centerx = Screen_rect.centerx
        self.rect.top = Screen_rect.top + (self.rect.height + 10) * order + 350

    def collision(self,x,y):
        if x >= self.rect.left and x <= self.rect.right:
            if y >= self.rect.top and y <= self.rect.bottom:
                self.image = self.images[1]
                return self.name
        self.image = self.images[0]
        return False

    def draw(self):
        self.Screen.blit(self.image,self.rect)