import pygame.display

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

    def toggle_fullscreen(self):
        if self.fullscreen:
            self.fullscreen = False
            pygame.display.set_mode((
                self.resolution_list[self.resolution]))
        else:
            self.fullscreen = True
            pygame.display.set_mode((
                self.resolution_list[self.resolution]),pygame.FULLSCREEN)


    