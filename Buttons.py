import pygame
import pygame.font
from math import sqrt
import sys
from time import sleep

"""Mother class Buttons%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
#Simple Button (Mother) vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
class Hexagon_Button():
    def __init__(self,Screen,Coords,Ctrl_Vars,active = True):
        self.Coords = Coords
        self.Screen = Screen #needed for graphics
        self.Screen_rect = self.Screen.get_rect()
        self.Ctrl_Vars = Ctrl_Vars #needed for functionality

        self.images = [pygame.image.load('Title/MenuGonOnS.png').convert(),
            pygame.image.load('Title/MenuGonS.png').convert()]
        self.rect = self.images[0].get_rect()
        #geometric properties
        self.height = self.rect.bottom
        self.width = self.rect.right
        self.side_length = self.height/2
        self.offset = (self.width*(1/2))
        self.outline = 4
        
        #state of activity
        self.On = False
        if active:
            self.hide = False
            self.active = True
        else:
            self.hide = True
            self.active = False

        #location
        self.position() #set position

        #Text (Default string and size)
        self.text = "N/A"
        self.init_text()

        self.sound = pygame.mixer.Sound("SFX/Button_press.wav")

    def position(self):
        #sets position of object based on where it is stored on an array grid
        x = self.Coords[0]
        y = self.Coords[1]

        self.left = x * (self.width)
        self.right = self.width + self.left
        self.bottom = self.Screen_rect.bottom - (y * (self.height * (3/4)))
        self.top = self.bottom - self.height
        if y%2 == 0: #stagger rows
            self.left += self.offset
            self.right += self.offset
        self.center_x = self.width/2 + self.left

        self.rect.left = self.left
        self.rect.bottom = self.bottom

    def init_text(self):
        def size_text():
            font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",self.size)
            font.set_bold(True)
            words = self.text.split()
            largest_word = words[0]
            if len(words) > 1:
                for word in words:
                    if len(word) >= len(largest_word):
                        largest_word = word
            TstFntImg = font.render(largest_word,True,text_color,None)
            rect = TstFntImg.get_rect()
            while rect.width > self.height - 40 or self.size <= 3:
                self.size -= 1
                font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",self.size)
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
        self.size = 40
        text_color = ((2,2,70))
        font = size_text()
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
            if x >= self.left and x <= self.right:
                slope1 = 1/sqrt(3)
                slope2 = 1/sqrt(3)
                #use to set create verticle bounds
                if x - self.center_x <= 0:
                    slope2 *= -1
                else:
                    slope1 *= -1

                ################
                x_rel = x - self.center_x #bounds depends on x location of the mouse 
                bottom_bound = self.bottom - (x_rel*slope2)
                top_bound = self.top - (x_rel*slope1)
                ################

                if y >= top_bound and y <= bottom_bound:
                    if self.Ctrl_Vars.Left_MouseDown:
                        self.press() # if all conditions are met use functionality

    def draw(self):
        if not self.hide:
            if self.On:
                i = 0
            else:
                i = 1
            self.images[i].set_colorkey((255,0,255))
            self.Screen.blit(self.images[i], self.rect)
        self.draw_text()

    def press(self):
        #General functionality is just to shine and turn off
        self.On = True
        if self.Ctrl_Vars.Left_click:
            pygame.mixer.Sound.play(self.sound)
            self.Ctrl_Vars.Left_click = False
            self.Ctrl_Vars.Left_MouseDown = False
            self.functionality() #Specific functiality: defined by daughter classes

    def functionality(self):
        print("No functioanlity")

    def reset(self):
        #default reset is to turn off shine
        self.On = False

    def translate(self,dx):
        #moves entire object. Used in folding unfolding
        self.left += dx
        self.right += dx
        self.center_x += dx
        self.rect.left += dx
        self.font_rect.left += dx

    def draw_text(self):
        self.Screen.blit(self.font_image,self.font_rect)

#Mother Folder vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
class Folder(Hexagon_Button):
    """A class of button that holds a foldable submenu of buttons"""
    def __init__(self,Screen,Coords,Ctrl_Vars):
        Hexagon_Button.__init__(self,Screen,Coords,Ctrl_Vars,False)
        self.hide = False
        self.open = False
        #animation parameters
        self.frames = 6
        self.pixel_increment = self.width // self.frames
        self.frame_count = 0

        self.build_submenu()

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
                if self.Ctrl_Vars.Left_MouseDown:
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
                    self.functionality()

    def functionality(self):
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

    def translate_group(self,dx):
        #move all objects in the submenu
        for i in range(len(self.Buttons)):
            self.Buttons[i].translate(dx*(i+1))

    def draw_submenu(self):
        #draws the sub class objects kept in the list
        for i in range(len(self.Buttons)):
            self.Buttons[i].draw()

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
            self.Screen.blit(self.images[i], self.rect)
            self.draw_text()
"""MENU SWITCHS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
class Start_Navigation(Hexagon_Button):
    def __init__(self,Screen,Coords,Ctrl_Vars,GoTo,Text,active = True):
        Hexagon_Button.__init__(self,Screen,Coords,Ctrl_Vars,active)
        self.GoTo = GoTo
        self.text = Text
        self.init_text()

    def functionality(self):
        #activates campaign mode
        self.Ctrl_Vars.Start_Vars.Menu_reset()
        self.Ctrl_Vars.Start_Vars.Set_Menu(self.GoTo)

