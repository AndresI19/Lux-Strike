import Tile as T
import random
import Tessellation
import RNG as rng
from Generation import generation,Post_Generation,Hexagon

#World Object!
"""This is the most big baby mamma of all the objects! This object will contain a grid of every tile object int he world,
and each tile contains its individual properties. The World starts with size parameters that determain the size of the map, 
and by association the world generation time. A genertaion object is used to create a world case by case, so reinitializing this object
hence creates a new world."""
class World():
    def __init__(self,Screen,Seed,Loading,DATA = None):
        self.Screen = Screen
        self.highlighted_list = []
        self.laser_list = []
        self.Doors = []
        if DATA == None:
            #Size Parameters
            self.num_cols = 18   #width
            self.num_rows = 35   #height

            #Tile list
            self.Map = Tessellation.Hex_Grid(self.num_cols,self.num_rows)
            #Spawn location
            self.spawn_col = 0
            self.spawn_row = 0

            self.generate_map(Seed,Loading)
            self.find_player_spawn()
        else:
            Matrix = DATA['Map']['Matrix']
            self.num_cols = len(Matrix)
            self.num_rows = len(Matrix[0])
            self.master_grid = Tessellation.Hex_Grid(self.num_cols,self.num_rows)
            self.Map = Tessellation.Hex_Grid(self.num_cols,self.num_rows)
            for col in range(self.num_cols):
                for row in range(self.num_rows):
                    ID,Elevation,Cliffs = Matrix[col][row]
                    tile = Hexagon(col,row,ID,Elevation,Cliffs)
                    self.master_grid.Matrix[col][row] = tile
            self.spawn_col,self.spawn_row = DATA['Map']['spawn']
            self.transcribe_grid()
            #TODO: Seed should be the world name
            self.seed = self.seed = rng.generate_Xdegit_seed(18)
            
###MAP GENERATION/ INITIALIZATION vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    def generate_map(self,Seed,Loading):
        #initialize generation object, creates a new world --------------------------------------
        max_parameters = [self.num_cols,self.num_rows]
        Generation = generation(Seed,max_parameters,Loading)
        #save seed for display and copy paste use
        self.seed = Generation.seed
        self.total_tiers = Generation.total_tiers

        post_generation = Post_Generation(Generation.MSTR_Grid,self.seed)

        #create world using matrix information ---------------------------------------------------
        self.master_grid = post_generation.grid
        self.transcribe_grid()

    def transcribe_grid(self):
        def special_case(key):
            if key == 101:
                self.stairs = [col,row]
            if key == 102:
                self.Doors.append(tile)
        #converts grid into tiles
        ID_Converter = T.TileClass()
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                elevation = self.master_grid.data(col,row).elevation
                ID = self.master_grid.data(col,row).ID
                cliffs = self.master_grid.data(col,row).cliffs
                for key in ID_Converter:
                    if ID == key:
                        tile = ID_Converter[key](self.Screen,col,row,cliffs,elevation)
                        special_case(key)
                self.Map.write(tile,col,row)

    def find_player_spawn(self):
        #what it says it does
        """simply worlds by finding the first sea level land going left to right, down to up. if it fails,
        plays just spawns in the corner"""
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.master_grid.data(col,row).ID == 1:
                    self.spawn_col = col
                    self.spawn_row = row
                    return

##Checks vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    def check_bounds(self,col,row):
        BX = col < self.num_cols and col > -1
        BY = row < self.num_rows and row > -1
        if BX and BY:
            return False
        else:
            return True

    def check_cliff(self,MOB,col,row):
        if isinstance(self.Map.data(col,row), T.Water):
            return False
        else:
            current_elevation = self.Map.data(MOB.col,MOB.row).elevation
            projected_elevation = self.Map.data(col,row).elevation
            cliff_height = projected_elevation - current_elevation
            if cliff_height <= 1 and cliff_height >= -2:
                return False
            else:
                return True

    def check_doors(self,MOB,col,row):
        for door in self.Doors:
            if door.col == col and door.row == row:
                if MOB.Stats.keys > 0:
                    MOB.Stats.keys -= 1
                    door.Open(self)
                    return True
        else:
            return False

##Standard Functionalities
    def translate(self,dx,dy):
        #move every element in the world
        for i in range(len(self.Map)):
            self.Map[i].translate(dx,dy)
        
    def reset_highlight(self):
        for i in range(len(self.highlighted_list)):
            col,row = self.highlighted_list[i]
            self.Map.data(col,row).highlighted = False
        self.highlighted_list = []
#-------------------------------------------------------------------------------------------------------------------#