#World creator HUD
import pygame
import pygame.font

class WC_HUD():
    def __init__(self,Screen,Ctrl_Vars):
        self.Screen = Screen
        self.Screen_rect = Screen.get_rect()
        self.hotbar = Hotbar(Screen,Ctrl_Vars)
        self.Ctrl_Vars = Ctrl_Vars

    def draw(self):
        if self.Ctrl_Vars.WC_Tools.HUD_Visable:
            self.hotbar.draw()

class Hotbar():
    def __init__(self,Screen,Ctrl_Vars):
        self.Screen = Screen
        self.Ctrl_Vars = Ctrl_Vars
        self.image = pygame.Surface((1000,75))
        self.image.fill((55,37,40))
        self.rect = self.image.get_rect()

        Screen_rect = Screen.get_rect()
        self.rect.centerx = Screen_rect.centerx
        self.rect.bottom = Screen_rect.bottom - 50

        self.font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",20)
        self.font.set_bold(True)

        self.init_text()

    def init_text(self):
        self.text = self.font.render(str(self.Ctrl_Vars.WC_Tools.ID),True,(255,255,255),None)
        self.text_rect = self.text.get_rect()
        self.text_rect.centery = self.rect.bottom - 25
        self.text_rect.right = self.rect.right - 25

    def draw(self):
        self.Screen.blit(self.image,self.rect)
        self.Screen.blit(self.text,self.text_rect)