class Menu_Navagation(Hexagon_Button):
    def __init__(self,Screen,Coords,Ctrl_Vars,load_type,Text,active = True):
        Hexagon_Button.__init__(self,Screen,Coords,Ctrl_Vars,active)
        self.text = Text
        self.init_text()
        self.load_type = load_type

    def functionality(self):
        self.Ctrl_Vars.Game_Menu_Vars.Menu_reset()
        self.Ctrl_Vars.Game_Menu_Vars.load_world = True
        self.Ctrl_Vars.Game_Menu_Vars.menu_select = False
        if self.load_type == "Custom":
            self.Ctrl_Vars.Game_Menu_Vars.Custom = True
        elif self.load_type == "Random":
            self.Ctrl_Vars.Game_Menu_Vars.Random = True
        else:
            self.Ctrl_Vars.Game_Menu_Vars.load_world = False
            self.Ctrl_Vars.Game_Menu_Vars.Game_active = False
            self.Ctrl_Vars.Game_Menu_Vars.Start_Screen = True
            self.Ctrl_Vars.Game_Menu_Vars.menu_select = True

"""Simple Button specialized types ***************************************************************************"""
#Number PAD
class Key(Hexagon_Button):
    def __init__(self,Screen,Coords,Ctrl_Vars,value):
        Hexagon_Button.__init__(self,Screen,Coords,Ctrl_Vars)
        self.text = "{}".format(str(value))
        self.init_text()
        self.value = str(value)

    def functionality(self):
        #activates campaign mode
        if len(self.Ctrl_Vars.seed) < 18:
            self.Ctrl_Vars.seed += "{}".format(self.value)

class Del_Key(Hexagon_Button):
    def __init__(self,Screen,Coords,Ctrl_Vars):
        Hexagon_Button.__init__(self,Screen,Coords,Ctrl_Vars)
        self.text = "Del"
        self.init_text()

    def functionality(self):
        #activates campaign mode
        self.Ctrl_Vars.seed = self.Ctrl_Vars.seed[:-1]

class Enter_Key(Hexagon_Button):
    def __init__(self,Screen,Coords,Ctrl_Vars):
        Hexagon_Button.__init__(self,Screen,Coords,Ctrl_Vars)
        self.text = "Enter"
        self.init_text()

    def functionality(self):
        #activates campaign mode
        if len(self.Ctrl_Vars.seed) >= 18:
            self.Ctrl_Vars.seed_menu = False
            self.Ctrl_Vars.load_world = True
            self.Ctrl_Vars.set_seed = True
            self.Ctrl_Vars.Start_Screen = False

class Clear(Hexagon_Button):
    def __init__(self,Screen,Coords,Ctrl_Vars):
        Hexagon_Button.__init__(self,Screen,Coords,Ctrl_Vars)
        self.text = "Clear"
        self.init_text()

    def functionality(self):
        #activates campaign mode
        self.Ctrl_Vars.seed = ""

class Save_seed(Hexagon_Button):
    def __init__(self,Screen,Coords,Ctrl_Vars):
        Hexagon_Button.__init__(self,Screen,Coords,Ctrl_Vars)
        self.text = "Save Seed"
        self.init_text()

    def functionality(self):
        #activates campaign mode
        File = 'Saved_Worlds/Favorite Seeds.txt'
        File = open(File,"a")
        File.writelines(self.Ctrl_Vars.seed + "\n")
        File.close()

