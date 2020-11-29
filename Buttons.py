import pygame,sys
import pygame.font
from math import sqrt
from time import sleep
from Save import delete_map
from Control_variables import Ctrl_Vars,Screen,ScreenRect

"""Button Functions %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
def Default(self):
    self.value = True
    return True

def OpenFolder(self):
    #the functionality of the button is to open the sub menu
    self.open = True
    """once the folder has fully extended allow functionality"""
    if self.frame_count >= self.frames:
        self.frame_count = self.frames
        for i in range(len(self.Buttons)):
            self.Buttons[i].active = True #allow functionality
    else:
        self.frame_count += 1
        self.translate_group(self.pixel_increment)

def Start_Nav(self):
    #activates campaign mode
    Ctrl_Vars.Start_Vars.Menu_reset()
    Ctrl_Vars.Start_Vars.Set_Menu(self.properties)

def Menu_Nav(self):
    key = self.properties
    Ctrl_Vars.Nav_GameTypes(key)

def Del(self):
    #activates campaign mode
    Ctrl_Vars.seed = Ctrl_Vars.seed[:-1]

def Clear(self):
    Ctrl_Vars.seed = ""

def SaveSeed(self):
    File = 'Saved_Worlds/Favorite Seeds.txt'
    File = open(File,"a")
    File.writelines(Ctrl_Vars.seed + "\n")
    File.close()

def SaveSettings(self):
    self.properties.Save_settings()
    print("Saved")

def SaveVolume(self):
    self.properties.default_volume()
    self.value = True

def Fullscreen(self):
    self.properties.toggle_fullscreen()

def Resume(self):
    Ctrl_Vars.GameNav.Game_active = True
    Ctrl_Vars.GameNav.Pause = False
    Ctrl_Vars.WC_Tools.Pause = False

def Retry(self):
    Ctrl_Vars.GameNav.Pause = False
    Ctrl_Vars.GameNav.Game_Over = False
    Ctrl_Vars.GameNav.Game_Win = False

    Ctrl_Vars.GameNav.load_world = True
    Ctrl_Vars.GameNav.restart_world = True

def Exit(self):
    sleep(0.5)
    sys.exit(0)

def DeleteWorld(self):
    delete_map(self.name)
    self.LIST.init_boxes()

def LoadWorld(self):
    Ctrl_Vars.GameNav.Menu_reset()
    Ctrl_Vars.GameNav.load_world = True
    Ctrl_Vars.GameNav.menu_select = False
    Ctrl_Vars.GameNav.Load = True
    Ctrl_Vars.seed = self.name
    Ctrl_Vars.Start_Vars.key = 'Title Screen'

def Resolution(self):
    Window,Settings,value = self.properties
    if Settings.settings['Resolution'] != value:
        Settings.settings['Full Screen'] = False
        Settings.settings['Resolution'] = value
        Settings.init_Screen()
        Window = Settings.create_window()

def key(self):
    if len(Ctrl_Vars.seed) < 18:
        Ctrl_Vars.seed += "{}".format(self.value)

"""Mother class Buttons%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
#Simple Button (Mother) vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
class Hex_Button():
    def __init__(self,Coords,text = "N/A",function = Default,properties = None,active = True):
        self.Coords = Coords
        self.text = text
        self.sound = pygame.mixer.Sound("SFX/Button_press.wav")

        self.functionality = function
        self.properties = properties

        self.images = [pygame.image.load('Title/MenuGonOnS.png').convert(),
            pygame.image.load('Title/MenuGonS.png').convert()]
        self.rect = self.images[0].get_rect()

        #Customize
        self.position() #set position
        self.init_text() #set text

        #state of activity
        self.On = False
        self.value = False
        if active:
            self.toggleOff()
        else:
            self.toggleOn()

    def reset(self):
        #default reset is to turn off shine
        self.Value = False
        self.On = False

    def press(self):
        #General functionality is just to shine and turn off
        self.On = True
        if Ctrl_Vars.Left_click:
            pygame.mixer.Sound.play(self.sound)
            Ctrl_Vars.Left_click = False
            Ctrl_Vars.Left_MouseDown = False
            self.functionality(self) #Specific functiality: passed in args

    def toggleOn(self):
        self.hide = True
        self.active = False

    def toggleOff(self):
        self.hide = False
        self.active = True

    def position(self):
        #sets position of object based on where it is stored on an array grid
        x,y = self.Coords
        
        #geometric properties
        self.height = self.rect.bottom
        width = self.rect.right
        offset = width/2

        self.left = x * (width)
        self.right = width + self.left
        self.bottom = ScreenRect.bottom - (y * (self.height * (3/4)))
        self.top = self.bottom - self.height
        if y%2 == 0: #stagger rows
            self.left += offset
            self.right += offset
        self.center_x = offset + self.left

        self.rect.left = self.left
        self.rect.bottom = self.bottom

    def init_text(self):
        def size_text(size):
            font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",size)
            font.set_bold(True)
            words = self.text.split()
            largest_word = words[0]
            if len(words) > 1:
                for word in words:
                    if len(word) >= len(largest_word):
                        largest_word = word
            TstFntImg = font.render(largest_word,True,text_color,None)
            rect = TstFntImg.get_rect()
            while rect.width > self.height - 40 or size <= 3:
                size -= 1
                font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",size)
                font.set_bold(True)
                TstFntImg = font.render(largest_word,True,text_color,None)
                rect = TstFntImg.get_rect()
            self.text_size = (rect.width,rect.height)
            return font
            
        def Make_image():
            words = self.text.split()
            image = font.render(words[0],False,text_color,None)
            if len(words) > 1:
                surface_rect = (self.text_size[0],self.text_size[1]*len(words))
                surface = pygame.Surface(surface_rect)
                surface.fill((255,255,255))

                rect = image.get_rect()
                rect.centerx = surface_rect[0]//2
                surface.blit(image,rect)
                for i in range(len(words)-1):
                    next_image = font.render(words[i+1],False,text_color,None)
                    next_rect = next_image.get_rect()
                    next_rect.top = rect.bottom
                    next_rect.centerx = surface_rect[0]//2
                    surface.blit(next_image,next_rect)
                    rect = next_rect
                surface.set_colorkey((255,255,255))
                image = surface
            else:
                image = font.render(self.text,True,text_color,None)
            return image
        
        #intialize text image using text in self memory
        text_color = ((2,2,70))
        font = size_text(40)
        self.font_image = Make_image()
        self.font_rect = self.font_image.get_rect()
        self.font_rect.centerx = self.rect.centerx
        self.font_rect.centery = self.rect.centery

    def check_contained(self,x,y):
        """compares coordinates given with hitbox, used in mouse detection but can be generalized if needed by moving mouse detection outside.
        Will evaluate if mouse is clicked"""
        if self.active:
            self.reset()
            #if in horizontal bounds
            if x > self.left and x < self.right:
                slope = 1/sqrt(3)
                #use to set create verticle bounds
                if x - self.center_x <= 0:
                    slope *= -1

                ################
                x_rel = x - self.center_x #bounds depends on x location of the mouse 
                bottom_bound = self.bottom - (x_rel*slope)
                top_bound = self.top - (x_rel*-slope)
                ################

                if y >= top_bound and y <= bottom_bound:
                    if Ctrl_Vars.Left_MouseDown:
                        self.press() # if all conditions are met use functionality

    def translate(self,dx):
        #moves entire object. Used in folding unfolding
        self.left += dx
        self.right += dx
        self.center_x += dx
        self.rect.left += dx
        self.font_rect.left += dx

    def draw(self):
        if not self.hide:
            if self.On:
                i = 0
            else:
                i = 1
            self.images[i].set_colorkey((255,0,255))
            Screen.blit(self.images[i], self.rect)
            Screen.blit(self.font_image,self.font_rect)

