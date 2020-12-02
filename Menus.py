import time,json
from Buttons import *
from Graphics import word_object,Animation
from Control_variables import Ctrl_Vars,Screen,ScreenRect

#switch command to instance a new active menu, TODO: turn into a dictionary key call
def menu_select(Window,Settings):
    if Ctrl_Vars.GameNav.Start_Screen:
        Active_Menu = Start_Envelope(Window,Settings)
        time.sleep(0.5)
    elif Ctrl_Vars.GameNav.Pause:
        Active_Menu = Pause_Envelope()
    elif Ctrl_Vars.GameNav.Game_Win:
        Active_Menu = Game_Win_Envelope()
        time.sleep(0.5)
    elif Ctrl_Vars.GameNav.Game_Over:
        Active_Menu = Game_Over_Envelope()
        time.sleep(0.5)
    elif Ctrl_Vars.main == False:
        if Ctrl_Vars.GameNav.Pause:
            Active_Menu = WC_Pause_Envelope()

    Ctrl_Vars.GameNav.menu_select = False
    #let garbage collector take care of un-used menus
    return Active_Menu

#Envelope class that contrains all start menu options and graphics vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
class Start_Envelope():
    def __init__(self,Window,Settings):
        self.Start_vars = Ctrl_Vars.Start_Vars
        self.Start_vars.load_menu = True
        self.Start_vars.Title = True
        self.Background = self.init_background()
        pygame.mixer.music.load('Music/6 Solutions per Side.mp3')
        pygame.mixer.music.play(-1)

        #Main options
        self.UI = []
        self.sub_menus = {
            'Title Screen': Title_Menu(Settings),
            'Volume': Sound_Menu(Settings), 
            'Jukebox': Jukebox_Menu(),
            'Display': Display_Menu(Window,Settings),
            'Seed': Num_Pad(),
            'Load World': World_load(Settings)
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
        return Animation(images,3,1)

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

#Contains three button folders will all options in it.
class Title_Menu():
    def __init__(self,settings):
        """These are folders, each contain a few more options within them"""
        self.Menus = [
            Settings([4,1],settings),
            Extras([4,2]),
            Play([4,3]),
            Hex_Button([9,0],"Quit",Exit)
        ]

    def draw(self):
        for i in range(len(self.Menus)):
            self.Menus[i].draw()

#allows the player to control the volume
class Sound_Menu():
    def __init__(self,Settings):
        self.Settings = Settings
        self.init_curtain()

        #Buttons
        self.Menus = []
        self.init_sliders()
        self.init_buttons()

    ##init *******************************************************************************
    def init_curtain(self):
        self.curtain = pygame.Surface((ScreenRect.right,ScreenRect.bottom))
        self.curtain.fill((0,0,0))
        self.curtain.set_alpha(120)

    def init_sliders(self):
        #Sliders
        spacing = 175
        x = ScreenRect.centerx - 120
        y = ScreenRect.top + 450
        self.slider_names = ["Master volume","Music volume","SFX volume","Voice volume"]
        self.sliders = []
        for i in range(len(self.slider_names)):
            name = self.slider_names[i]
            self.sliders.append(Slider_Bar(x,y + spacing * i,name))
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
            Hex_Button([9,0],"Title Screen",Start_Nav,"Title Screen"),
            Hex_Button([9,1],"Save",SaveSettings,self.Settings)
        ]
        self.Default = Hex_Button([9,2],"Default",Default,self.Settings)
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
        Screen.blit(self.curtain,(0,0))
        for i in range(len(self.Menus)):
            self.Menus[i].draw()

#allows the player to control the resolution or toggle fullscreen
class Display_Menu():
    def __init__(self,Window,Settings):
        self.init_curtain()     
        self.Menus = [
            Hex_Button([9,1],"Save",SaveSettings,(Settings)),
            Hex_Button([9,0],"Title Screen",Start_Nav,"Title Screen"),
            Hex_Button([4,2],"Full Screen",Fullscreen,Settings),
            Hex_Button([4,2],"Full Screen",Fullscreen,Settings),

            Hex_Button([3,1],"1920X1080",Resolution,(Window,Settings,[1920,1080])),
            Hex_Button([4,1],"1600X900",Resolution,(Window,Settings,[1600,900])),
            Hex_Button([5,1],"1280X720",Resolution,(Window,Settings,[1280,720])),
            Hex_Button([6,1],"640X480",Resolution,(Window,Settings,[640,480]))
        ]

    def init_curtain(self):
        self.curtain = pygame.Surface((ScreenRect.right,ScreenRect.bottom))
        self.curtain.fill((0,0,0))
        self.curtain.set_alpha(120)

    def draw(self):
        Screen.blit(self.curtain,(0,0))
        for i in range(len(self.Menus)):
            self.Menus[i].draw()

