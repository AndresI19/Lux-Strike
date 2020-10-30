import pygame

#graphics master loops vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
#main game
def Display(Screen,World,HUD,Player,Enemies,Drops):
    Screen.fill((0,0,0))
    Draw_map(World,Player,Enemies,Drops)
    HUD.draw()

def Draw_map(World,Player,Enemies,Drops):
    for row in range(World.num_rows):
        draw_row = World.num_rows - row - 1
        for col in range(World.num_cols):
            World.Map.data(col,draw_row).draw()
        if Player.row == draw_row:
            Player.Draw()
        for enemy in Enemies.Group:
            if enemy.row == draw_row:
                enemy.Draw()
        for drop in Drops.Group:
            if drop.row == draw_row:
                drop.draw()

def scale(Window,Screen,Settings):
    if not Settings.settings['Resolution'] == [1920,1080] and not Settings.settings['Full Screen'] == True:
        Screen = pygame.transform.scale(Screen,(Settings.Screen_width,Settings.Screen_height))
    Window.blit(Screen,(0,0))
    pygame.display.flip()

#Menu displays
def Menu_diplay(Menu):
    Menu.draw()
    pygame.display.flip()

#graphics master loops ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
""" TODO: #Loading Screen object"""
class Load_Screen():
    def __init__(self,Window,Screen,Settings,N):
        #loading screen variables
        self.Window = Window
        self.Settings = Settings
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
        self.scale_draw()

    def scale_draw(self):
        if not self.Settings.settings['Resolution'] == [1920,1080]:
            Screen = pygame.transform.scale(
                self.Screen,(self.Settings.Screen_width,self.Settings.Screen_height))
        else:
            Screen = self.Screen
        self.Window.blit(Screen,(0,0))
        pygame.display.flip()

    def Update(self):
        self.count += self.i
        if self.count >= self.requirement:
            self.count = 0
            self.bar_left += 2
            if self.bar_left <= (1826):
                self.Screen.blit(self.bar,(self.bar_left,self.bar_top))
            self.scale_draw()
        
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
