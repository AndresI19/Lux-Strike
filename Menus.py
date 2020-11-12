import pygame
import Buttons
from Graphics import word_object
import time
from Tessellation import Animation
import json

def menu_select(Screen,Window,Ctrl_Vars,Settings):
    if Ctrl_Vars.Game_Menu_Vars.Start_Screen:
        Active_Menu = Start_Envelope(Screen,Window,Ctrl_Vars,Settings)
        time.sleep(0.5)
    elif Ctrl_Vars.Game_Menu_Vars.Pause:
        Active_Menu = Pause_Envelope(Screen,Ctrl_Vars)
    elif Ctrl_Vars.WC_Tools.Pause:
        Active_Menu = WC_Pause_Envelope(Screen,Ctrl_Vars)
    elif Ctrl_Vars.Game_Menu_Vars.Game_Win:
        Active_Menu = Game_Win_Envelope(Screen,Ctrl_Vars)
        time.sleep(0.5)
    elif Ctrl_Vars.Game_Menu_Vars.Game_Over:
        Active_Menu = Game_Over_Envelope(Screen,Ctrl_Vars)
        time.sleep(0.5)

    Ctrl_Vars.Game_Menu_Vars.menu_select = False
    #let garbage collector take care of un-used menus
    return Active_Menu

#Envelope class that contrains all start menu options and graphics vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
class Start_Envelope():
    def __init__(self,Screen,Window,Ctrl_Vars,Settings):
        self.Ctrl_Vars = Ctrl_Vars
        self.Screen = Screen
        self.Still = Background(Screen)
        self.Start_vars = Ctrl_Vars.Start_Vars
        self.Start_vars.load_menu = True
        self.Start_vars.Title = True
        pygame.mixer.music.load('Music/6 Solutions per Side.mp3')
        pygame.mixer.music.play(-1)

        #Main options
        self.Title_Screen = Title_Menu(Screen,Ctrl_Vars,Settings)
        self.Volume_Screen = Sound_Menu(Screen,Ctrl_Vars,Settings)
        self.Display_Screen = Display_Menu(Screen,Window,Ctrl_Vars,Settings)
        self.JukeBox_Screen = Jukebox_Menu(Screen,Ctrl_Vars)
        self.Num_Pad = Num_Pad(Screen,Ctrl_Vars)
        self.Load_pad = World_load(Settings,Screen,Ctrl_Vars)
        self.Sub_menu_select()

    def Sub_menu_select(self): #a menu select for everything in the start menu
        if self.Start_vars.load_menu:
            if self.Start_vars.Title:
                self.Active_Menu = self.Title_Screen
            elif self.Start_vars.Sound_Settings:
                self.Active_Menu = self.Volume_Screen
                pygame.mixer.music.load('Music/Bad KpR.mp3')
                pygame.mixer.music.play(-1)
            elif self.Start_vars.Num_pad:
                self.Active_Menu = self.Num_Pad
            elif self.Start_vars.Load_pad:
                self.Active_Menu = self.Load_pad
            elif self.Start_vars.Display_Settings:
                self.Active_Menu = self.Display_Screen
            elif self.Start_vars.Jukebox:
                self.Active_Menu = self.JukeBox_Screen
            time.sleep(0.5)
            self.Start_vars.load_menu = False
            self.Menus = self.Active_Menu.Menus
        
    def draw(self):
        self.Sub_menu_select()
        self.Still.draw()
        self.Active_Menu.draw()