#Mother Folder vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
class Folder(Hex_Button):
    """A class of button that holds a foldable submenu of buttons"""
    def __init__(self,Coords,text = "N/A"):
        Hex_Button.__init__(self,Coords,text,OpenFolder,None,True)
        self.open = False
        #animation parameters
        self.frames = 6
        self.frame_count = 0

        self.width = self.rect.right - self.rect.left
        self.pixel_increment = self.width // self.frames

        self.build_submenu()

    def reset(self):
        #resets the folder to its original operational state
        if not self.open: #closed
            #unfold
            if self.frame_count > 0:
                for i in range(len(self.Buttons)):
                    self.Buttons[i].active = False
                self.frame_count -= 1
                self.translate_group(-self.pixel_increment)
            elif self.frame_count == 0:
                #turn off
                self.frame_count = 0
                self.On = False

    def build_submenu(self):
        #creates a list of button objects to make a menu with
        self.Buttons = []

    def check_contained(self,x,y):
        #Campares mouse cordinates with hitbox
        """The first pass of the if statement operates liek the parent class,
        the second pass extends the hitbox over the hitboxes of every button
        in the submenu, it will not activate a functionality at that point
        since its functionality by that point is already being use"""
        if not self.open: #closed
            self.check_contained_closed(x,y)
        else:
            self.check_contained_opened(x,y)
        #hit detection of all submenu options active once all first hitbox check goes thru
        for j in range(len(self.Buttons)):
            self.Buttons[j].check_contained(x,y)

    def check_contained_closed(self,x,y):
        self.reset() #reset every before evaluating. Will not be noticed since its not drawn until after it is set again
        #horizontal bounds
        if x >= self.left and x <= self.right:
            slope1 = 1/sqrt(3)
            slope2 = 1/sqrt(3)

            if x - self.center_x <= 0:
                slope2 *= -1
            else:
                slope1 *= -1

            ################
            x_rel = x - self.center_x
            bottom_bound = self.bottom - (x_rel*slope2)
            top_bound = self.top - (x_rel*slope1)
            ################
            #verticle bounds based on hexagonal shape
            if y >= top_bound and y <= bottom_bound:
                if Ctrl_Vars.Left_MouseDown:
                    self.press()

    def check_contained_opened(self,x,y):
        self.open = False #reset this until evaluated as open
        """Since the folder is now open we evaluate the hitbox as its original size, times all the button submenues extended to the right.
        This is done with similar code as the closed case, but just using a for loop over"""
        for i in range(len(self.Buttons)+1):
            displacement = i * self.width
            horizontal_bound = x >= (self.left + displacement) and (x <= self.right + displacement)

            if horizontal_bound:
                slope1 = 1/sqrt(3)
                slope2 = 1/sqrt(3)

                if x - (self.center_x + displacement) <= 0:
                    slope2 *= -1
                else:
                    slope1 *= -1

                ################
                x_rel = x - (self.center_x + displacement)
                bottom_bound = self.bottom - (x_rel*slope2)
                top_bound = self.top - (x_rel*slope1)
                ################
                if y >= top_bound and y <= bottom_bound:
                    self.functionality(self)

    def translate_group(self,dx):
        #move all objects in the submenu
        for i in range(len(self.Buttons)):
            self.Buttons[i].translate(dx*(i+1))

    def draw(self):
        if not self.hide:
            if self.On:
                i = 0 #image selector
                for j in range(len(self.Buttons)):
                    self.Buttons[j].hide = False
                self.draw_submenu() #dont have to draw this otherwise
            else:
                i = 1
                for j in range(len(self.Buttons)):
                    self.Buttons[j].hide = True
            self.images[i].set_colorkey((255,0,255))
            Screen.blit(self.images[i], self.rect)
            Screen.blit(self.font_image,self.font_rect)

    def draw_submenu(self):
        #draws the sub class objects kept in the list
        for i in range(len(self.Buttons)):
            self.Buttons[i].draw()