#just playes music. its not even good
class Jukebox_Menu():
    def __init__(self):
        self.Ctrl_Vars = Ctrl_Vars
        self.Menus = [
            Hex_Button([9,0],"Title Screen",Start_Nav,("Title Screen"))
        ]
        self.init_buttons()
        self.init_curtain()

    def init_buttons(self):
        count = 0
        for i in range(1,8):
            for j in range(0,5):
                button = Music_Button([i,j],count)
                self.Menus.append(button)
                count += 1

    def init_curtain(self):
        self.curtain = pygame.Surface((ScreenRect.right,ScreenRect.bottom))
        self.curtain.fill((0,0,0))
        self.curtain.set_alpha(120)

    def draw(self):
        for i in range(len(self.Menus)):
            self.Menus[i].draw()

#what you see when you hit pause
class Pause_Envelope():
    def __init__(self):
        self.text = "Paused"
        self.init_text(100)
        pygame.mixer.music.load('Music/Think.mp3')
        pygame.mixer.music.play(-1)

        #Main options
        """These are folders, each contain a few more options within them"""
        self.UI = [
            Quit_Folder([7,1]),
            Hex_Button([4,3],"Resume",Resume),
            Hex_Button([6,3],"Retry",Retry)
        ]

    def init_text(self,size):
        text_color = ((255,255,255))
        font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",size)
        font.set_bold(True)
        self.font_image = font.render(self.text,True,text_color,None)
        self.font_rect = self.font_image.get_rect()
        self.font_rect.centerx = ScreenRect.centerx
        self.font_rect.centery = 250

    def draw(self):
        Screen.fill((0,0,0))
        Screen.blit(self.font_image,self.font_rect)
        for item in self.UI:
            item.draw()

#what you see when you die
class Game_Over_Envelope():
    def __init__(self):
        self.text = "Death"
        self.init_text(100)
        pygame.mixer.music.load('Music/Beach Ball.mp3')
        pygame.mixer.music.play(-1)
        self.init_image()
        self.UI = [
            Quit_Folder([6,3]),
            Hex_Button([4,3],"Retry",Retry)
        ]

    def init_image(self):
        self.image = pygame.image.load('HUD/Death.png')
        self.image.set_colorkey((255,0,255))
        self.image_rect = self.image.get_rect()
        self.image_rect.bottom = ScreenRect.bottom - 100
        self.image_rect.centerx = ScreenRect.centerx

    def init_text(self,size):
        text_color = ((255,255,255))
        font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",size)
        font.set_bold(True)
        self.font_image = font.render(self.text,True,text_color,None)
        self.font_rect = self.font_image.get_rect()
        self.font_rect.centerx = ScreenRect.centerx
        self.font_rect.centery = 250

    def draw(self):
        Screen.fill((0,0,0))
        Screen.blit(self.image,self.image_rect)
        Screen.blit(self.font_image,self.font_rect)
        for item in self.UI:
            item.draw()

