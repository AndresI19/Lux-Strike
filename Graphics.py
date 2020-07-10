from pygame import display,Surface

#graphics master loops vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
#main game
def Display(Screen,World,HUD,Player,Enemies):
    Screen.fill((0,0,0))
    World.Background(0) #0
    Enemies.Draw()
    Player.Draw()
    World.Background(1) #1
    HUD.draw()
    display.flip()

#Menu displays
def Menu_diplay(Menu):
    Menu.draw()
    display.flip()

#graphics master loops ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

""" TODO: FIXME: #Loading Screen object
class load_world_screen():
    def __init__(self,Screen,sample_size,total_tiers,Max_Rows,Max_Columns):
        #loading screen variables
        self.Screen = Screen
        self.screen_rect = self.Screen.get_rect()
        self.bar_size = self.screen_rect.width * (9/10)
        self.frames = (sample_size*total_tiers + sample_size*total_tiers*Max_Columns*Max_Rows)
        self.increment = float(self.bar_size/self.frames)
        self.count = 0
        self.bar_left = self.screen_rect.width/20
        self.bar_bottom = self.screen_rect.bottom * (9/10)
        self.bar = Surface(
            (1,15)  )
        self.bar.fill((255,0,0))

    def Update(self):
        self.bar_left += 1
        self.Screen.blit(self.bar,(self.bar_left,self.bar_bottom))
        display.flip()"""
