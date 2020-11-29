import pygame
import json

#Class for display,sound and TODO: Controls
class Settings():
    def __init__(self):
        self.path = 'Saved_Worlds/Settings.json'
        self.settings = {           #These are default settings, this dictionary gets implemented but in case something fails its here
            "Master volume" : 100,
            "SFX volume" : 100,
            "Music volume" : 100,
            "Voice volume" : 100,
            "Resolution" : [1600,900],
            "Full Screen" : False
        }

        self.drag_sensativity = 1
        self.Load_settings()
        self.init_Screen()
        
        self.box = 0

    def init_Screen(self):
        self.Screen_width, self.Screen_height = self.settings['Resolution']
        self.Screen_center = [self.Screen_width//2,self.Screen_height//2]
        self.mouseX_scaling = 1920/self.Screen_width
        self.mouseY_scaling = 1080/self.Screen_height
    
    def create_window(self):
        if self.settings['Full Screen']:
            window = pygame.display.set_mode(self.settings['Resolution'],pygame.FULLSCREEN)
        else:
            window = pygame.display.set_mode((self.Screen_width,self.Screen_height))

        return window

    def default_resolution(self):
        self.settings['Resolution'] = [1600,900]
        self.settings['Full Screen'] = False

    def toggle_fullscreen(self):
        if self.settings['Full Screen']:
            self.settings['Full Screen'] = False
            self.settings['Resolution'] = [1600,900]
            self.init_Screen()
            pygame.display.set_mode(self.settings['Resolution'])
        else:
            self.settings['Full Screen'] = True
            self.settings['Resolution'] = [1920,1080]
            self.init_Screen()
            pygame.display.set_mode(self.settings['Resolution'],pygame.FULLSCREEN)

    def default_volume(self):
        self.settings["Master volume"] = 100
        self.settings["SFX volume"] = 100
        self.settings["Music volume"] = 100
        self.settings["Voice volume"] = 100

    def Save_settings(self):
        data = {
            "Master volume" : self.settings['Master volume'],
            "SFX volume" : self.settings['SFX volume'],
            "Music volume" : self.settings['Music volume'],
            "Voice volume" : self.settings['Voice volume'],
            "Resolution" : self.settings['Resolution'],
            "Full Screen" : self.settings['Full Screen']
        }
        with open (self.path,'w') as Save_file:
            json.dump(data,Save_file)
        Save_file.close()

    def Load_settings(self):
        with open (self.path,'r') as Save_file:
            data = json.load(Save_file)
        self.settings['Master volume'] = data["Master volume"]
        self.settings['SFX volume'] = data["SFX volume"]
        self.settings['Music volume'] = data["Music volume"]
        self.settings['Voice volume'] = data["Voice volume"]
        self.settings['Resolution'] = data["Resolution"]
        self.settings['Full Screen'] = data["Full Screen"]