#what you see when you win
class Game_Win_Envelope():
    def __init__(self):
        self.UI = [
            Quit_Folder([7,1]),
            Hex_Button([4,3],"Random",Menu_Nav,("Random")),
            Hex_Button([6,3],"Retry",Retry),
            Hex_Button([4,1],"Save Seed",SaveSeed)
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
        self.image_rect.centerx = ScreenRect.centerx
        self.image_rect.top += 25

        self.frame_count = 0
        self.frames = 64

        self.buffer_frames = 30
        self.buffer_frame_count = 0
        self.buffer = True
        self.direction = 1

    def init_background(self):
        self.background = pygame.Surface((ScreenRect.width,ScreenRect.height))
        self.background.convert()
        self.background.fill((0,0,0))
        self.alpha = 0
        self.background.set_alpha(self.alpha)

    def fade_background(self):
        if self.alpha <= 255:
            self.alpha += 2
            self.background.set_alpha(self.alpha)
        Screen.blit(self.background,ScreenRect)

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
            Screen.blit(self.image,self.image_rect)
            self.frame_count += 1

    def draw(self):
        self.fade_background()
        self.animate()
        for item in self.UI:
            item.draw()

#used to type digits into CtrlVars for use in whatever
class Num_Pad():
    #Makes a number pad like on a phone for entering numbers. The functionality of this one can and should be generalized
    def __init__(self):
        self.init_curtain()

        seed = Ctrl_Vars.seed
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
        self.curtain_rect.centerx = ScreenRect.centerx
        self.curtain_rect.centery = 270

    def Menus_init(self):
        self.Menus = [
            Hex_Button([3,0],"Delete",Del),
            Key([4,0],0),
            Hex_Button([5,0],"Enter",Menu_Nav,("Custom")),
            Hex_Button([2,0],"Clear",Clear),
            Hex_Button([9,0],"Title Screen",Start_Nav,("Title Screen"))
        ]
        x = 3 #column
        y = 3 #row
        for i in range(9): #arranging main 9 numbers not including 0
            self.Menus.append(Key([x,y],i+1))
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
        self.font_rect.centerx = ScreenRect.centerx
        self.font_rect.centery = 270

    def update_text(self):
        seed = Ctrl_Vars.seed
        self.text = "{}".format(seed)
        self.init_text()
        self.num_left.text = "~" + str(18 - len(seed))
        self.num_left.init_text()

    def draw(self):
        Screen.blit(self.curtain,self.curtain_rect)
        self.update_text()
        Screen.blit(self.font_image,self.font_rect)
        self.num_left.draw((1550,285))
        for i in range(len(self.Menus)):
            self.Menus[i].draw()

#WORLD_LOADING: loads world from file: FIXME: 2 visual glitches, can use some poish as well
class World_load():
    def __init__(self,Settings):
        self.Settings = Settings
        self.World_list = world_list()
        self.Menus = [
            Hex_Button([9,0],"Title Screen",Start_Nav,("Title Screen")),
            Delete_World([8,2],"Delete",False,self.World_list),
            Load_World([7,2],"Load",False),
        ]
        self.World_list.buttons = [
            self.Menus[1],self.Menus[2]
        ]

    def navigation(self):
        Ctrl_Vars.GameNav.Menu_reset()
        Ctrl_Vars.GameNav.load_world = True
        Ctrl_Vars.GameNav.menu_select = False
        Ctrl_Vars.GameNav.Load = True

    def collision(self):
        if self.Menus[2].name != None:
            self.Off_Buttons()
        x,y = pygame.mouse.get_pos()
        x *= self.Settings.mouseX_scaling
        y *= self.Settings.mouseY_scaling
        value = self.World_list.collision(x,y)
        if value != False:
            self.Menus[1].name,self.Menus[2].name = value,value
            return

    def Off_Buttons(self):
        for i in range(len(self.World_list.buttons)):
            self.World_list.buttons[i].toggleOff()

    def draw(self):
        self.collision()
        for i in range(len(self.Menus)):
            self.Menus[i].draw()
        self.World_list.draw()

#containts a list of all worlds saved in saved world json file
class world_list():
    def __init__(self):
        self.init_boxes()
        self.buttons = []

    def init_boxes(self):
        self.world_names = []
        with open('Saved_Worlds/Saves.json','r') as File:
            data = json.load(File)
            count = 0
            for name in data:
                world_name = list_item(name,count)
                self.world_names.append(world_name)
                count += 1
        File.close()

    def On_Buttons(self):
        for i in range(len(self.buttons)):
            self.buttons[i].toggleOn()
    
    def collision(self,x,y):
        for item in self.world_names:
            value = item.collision(x,y)
            if value != False:
                self.On_Buttons()
                return value
        return False
        
    def draw(self):
        for item in self.world_names:
            item.draw()

#is a rectangular button that when clicked sets the CtrlVar key to the name of the world
class list_item():
    def __init__(self,name,order):
        self.name = name

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

        self.rect.centerx = ScreenRect.centerx
        self.rect.top = ScreenRect.top + (self.rect.height + 10) * order + 350

    def collision(self,x,y):
        if Ctrl_Vars.Left_MouseDown:
            if x >= self.rect.left and x <= self.rect.right:
                if y >= self.rect.top and y <= self.rect.bottom:
                    self.image = self.images[1]
                    Ctrl_Vars.Left_MouseDown = False
                    return self.name
            self.image = self.images[0]
        return False

    def draw(self):
        Screen.blit(self.image,self.rect)

"""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
~~~~~~~~~~~~~~~ WORLD CREATOR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
#pause screen at world creator
class WC_Pause_Envelope():
    def __init__(self):
        self.text = "Paused"
        self.init_text(100)
        self.UI = [
            Quit_Folder([7,1]),
            Hex_Button([4,3],"Resume",Resume)
        ]

        self.Curtain()

    def Curtain(self):
        self.curtain = pygame.Surface((ScreenRect.right,ScreenRect.bottom))
        self.curtain.fill((0,0,0))
        self.curtain.set_alpha(255)

    def init_text(self,size):
        text_color = ((255,255,255))
        font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",size)
        font.set_bold(True)
        self.font_image = font.render(self.text,True,text_color,None)
        self.font_rect = self.font_image.get_rect()
        self.font_rect.centerx = ScreenRect.centerx
        self.font_rect.centery = 250

    def draw(self):
        Screen.blit(self.curtain,ScreenRect)
        Screen.blit(self.font_image,self.font_rect)
        for i in range(len(self.UI)):
            self.UI[i].draw()