class Resolution(Hexagon_Button):
    def __init__(self,Window,Screen,Coords,Ctrl_Vars,Settings,value,text):
        Hexagon_Button.__init__(self,Screen,Coords,Ctrl_Vars)
        self.text = text
        self.value = value
        self.init_text()
        self.Window = Window
        self.Settings = Settings

    def functionality(self):
        #activates campaign mode
        if self.Settings.resolution != self.value:
            self.Settings.resolution = self.value
            self.Settings.init_Screen()
            self.Window = self.Settings.create_window(self.Window)

#Extras ------------------
class Music_Button(Hexagon_Button):
    def __init__(self,Screen,Coords,N,Ctrl_Vars):
        Hexagon_Button.__init__(self,Screen,Coords,Ctrl_Vars)
        self.music_library = ["6 Solutions per Side","Bad KpR","Beach Ball","Navy Blues","Approach","Think"]
        self.N = N
        if self.N < len(self.music_library):
            self.text = self.music_library[N]
        else:
            self.text = 'N/A'
        self.init_text()

    def functionality(self):
        if self.N < len(self.music_library):
            sleep(0.25)
            pygame.mixer.music.load(
                'Music/{}.mp3'.format(self.text)
                )
            pygame.mixer.music.play(-1)

#Settings
class Default_Sound(Hexagon_Button):
    def __init__(self,Screen,Coords,Ctrl_Vars,Settings):
        Hexagon_Button.__init__(self,Screen,Coords,Ctrl_Vars)
        self.clicked = False
        self.Settings = Settings
        self.text = "Set Default"
        self.init_text()
        self.value = False

    def reset(self):
        self.On = False
        self.value = False

    def functionality(self):
        #activates campaign mode
        self.value = True

class Save_Settings(Hexagon_Button):
    def __init__(self,Screen,Coords,Ctrl_Vars,Settings):
        Hexagon_Button.__init__(self,Screen,Coords,Ctrl_Vars)
        self.clicked = False
        self.text = "Save"
        self.init_text()
        self.Settings = Settings

    def functionality(self):
        #activates campaign mode
        self.Settings.save_volume()

class Full_Screen(Hexagon_Button):
    def __init__(self,Screen,Coords,Ctrl_Vars,Settings,active):
        Hexagon_Button.__init__(self,Screen,Coords,Ctrl_Vars,active)
        self.Settings = Settings
        self.clicked = False
        self.text = "Full Screen"
        self.init_text()
    
    def functionality(self):
        #activates campaign mode
        self.Settings.toggle_fullscreen()
  
#In game: play-------------
class Resume(Hexagon_Button):
    def __init__(self,Screen,Coords,Ctrl_Vars):
        Hexagon_Button.__init__(self,Screen,Coords,Ctrl_Vars)
        self.clicked = False
        self.text = "Resume"
        self.init_text()

    def functionality(self):
        #activates campaign mode
        self.Ctrl_Vars.Game_Menu_Vars.Game_active = True
        self.Ctrl_Vars.Game_Menu_Vars.Pause = False

class Retry(Hexagon_Button):
    def __init__(self,Screen,Coords,Ctrl_Vars):
        Hexagon_Button.__init__(self,Screen,Coords,Ctrl_Vars)
        self.clicked = False
        self.text = "Retry"
        self.init_text()

    def functionality(self):
        #activates campaign mode
        self.Ctrl_Vars.Game_Menu_Vars.load_world = True
        self.Ctrl_Vars.Game_Menu_Vars.Pause = False

        self.Ctrl_Vars.restart_world = True
        self.Ctrl_Vars.Game_Menu_Vars.Game_Over = False
        self.Ctrl_Vars.Game_Menu_Vars.Game_Win = False

class Quit(Hexagon_Button):
    def __init__(self,Screen,Coords,Ctrl_Vars,active):
        Hexagon_Button.__init__(self,Screen,Coords,Ctrl_Vars,active)
        self.clicked = False
        self.text = "Desktop"
        self.init_text()

    def functionality(self):
        #activates campaign mode
        sleep(0.5)
        sys.exit(0)