class Title_Menu():
    def __init__(self,Screen,Ctrl_Vars,Settings):
        self.Menus = []
        """These are folders, each contain a few more options within them"""
        self.Menus.append(Buttons.Settings(Screen,[4,1],Ctrl_Vars,Settings)) #Settings
        self.Menus.append(Buttons.Extras(Screen,[4,2],Ctrl_Vars))
        self.Menus.append(Buttons.Play(Screen,[4,3],Ctrl_Vars))
        self.Menus.append(Buttons.Quit(Screen,[9,0],Ctrl_Vars,True)) 

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
        i = 175
        x = self.Screen_rect.centerx - 120
        y = self.Screen_rect.top + 450
        self.MasterV_Slider = Buttons.Slider_Bar(self.Screen,self.Ctrl_Vars,x,y,"Master Volume")
        self.MusicV_slider = Buttons.Slider_Bar(self.Screen,self.Ctrl_Vars,x,y + i,"Music Volume")
        self.SFX_slider = Buttons.Slider_Bar(self.Screen,self.Ctrl_Vars,x,y + i*2,"SFX Volume")
        self.Voice_slider = Buttons.Slider_Bar(self.Screen,self.Ctrl_Vars,x,y + i*3,"Voice Volume")
        self.Menus.append(self.MasterV_Slider)
        self.Menus.append(self.MusicV_slider)
        self.Menus.append(self.SFX_slider)
        self.Menus.append(self.Voice_slider)
        self.init_slider_values()

    def init_slider_values(self):
        self.MasterV_Slider.value = self.Settings.settings["Master volume"]
        self.MasterV_Slider.set_Knob()
        self.MusicV_slider.value = self.Settings.settings["Music volume"]
        self.MusicV_slider.set_Knob()
        self.SFX_slider.value = self.Settings.settings["SFX volume"]
        self.SFX_slider.set_Knob()
        self.Voice_slider.value = self.Settings.settings["Voice volume"]
        self.Voice_slider.set_Knob()

    def init_buttons(self):
        Back_Nav = Buttons.Start_Navigation(self.Screen,[9,0],self.Ctrl_Vars,"Title","Back")#back button
        Save = Buttons.Save_Settings(self.Screen,[9,1],self.Ctrl_Vars,self.Settings) #commit changes to file
        self.Default = Buttons.Default_Sound(self.Screen,[9,2],self.Ctrl_Vars,self.Settings)
        self.Menus.append(Back_Nav) 
        self.Menus.append(Save)
        self.Menus.append(self.Default) #return default

    ##Standard
    def update(self):
        if self.Default.value:
            self.init_slider_values()
            self.Default.value = False
        self.Settings.settings["Master volume"] = self.MasterV_Slider.value
        self.Settings.settings["Music volume"] = self.MusicV_slider.value
        self.Settings.settings["SFX volume"] = self.SFX_slider.value
        self.Settings.settings["Voice volume"] = self.Voice_slider.value
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
        self.Menus = []
        self.init_buttons()

    def init_curtain(self):
        Screen_rect = self.Screen.get_rect()
        self.curtain = pygame.Surface((Screen_rect.right,Screen_rect.bottom))
        self.curtain.fill((0,0,0))
        self.curtain.set_alpha(120)

    def init_buttons(self):
        #Buttons
        Save = Buttons.Save_Settings(self.Screen,[9,1],self.Ctrl_Vars,self.Settings) #commit
        Back_Nav = Buttons.Start_Navigation(self.Screen,[9,0],self.Ctrl_Vars,"Title","Back",True)
        Full_Screen = Buttons.Full_Screen(self.Screen,[4,2],self.Ctrl_Vars,self.Settings,True)
        R1920X1080 = Buttons.Resolution(self.Window,self.Screen,[3,1],self.Ctrl_Vars,self.Settings,[1920,1080],"1920X1080")
        R1600X900 = Buttons.Resolution(self.Window,self.Screen,[4,1],self.Ctrl_Vars,self.Settings,[1600,900],"1600X900")
        R1280X720 = Buttons.Resolution(self.Window,self.Screen,[5,1],self.Ctrl_Vars,self.Settings,[1280,720],"1280X720")
        R640X480 = Buttons.Resolution(self.Window,self.Screen,[6,1],self.Ctrl_Vars,self.Settings,[640,480],"640X480")

        self.Menus.append(Save)
        self.Menus.append(Back_Nav) #back button
        self.Menus.append(Full_Screen)
        self.Menus.append(R1920X1080)
        self.Menus.append(R1600X900)
        self.Menus.append(R1280X720)
        self.Menus.append(R640X480)

    def draw(self):
        self.Screen.blit(self.curtain,(0,0))
        for i in range(len(self.Menus)):
            self.Menus[i].draw()

class Jukebox_Menu():
    def __init__(self,Screen,Ctrl_Vars):
        self.Screen = Screen
        self.Ctrl_Vars = Ctrl_Vars
        self.Menus = []
        self.init_curtain()
        self.init_buttons()

    def init_buttons(self):
        count = 0
        for i in range(1,8):
            for j in range(0,5):
                button = Buttons.Music_Button(self.Screen,[i,j],count,self.Ctrl_Vars)
                self.Menus.append(button)
                count += 1     
        Back_Nav = Buttons.Start_Navigation(self.Screen,[9,0],self.Ctrl_Vars,"Title","Back")
        self.Menus.append(Back_Nav)

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
        self.Menus = []
        #self.Menus.append(Buttons.Settings(Screen,1,1,Ctrl_Vars))
        self.Menus.append(Buttons.Quit_Folder(Screen,[7,1],Ctrl_Vars))
        self.Menus.append(Buttons.Resume(Screen,[4,3],Ctrl_Vars))
        self.Menus.append(Buttons.Retry(Screen,[6,3],Ctrl_Vars))

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
        for i in range(len(self.Menus)):
            self.Menus[i].draw()

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
        self.init_menus()

    def init_menus(self):
        #Main options
        """These are folders, each contain a few more options within them"""
        self.Menus = []
        #self.Menus.append(Buttons.Settings(Screen,1,1,Ctrl_Vars))
        self.Menus.append(Buttons.Quit_Folder(self.Screen,[6,3],self.Ctrl_Vars))
        self.Menus.append(Buttons.Retry(self.Screen,[4,3],self.Ctrl_Vars))

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
        for i in range(len(self.Menus)):
            self.Menus[i].draw()

