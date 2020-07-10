#class for player input variables; ei knowing the mouse is down or what menu is on
class Ctrl_Vars():
    def __init__(self):
        self.menu_var_init()
        self.timer_init()

        self.Left_MouseDown = False
        self.L_click_memory = False
        self.Left_click = False
        self.Right_MouseDown = False
        
        self.camera_follow = True
        self.foreground_list = [0,0] #to rework and delete
        self.seed = "" #this is a 'soft' version of the seed, it is not used as the seed unless the player indicates so.

    def timer_init(self):
        #Turn timer variables
        self.Turn_Frames = 60
        self.turn_frame = 0
        self.TURN_PLAYER = True
        self.TURN_ENEMY = False
    
    def menu_var_init(self):
        #initialize all menu switch bools
        self.Game_active = True #True win playing game, false if in menu
        #menus
        self.Pause = False
        self.Start_Screen = False
        self.Game_Win = False
        self.Game_Over = False
        self.seed_menu = False 

        #World building Instructions
        self.load_world = False #the bool called to load a new world
        self.initialized = False #memory used to know if game objects have already been loaded and dont need to be re initialized
        self.restart_world = False
        self.Random = False
        self.set_seed = False
    
    def turn_timer(self):
        """simple reset timer for how long the player and enemy has to act.
        Action time is usually shorter since a aplayer input maksea new turn"""
        if self.turn_frame + 1 >= self.Turn_Frames:
            self.switch_turns()
        else:
            self.turn_frame += 1

    def switch_turns(self):
        #simple flip flop function for swtiching player/AI turns
        if self.TURN_PLAYER:
            self.TURN_PLAYER = False
            self.TURN_ENEMY = True
        elif self.TURN_ENEMY:
            self.TURN_PLAYER = True
            self.TURN_ENEMY = False     
        self.turn_frame = 0 

    def mouse_down_update(self):
        #Fucntional way to know and act on the exact frame the mouse was clicked. Probably a better way to do this.
        if self.Left_MouseDown:
            if not self.L_click_memory:
                self.Left_click = True
                self.L_click_memory = True
            else:
                self.Left_click = False
        else:
            self.L_click_memory = False      
                 