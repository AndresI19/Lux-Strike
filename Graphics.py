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
    def __init__(self,Window,Screen,Settings):
        #loading screen variables
        self.Window = Window
        self.Settings = Settings
        self.Screen = Screen
        self.screen_rect = self.Screen.get_rect()

        self.bar_size = (self.screen_rect.width * 9) // 10
        self.bar_left = self.screen_rect.width/20 + 2
        self.bar_top = self.screen_rect.bottom * (9/10) - 100
        self.bar = pygame.image.load('HUD/Bar.png')

        self.count = 0 #dynamic
        self.bar_frame = pygame.image.load('HUD/Load_Bar.png').convert()
        self.bar_frame.set_colorkey((255,0,255))
        self.Screen.blit(self.bar_frame,(0,self.bar_top-9))

        self.init_text()
        self.scale_draw()

    def set_steps(self,N):
        self.i = float(1/N) * 100 * 2
        self.requirement = self.bar_size/N

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

class word_object():
    #Word object, is nothing more than a rendered text object, with the ability to display in a certain way
    def __init__(self,word,tags):
        self.word = word
        self.length = len(self.word)
        self.text = ""
        self.frame = 0
        self.full = False
        self.quake,self.flash = False,False
        self.set_tags(tags)
        font_size = 30
        self.font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",font_size)
        self.font.set_bold(True)
        self.sound = pygame.mixer.Sound("SFX/letter type.wav")

    def init_text(self):
        self.font_image = self.font.render(self.text,True,self.color,None)
        self.font_rect = self.font_image.get_rect()

    def set_tags(self,tags):
        #/ - New line || $ - Color || % - Effect
        self.color = (255,255,255)
        for tag in tags:
            if tag[0] == '$':
                if tag[1] == 'R':
                    self.color = (255,0,0)
                elif tag[1] == 'G':
                    self.color = (0,255,0)
                elif tag[1] == 'B':
                    self.color = (0,0,255)
                elif tag[1] == 'Y':
                    self.color = (255,255,0)
            elif tag[0] == '%':
                if tag[1] == 'Q':
                    self.quake = True
                elif tag[1] == 'F':
                    self.flash = True

    def after_effects(self,coordinates):
        x = coordinates[0]
        y = coordinates[1]
        if self.quake:
            if self.frame%4 == 0:
                y += 2
            elif self.frame%4 == 2:
                y -= 2
        if self.flash:
            if self.frame%40 == 0:
                self.font_image = self.font.render(self.text,True,self.color,None)
            elif self.frame%40 == 20:
                self.font_image = self.font.render(self.text,True,(0,0,0),None)
        return (x,y)

    def draw(self,Screen,coordinates):
        if self.frame >= self.length:
            self.full = True
        else:
            self.text += self.word[self.frame]
            self.init_text()
            pygame.mixer.Sound.play(self.sound)
        self.frame += 1
        coordinates = self.after_effects(coordinates)
        Screen.blit(self.font_image,coordinates)

    def print(self):#for testing. will delete
        print(self.word)

#ANIMATION OBJECT
class Animation():
    def __init__(self,Screen,reel,speed = 1,Type = 0):
        self.Screen = Screen
        self.reel = reel
        self.speed = speed
        self.frames = len(reel) * self.speed
        self.active = False

        self.count = 0 

        if Type == 0 or Type == 'loop':
            self.clock = self.clock_loop
        elif Type == 1 or Type == 'wave':
            self.flip_flop = 1
            self.clock = self.clock_wave
        elif Type == 2 or Type == 'once':
            self.clock = self.clock_once
        else:
            print("Failed to init animation type, default to loop")
            self.clock = self.clock_loop

    def clock_loop(self):
        if self.count + 1 >= self.frames:
            self.count = 0
        else:
            self.count += 1
        self.image = self.reel[self.count//self.speed]

    def clock_wave(self):
        if self.flip_flop > 0:
            if self.count + 1 >= self.frames:
                self.flip_flop *= -1
        elif self.count - 1 < 0:
            self.flip_flop *= -1
        self.count += self.flip_flop
        self.image = self.reel[self.count//self.speed]

    def clock_once(self):
        if self.active:
            if self.count + 1 >= self.frames:
                self.toggle()
            else:
                self.count += 1
            self.image = self.reel[self.count//self.speed]
            return True

    def toggle(self):
        if self.active:
            self.active = False
        else:
            self.active = True

    def draw(self,rect):
        self.Screen.blit(self.image,rect)
    
    def get_rect(self):
        return self.reel[0].get_rect()