class Game_Win_Envelope():
    def __init__(self,Screen,Ctrl_Vars):
        self.Screen = Screen
        self.Screen_rect = self.Screen.get_rect()

        #Main options
        self.Menus = []

        self.Menus.append(Buttons.Quit_Folder(Screen,[7,1],Ctrl_Vars))
        Random = Buttons.Menu_Navagation(Screen,[4,3],Ctrl_Vars,"Random","Random")
        self.Menus.append(Random)
        self.Menus.append(Buttons.Retry(Screen,[6,3],Ctrl_Vars))
        self.Menus.append(Buttons.Save_seed(Screen,[4,1],Ctrl_Vars))
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
        for i in range(len(self.Menus)):
            self.Menus[i].draw()

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
        self.Menus = []
        x = 3 #column
        y = 3 #row
        for i in range(9): #arranging main 9 numbers not including 0
            self.Menus.append(Buttons.Key(self.Screen,[x,y],self.Ctrl_Vars,i+1))
            x += 1
            if x >= 6:
                y -= 1
                x = 3
        #arranging 0 and functional keys by hand
        self.Menus.append(Buttons.Del_Key(self.Screen,[3,0],self.Ctrl_Vars)) 
        self.Menus.append(Buttons.Key(self.Screen,[4,0],self.Ctrl_Vars,0)) 
        Enter = Buttons.Menu_Navagation(self.Screen,[5,0],self.Ctrl_Vars,"Custom","Enter")
        self.Menus.append(Enter)
        self.Menus.append(Buttons.Clear(self.Screen,[2,0],self.Ctrl_Vars))
        self.Menus.append(Buttons.Start_Navigation(self.Screen,[9,0],self.Ctrl_Vars,"Title","Back")) #back button

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

        self.Menus_init()
        self.World_list = world_list(Screen)

    def Menus_init(self):
        self.Menus = []
        #arranging 0 and functional keys by hand
        self.Menus.append(Buttons.Del_Key(self.Screen,[3,0],self.Ctrl_Vars)) 
        self.Menus.append(Buttons.Clear(self.Screen,[2,0],self.Ctrl_Vars))
        self.Menus.append(Buttons.Start_Navigation(self.Screen,[9,0],self.Ctrl_Vars,"Title","Back")) #back button

    def navigation(self):
        self.Ctrl_Vars.Game_Menu_Vars.Menu_reset()
        self.Ctrl_Vars.Game_Menu_Vars.load_world = True
        self.Ctrl_Vars.Game_Menu_Vars.menu_select = False
        self.Ctrl_Vars.Game_Menu_Vars.Load = True

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

class Background():
    def __init__(self,Screen):
        self.Screen = Screen
        images = []
        N = 36
        for i in range(N):
            image = pygame.image.load(
                'Title/Title{}.png'.format(i)
                ).convert()
            image.set_colorkey((255,0,255))
            images.append(image)
        for i in range(N):
            image = pygame.image.load(
                'Title/Title{}.png'.format(N-1)
                ).convert()
            image.set_colorkey((255,0,255))
            images.append(image)
        self.Animation = Animation(self.Screen,images,2)

    def draw(self):
        self.Animation.loop((0,0))

"""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
~~~~~~~~~~~~~~~ WORLD CREATOR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
class WC_Pause_Envelope():
    def __init__(self,Screen,Ctrl_Vars):
        self.Screen = Screen
        self.Screen_rect = self.Screen.get_rect()
        self.text = "Paused"
        self.init_text(100)

        #Main options
        """These are folders, each contain a few more options within them"""
        self.Menus = []
        self.Menus.append(Buttons.Quit_Folder(Screen,[7,1],Ctrl_Vars))
        self.Menus.append(Buttons.Resume(Screen,[4,3],Ctrl_Vars))

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
        for i in range(len(self.Menus)):
            self.Menus[i].draw()

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