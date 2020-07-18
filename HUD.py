import pygame
import pygame.font
import text_reader
pygame.mixer.init()

#Envelope class containing all border rectangles
class HUD():
    def __init__(self,Settings,Screen,Ctrl_Vars,World,Player,Enemies):
        self.Screen = Screen
        self.Screen_rect = Screen.get_rect()
        self.Settings = Settings
        self.HUD_Borders = self.make_HUD_Borders()
        self.Player_Stats = Player_Stats(Screen,Player.Stats)
        self.Mini_map = Mini_map(Screen,World,Player,Enemies)
        self.Dialog_box = Dialog_box(Screen,Ctrl_Vars)
        self.init_text(World)

    def init_text(self,World):
        #initialize the text that displays the seed
        self.text_color = ((255,255,255))
        self.font_size = 15
        self.font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",self.font_size)
        self.font.set_bold(True)
        self.font_image = self.font.render("Seed: "+ World.seed,True,self.text_color,None)
        self.font_rect = self.font_image.get_rect()
        self.font_rect.right = self.Screen_rect.right - 1
        self.font_rect.top = self.Screen_rect.top + 3

    def make_HUD_Borders(self):
        #left border margin
        Left = pygame.Surface((self.Settings.Screen_width//18,self.Settings.Screen_height))
        Left_rect = Left.get_rect()

        #Bottom border margin
        Bottom = pygame.Surface((self.Settings.Screen_width,self.Settings.Screen_height//9))
        Bottom_rect = Bottom.get_rect()
        Bottom_rect.bottom = self.Screen_rect.bottom

        #Right border margin
        Right = pygame.Surface((self.Settings.Screen_width//9,self.Settings.Screen_height))
        Right_rect = Right.get_rect()
        Right_rect.right = self.Screen_rect.right

        #add all border margins to a list for easy operation
        HUD_Borders = [Left,Bottom,Right]
        HUD_rects = [Left_rect,Bottom_rect,Right_rect]
        for i in range(3):
            HUD_Borders[i].convert()
            HUD_Borders[i].fill((0,0,0))
        return (HUD_Borders,HUD_rects)

    def draw(self):
        for i in range(3):
            self.Screen.blit(self.HUD_Borders[0][i],self.HUD_Borders[1][i])
        self.Mini_map.draw()
        self.Player_Stats.draw()
        self.Screen.blit(self.font_image,self.font_rect)
        #self.Dialog_box.draw()
        
#Left
class Player_Stats():
    def __init__(self,Screen,Stats):
        self.Screen = Screen
        self.Stats = Stats
        self.Empty_bar = pygame.image.load("HUD/HealthBar.png").convert()
        self.Empty_bar.set_colorkey((255,0,255))
        self.Empty_bar_rect = self.Empty_bar.get_rect()
        self.Empty_bar_rect.top = 5
        self.Empty_bar_rect.left = 5

        self.Health_Points_display = []
        self.position_health_points()

    def position_health_points(self):
        j = 2
        i = 0
        flip = 1
        while i <= 5:
            healthIcon = HealthIcon(j,i)
            self.Health_Points_display.append(healthIcon)
            if flip == 1:
                j -= 1
                i += 1
            else:
                j += 1
            flip *= -1

    def draw(self):
        self.Screen.blit(self.Empty_bar,self.Empty_bar_rect)
        #draw each icon over it
        for i in range(self.Stats.Health_Points):
            self.Health_Points_display[i].draw(self.Screen)

class HealthIcon():
    def __init__(self,x,y):
        #a single health icon
        self.HealthIcon = pygame.image.load("HUD/HealthIcon.png").convert()
        self.HealthIcon.set_colorkey((255,0,255))
        self.HealthIcon_rect = self.HealthIcon.get_rect()
        self.build(x,y)

    def build(self,x,y):
        outline = 1

        width = self.HealthIcon_rect.right
        side_length = width//2
        offset = side_length * (3/2)
        
        position_y = 41
        position_x = 5

        self.HealthIcon_rect.bottom = x * ((self.HealthIcon_rect.height / 2) - outline) + position_y
        self.HealthIcon_rect.left = y * (width + side_length) + position_x
        if x%2 == 0:
            self.HealthIcon_rect.left += offset

    def draw(self,Screen):
        Screen.blit(self.HealthIcon,self.HealthIcon_rect)

class Mini_map():
    def __init__(self,Screen,World,Player,Enemies):
        self.Screen = Screen
        self.World = World
        self.Player = Player
        self.Enemies = Enemies
        self.scaling_factor = 4

    def draw(self):
        for col in range(len(self.World.Terrain)):
            for row in range(len(self.World.Terrain[col])):
                self.World.Terrain[-1-col][row].Icon.draw()
        self.Enemies.Icon_draw()
        self.Player.Icon.draw()

class Dialog_box():
    def __init__(self,Screen,Ctrl_Vars):
        self.Screen = Screen
        self.Screen_rect = self.Screen.get_rect()
        self.Ctrl_Vars = Ctrl_Vars
        self.init_background()

        self.dialog_x = self.background_rect.left + 30
        self.dialog_y = self.background_rect.top + 10

        self.character_name = ''
        self.font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",25)
        self.font.set_bold(True)

        self.frame = 0
        self.box = []
        self.init_dialog()

    def init_background(self):
        self.background_image = pygame.Surface(
            (self.Screen_rect.width//2,self.Screen_rect.height//5)
            )
        self.background_image.convert()
        self.background_image.fill((2,2,70))
        self.background_image.set_alpha(185)
        self.background_rect = self.background_image.get_rect()
        self.background_rect.centerx = self.Screen_rect.centerx
        self.background_rect.bottom = self.Screen_rect.bottom - 100

    def init_dialog(self):
        File = "Dialog/Dialog.txt"
        Code = 'Tutorial0'
        #Code = "E2P2"
        self.dialog = text_reader.load_text(Code,File)
        self.init_box()

    def init_box(self):
        if self.Ctrl_Vars.box_count < len(self.dialog):
            count = self.Ctrl_Vars.box_count
            profile = self.dialog[count][0]
            self.character_name = profile['Character']
            self.init_character_text()
            self.image_path = profile['Image_Code']
            self.portrait_side = profile['Side']
            self.init_portraits()
            self.box = self.dialog[count][1]

    def init_character_text(self):
        self.font_image = self.font.render(self.character_name,True,(255,255,255),None)
        self.font_rect = self.font_image.get_rect()
        self.font_rect.right = self.background_rect.right - 15
        self.font_rect.bottom = self.background_rect.bottom - 10

    def init_portraits(self):
        self.portrait = pygame.image.load("Portraits/{}.png".format(
            self.image_path)).convert()
        self.portrait.set_colorkey((255,0,255))
        self.portrait_rect = self.portrait.get_rect()
        self.portrait_rect.centery = self.background_rect.centery
        self.portrait_rect.centerx = (self.background_rect.centerx - (
            int(self.portrait_side)*(self.background_rect.right - self.background_rect.centerx + 75))
            )
        if int(self.portrait_side) == -1:
            self.portrait = pygame.transform.flip(self.portrait, True, False)

    def draw(self):
        if self.Ctrl_Vars.box_count < len(self.dialog):
            self.Screen.blit(self.background_image, self.background_rect)
            self.Screen.blit(self.font_image, self.font_rect)
            self.text_scroll()
            self.Screen.blit(self.portrait, self.portrait_rect)

    def text_scroll(self):
        x = self.dialog_x
        y = self.dialog_y
        for line in self.box:
            for word in line:
                word.draw(self.Screen,(x,y))
                if word.full == False:
                    break
                x += word.font_rect.right
            if not line[-1].full:
                break
            y += word.font_rect.bottom
            x = self.dialog_x
        
#When worlds become sufficiently large this will be necessary but it would need to be accompanied by rendering function and would require defined space
"""TODO:    def translate(self,x,y):
        for col in range(len(self.World.Terrain)):
            for row in range(len(self.World.Terrain[col])):
                self.World.Terrain[-1-col][row].image_rect.centerx += x / self.scaling_factor
                self.World.Terrain[-1-col][row].image_rect.bottom += y / self.scaling_factor"""

#Planned UI elements
"""TODO: class Terrain_info():
    def __init__(self,Screen):
        self.Screen = Screen

#Right
class Currancy_bar():
    def __init__(self,Screen):
        self.Screen = Screen

class Target_Tile_Display():
    def __init__(self,Screen):
            self.Screen = Screen"""

"""#Bottom
class Time_Weather():
    def __init__(self,Screen):
        self.Screen = Screen

class Weapons_Menu():
    def __init__(self,Screen):
        self.Screen = Screen"""