"""Simple Button specialized types ***************************************************************************"""
#Number PAD
class Key(Hex_Button):
    def __init__(self,Coords,value):
        text = "{}".format(str(value))
        Hex_Button.__init__(self,Coords,text,key)
        self.value = str(value)

#Extras ------------------
class Music_Button(Hex_Button):
    def __init__(self,Coords,N):
        def functionality(self):
            if self.N < len(self.music_library):
                sleep(0.25)
                pygame.mixer.music.load(
                    'Music/{}.mp3'.format(self.text)
                    )
                pygame.mixer.music.play(-1)
        self.music_library = ["6 Solutions per Side","Bad KpR","Beach Ball","Navy Blues","Approach","Think"]
        self.N = N
        if self.N < len(self.music_library):
            text = self.music_library[N]
        else:
            text = 'N/A'
        Hex_Button.__init__(self,Coords,text,functionality)

class Delete_World(Hex_Button):
    def __init__(self,Coords,text,active,LIST):
        Hex_Button.__init__(self,Coords,text,DeleteWorld,None,active)
        self.clicked = False
        self.text = "Delete"
        self.init_text()
        self.LIST = LIST
        self.name = None

class Load_World(Hex_Button):
    def __init__(self,Coords,text,active):
        Hex_Button.__init__(self,Coords,text,LoadWorld,None,active)
        self.clicked = False
        self.text = "Load"
        self.init_text()
        self.name = None

"""Specialized Folders   *******************************************************************************"""
#Start Screen
class Play(Folder):
    def __init__(self,Coords):
        Folder.__init__(self,Coords)
        self.text = "Play!"
        self.init_text()

    def build_submenu(self):
        #Play Options ----
        self.Buttons = [
            Hex_Button(self.Coords,"Random",Menu_Nav,"Random",False),
            Hex_Button(self.Coords,"Load World",Start_Nav,"Load World",False),
            Hex_Button(self.Coords,"Seed",Start_Nav,"Seed",False)
        ]

class Extras(Folder):
    def __init__(self,Coords):
        Folder.__init__(self,Coords)

    def build_submenu(self):
        #Extras Options ----
        self.text = "Extras!"
        self.init_text()
        self.Buttons = [
            Hex_Button(self.Coords,"Jukebox",Start_Nav,("Jukebox"),False),
            Hex_Button(self.Coords,"World Creator",Menu_Nav,("World Creator"),False),
            Hex_Button(self.Coords)
        ]

