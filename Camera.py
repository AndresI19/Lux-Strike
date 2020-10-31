#CAMERA!
class Camera():
    def __init__(self,World,Player,Enemies,Drops):
        self.World = World
        self.Player = Player
        self.Enemies = Enemies
        self.Drops = Drops

        self.follow = True

        self.increment = []
        self.frames = 0
        self.count = 0
        self.Center_Screen()

    def View(self,Ctrl_Vars):
        if self.follow:
            self.Center_Screen()
        else:
            self.read_pan()
        if self.Player.hitstun:
            self.Camera_shake(4,Ctrl_Vars.phase_frame)

    def Translate_Screen(self,coordinates):
        dx = coordinates[0]
        dy = coordinates[1]
        self.World.translate(dx,dy)
        self.Player.translate(dx,dy)
        self.Enemies.translate(dx,dy)
        self.Drops.translate(dx,dy)

    def Center_Screen(self,center = [960,440]):
        xf,yf = center
        xi = self.Player.MOB_rect.centerx
        yi = self.Player.MOB_rect.centery
        dx = xf - xi
        dy = yf - yi
        self.Translate_Screen((dx,dy))

    def set_pan(self,frames,Subject = None,Center = [960,440]):
        if Subject == None:
            #defualt subject is the player
            xi = self.Player.MOB_rect.centerx
            yi = self.Player.MOB_rect.centery
        else:
            xi = Subject[0]
            yi = Subject[1]
        xf,yf = Center
        inc_x = (xf - xi)//frames
        inc_y = (yf - yi)//frames
        self.frames = frames
        self.increment = [inc_x,inc_y]

    def read_pan(self):
        if self.frames != 0:
            if self.count + 1 <= self.frames:
                self.count += 1
                self.Translate_Screen(self.increment)
            else:
                self.count = 0
                self.frames = 0
                self.follow = True

    def Camera_shake(self,degree,frame):
        if frame%2 == 0:
            x = degree
        elif frame%2 == 1:
            x = -1*degree
        self.Translate_Screen((x,0))