"""Specialized Folders   *******************************************************************************"""
#Start Screen
class Play(Folder):
    def __init__(self,Screen,Coords,Ctrl_Vars):
        Folder.__init__(self,Screen,Coords,Ctrl_Vars)
        self.text = "Play!"
        self.init_text()

    def build_submenu(self):
        #Play Options ----
        self.Buttons = []
        campaign_Button = Menu_Navagation(self.Screen,self.Coords,self.Ctrl_Vars,"Random","Random",False)
        #campaign_Button = Campaign(self.Screen,self.Coords,self.Ctrl_Vars,False)
        Endless_Button = Hexagon_Button(self.Screen,self.Coords,self.Ctrl_Vars,False)
        seed_Button = Start_Navigation(self.Screen,self.Coords,self.Ctrl_Vars,"Num_Pad","Custom",False)
        self.Buttons.append(campaign_Button)
        self.Buttons.append(Endless_Button)
        self.Buttons.append(seed_Button)

class Extras(Folder):
    def __init__(self,Screen,Coords,Ctrl_Vars):
        Folder.__init__(self,Screen,Coords,Ctrl_Vars)

    def build_submenu(self):
        #Extras Options ----
        self.text = "Extras!"
        self.init_text()
        self.Buttons = []
        Jukebox_Button = Start_Navigation(self.Screen,self.Coords,self.Ctrl_Vars,"Jukebox","Jukebox",True)
        Gallary_Button = Hexagon_Button(self.Screen,self.Coords,self.Ctrl_Vars,False)
        Store_Button = Hexagon_Button(self.Screen,self.Coords,self.Ctrl_Vars,False)
        self.Buttons.append(Jukebox_Button)
        self.Buttons.append(Gallary_Button)
        self.Buttons.append(Store_Button)

class Settings(Folder):
    def __init__(self,Screen,Coords,Ctrl_Vars,Settings):
        Folder.__init__(self,Screen,Coords,Ctrl_Vars)
        self.text = 'Settings'
        self.init_text()
        
    def build_submenu(self):
        #Settings Options ----
        self.Buttons = []
        Sound_Button = Start_Navigation(self.Screen,self.Coords,self.Ctrl_Vars,"Sound_Settings","Volume",True)
        Display_Button = Start_Navigation(self.Screen,self.Coords,self.Ctrl_Vars,"Display_Settings","Display",True)
        Controls_Button = Hexagon_Button(self.Screen,self.Coords,self.Ctrl_Vars,False)
        self.Buttons.append(Display_Button)
        self.Buttons.append(Sound_Button)
        self.Buttons.append(Controls_Button)

#Pause Screen
class Quit_Folder(Folder):
    def __init__(self,Screen,Coords,Ctrl_Vars):
        Folder.__init__(self,Screen,Coords,Ctrl_Vars)
        self.text = "Quit"
        self.init_text()

    def build_submenu(self):
        #Settings Options ----
        self.Buttons = []
        return_start = Menu_Navagation(self.Screen,self.Coords,self.Ctrl_Vars,"Return Start","Return Start",False)
        #return_start = Return_start(self.Screen,self.Coords,self.Ctrl_Vars,False)
        Exit = Quit(self.Screen,self.Coords,self.Ctrl_Vars,False)
        self.Buttons.append(return_start)
        self.Buttons.append(Exit)

"""SLIDERS *********************************************************************************************"""
class Slider_Bar():
    def __init__(self,Screen,Ctrl_Vars,x,y,Name):
        self.Screen = Screen #needed for graphics
        self.Screen_rect = self.Screen.get_rect()
        self.Ctrl_Vars = Ctrl_Vars
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
        self.Knob = Slider_Knob(self.Screen,self.Ctrl_Vars,Kx,Ky)

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
        self.Screen.blit(self.text_image,self.text_rect)
        self.Screen.blit(self.image,self.image_rect)
        self.Screen.blit(self.fill,self.fill_rect)
        self.Knob.draw()

    def check_contained(self,x,y):
        if y >= self.image_rect.top and y <= self.image_rect.bottom: #since its narrow, check first
            if x >= self.image_rect.left + self.margin and x <= self.image_rect.right - self.margin:
                if self.Ctrl_Vars.Left_MouseDown:
                    dx = x - self.Knob.rect.centerx
                    self.Slide_Knob(dx)

class Slider_Knob():
    def __init__(self,Screen,Ctrl_Vars,x,y):
        self.Screen = Screen #needed for graphics
        self.Screen_rect = self.Screen.get_rect()
        self.image = pygame.image.load('HUD/Slider_Knob.png').convert()
        self.image.set_colorkey((255,0,255))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def draw(self):
        self.Screen.blit(self.image,self.rect)