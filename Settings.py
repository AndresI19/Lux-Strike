import pygame.display
import text_reader as tr

#class for player set variables
class Settings():
    def __init__(self):
        #Initialize games static settings.
        # Screen settings
        self.resolution_list = ((1920,1080),(1600,900))
        self.resolution = 0
        self.Screen_width = self.resolution_list[self.resolution][0]
        self.Screen_height = self.resolution_list[self.resolution][1]
        self.Screen_center = [self.Screen_width//2,self.Screen_height//2]

        self.bg_color = (255,255,255)

        self.drag_sensativity = 1
        self.fullscreen = False

        self.set_settings_from_file()
        
        self.box = 0

    def set_settings_from_file(self):
        self.master_volume = tr.get_settings('master_volume')
        self.SFX_volume = tr.get_settings('SFX_volume')
        self.music_volume = tr.get_settings('music_volume')
        self.voice_volume = tr.get_settings('voice_volume')

    def set_default_settings(self):
        self.master_volume = 100
        self.SFX_volume = 100
        self.music_volume = 100
        self.voice_volume = 100

    def set_master_volume(self,value):
        value = round(value)
        self.master_volume = value
        self.SFX_volume *= value
        self.music_volume *= value
        self.voice_volume *= value

    #simple full screen toggle
    def toggle_fullscreen(self):
        if self.fullscreen:
            self.fullscreen = False
            pygame.display.set_mode((
                self.resolution_list[self.resolution]))
        else:
            self.fullscreen = True
            pygame.display.set_mode((
                self.resolution_list[self.resolution]),pygame.FULLSCREEN)