class Settings(Folder):
    def __init__(self,Coords,Settings):
        Folder.__init__(self,Coords)
        self.text = 'Settings'
        self.init_text()
        
    def build_submenu(self):
        #Settings Options ----
        self.Buttons = [
            Hex_Button(self.Coords,"Volume",Start_Nav,"Volume",False),
            Hex_Button(self.Coords,"Display",Start_Nav,"Display",False),
            Hex_Button(self.Coords)
        ]

#Quit Folder
class Quit_Folder(Folder):
    def __init__(self,Coords):
        Folder.__init__(self,Coords)
        self.text = "Quit"
        self.init_text()

    def build_submenu(self):
        #Settings Options ----
        self.Buttons = [
            Hex_Button(self.Coords,"Title Screen",Menu_Nav,"Title Screen",False),
            Hex_Button(self.Coords,"Quit",Exit)
        ]

"""SLIDERS *********************************************************************************************"""
class Slider_Bar():
    def __init__(self,x,y,Name):
        self.margin = 39
        self.init_image(x,y)

        self.color = (3,12,128)
        self.fill = pygame.Surface((0,59))
        self.fill.fill(self.color)
        self.fill_rect = self.fill.get_rect()
        self.fill_rect.left = self.image_rect.left + self.margin
        self.fill_rect.centery = self.image_rect.centery

        self.text_color = ((255,255,255))
        self.title = Name
        #self.init_title(35)

        self.value = 0
        self.init_text(35)
        self.length = 1400 #actually 1445 but minus the knob width which is 47

    def init_image(self,x,y):
        self.image = pygame.image.load('HUD/Slider_Bar.png').convert()
        self.image.set_colorkey((255,0,255))
        self.image_rect = self.image.get_rect()
        self.image_rect.centerx = x
        self.image_rect.centery = y
        Kx = self.image_rect.left + self.margin
        Ky = self.image_rect.top
        self.Knob = Slider_Knob(Kx,Ky)

    def init_text(self,size):
        #intialize text image using text in self memory
        font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",size)
        font.set_bold(True)
        text = self.title + ':  {}'.format(self.value)
        self.text_image = font.render(text,True,self.text_color,None)
        self.text_rect = self.text_image.get_rect()
        self.text_rect.left = self.image_rect.left
        self.text_rect.bottom = self.image_rect.top - 6

    def update(self):
        dx = self.Knob.rect.left - (self.image_rect.left + self.margin) 
        if dx <= 0:
            dx =0
        elif dx >= self.length:
            dx = self.length
        self.value = dx//14
        #updating graphics
        self.init_text(35)
        self.fill = pygame.Surface((dx+30,58))
        self.fill.fill(self.color)
        self.fill_rect = self.fill.get_rect()
        self.fill_rect.left = self.image_rect.left + self.margin
        self.fill_rect.centery = self.image_rect.centery

    def Slide_Knob(self,dx):
        #right bound
        if self.Knob.rect.left + dx <= self.image_rect.left:
            self.Knob.rect.left = self.image_rect.left + self.margin
        #left bound
        elif self.Knob.rect.right + dx >= self.image_rect.right:
            self.Knob.rect.right = self.image_rect.right - self.margin
        #operational area
        else:
            self.Knob.rect.left += dx
            self.update()

    def set_Knob(self):
        dx = self.value * 14
        self.Knob.rect.left = self.image_rect.left + self.margin + dx
        self.update()

    def draw(self):
        Screen.blit(self.text_image,self.text_rect)
        Screen.blit(self.image,self.image_rect)
        Screen.blit(self.fill,self.fill_rect)
        self.Knob.draw()

    def check_contained(self,x,y):
        if y >= self.image_rect.top and y <= self.image_rect.bottom: #since its narrow, check first
            if x >= self.image_rect.left + self.margin and x <= self.image_rect.right - self.margin:
                if Ctrl_Vars.Left_MouseDown:
                    dx = x - self.Knob.rect.centerx
                    self.Slide_Knob(dx)

class Slider_Knob():
    def __init__(self,x,y):
        self.image = pygame.image.load('HUD/Slider_Knob.png').convert()
        self.image.set_colorkey((255,0,255))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def draw(self):
        Screen.blit(self.image,self.rect)

class Typing_Box():
    def __init__(self,Screen):
        self.image = pygame.Surface((1000,200))
        self.image.fill((0,0,0))
        self.image.set_alpha(185)
        self.rect = self.image.get_rect()
        self.rect.centerx = ScreenRect.centerx
        self.rect.centery = ScreenRect.centery

    def draw(self):
        Screen.blit(self.image,self.rect)