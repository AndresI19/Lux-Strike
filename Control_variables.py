#class for player input variables; ei knowing the mouse is down or what menu is on
class Ctrl_Vars():
    def __init__(self):
        self.menu_var_init()
        self.timer_init()
        self.set_button_downs()
        self.initialized = False #memory used to know if game objects have already been loaded and dont need to be re initialized

        self.box_count = 0

        self.camera_follow = True
        self.foreground_list = [0,0] #to rework and delete
        self.seed = "" #this is a 'soft' version of the seed, it is not used as the seed unless the player indicates so.
##Dynamic game stats
        self.wallet = 0
        self.keys = 1
#Key Controls _____________________________________________
#HOLD KEYS____________________________________________________________
        self.Left_MouseDown = False
        self.LSHIFT_DOWN = False
        self.L_click_memory = False
        self.Left_click = False
        self.Right_MouseDown = False

    def set_button_downs(self):
        self.q_down = False
        self.w_down = False
        self.e_down = False
        self.a_down = False
        self.s_down = False
        self.d_down = False

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
#Menu Controls_______________________________________________
    def menu_var_init(self):
        #initialize all menu switch bools
        self.Game_active = True #True win playing game, false if in menu
        self.menu_select = False
        #menus
        self.Pause = False
        self.Start_Screen = False
        self.Game_Win = False
        self.Game_Over = False
        self.seed_menu = False 
        self.load_world = False #the bool called to load a new world

        #World building Instructions
        self.restart_world = False
        self.Random = False
        self.set_seed = False
#Clocks ______________________________________________________________
    def timer_init(self):
        #Turn timer variables
        self.Turn_Frames = 60
        self.turn_frame = 0
        self.TURN_PLAYER = True
        self.TURN_ENEMY = False
    
        self.phase_frame = 0
        self.phase_Frames = 4 #set to 2 for no animation frames
        self.phase_active = False

    def switch_turns(self):
        #simple flip flop function for swtiching player/AI turns
        if self.TURN_PLAYER:
            self.TURN_PLAYER = False
            self.TURN_ENEMY = True
        elif self.TURN_ENEMY:
            self.TURN_PLAYER = True
            self.TURN_ENEMY = False     
        self.turn_frame = 0

    def merge_timer(self):
        if self.phase_active:
            if self.phase_frame + 1 >= self.phase_Frames:
                self.end_phase()
            else:
                self.phase_frame += 1
        else:
            if self.turn_frame + 1 >= self.Turn_Frames:
                self.end_turn()
            else:
                self.turn_frame += 1

    def end_phase(self):
        self.phase_frame = 0
        self.phase_active = False
        self.switch_turns()

    def end_turn(self):
        self.turn_frame = 0
        self.phase_active = True            