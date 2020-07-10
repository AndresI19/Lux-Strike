from math import sqrt,sin,cos
import RNG as rng
from pygame import display

class Generation():
    def __init__(self,Seed,Max_parameters, map_size,Screen):
        #Seed for world gen!
        if type(Seed) == str:
            self.seed = Seed
        else:
            self.seed = rng.generate_Xdegit_seed(18)
        #set size parameters from arguments
        self.Max_Columns,self.Max_Rows = Max_parameters[0],Max_parameters[1]
        self.map_size_x,self.map_size_y = map_size[0],map_size[1]
        #set max height 
        self.total_tiers = rng.seed_random_bound_int(
            self.seed, (4,6), 0)
        #empty grid
        self.master_grid = self.build_grid()
        #create a list of variablesto use in parametric
        self.variables = [0 for i in range (16)]
        #size correction variables
        self.corrections = [(0,0),(0,0)]
        #number of iterations of the parametric function
        self.sample_size = 2500

        #experimental
        """self.Loading_screen = loading_screen(Screen,self.sample_size,self.total_tiers,
            self.Max_Rows,self.Max_Columns)"""
        #start -----------
        self.generate_master_grid()
        #------------------

    def generate_master_grid(self):
        Grids = []
        for tier in range(self.total_tiers):
            if not tier == 0:
                grid = self.build_grid()
                grid = self.build_terrain(grid,tier)
                grid = self.grid_fill_shape(grid)
                Grids.append(grid)
        self.condence_tiers(Grids)

###################################
    def build_terrain(self,grid,tier):
        seed = self.seed
        if tier >=1:
            seed = rng.generate_seed_from_seed(self.seed,tier)
        self.make_variable_list(seed)
        self.adjust_parametric(tier)
        grid = self.check_parametric_contained(grid)
        return grid

    def make_variable_list(self,seed):
        for i in range(len(self.variables)):
            self.variables[i] = rng.seed_random_bound_int(
                seed, (-8,8), i)

    def condence_tiers(self,Grids):
        for col in range(len(Grids[0])):
            for row in range(len(Grids[0][0])):
                SUM = 0

                tier = 0
                #Plains terrain
                for tier in range(len(Grids)):
                    if not Grids[0][col][row].ID == 0:
                        self.master_grid[col][row].ID = 1
                        SUM += Grids[tier][col][row].elevation
                self.master_grid[col][row].elevation = SUM

    def build_grid(self):
        grid = []
        for col in range(self.Max_Rows):
            grid.append([])
            for row in range(self.Max_Columns):
                hexagon = Hexagon(row,col)
                hexagon.position()
                grid[col].append(hexagon)
        return grid

    def adjust_parametric(self,tier):
        """iterates once on the parametric to find a maximum and minimum, 
        uses these parameters to determain scale of correctional factors"""
        number_samples = self.sample_size
        x_min = 0
        x_max = 0
        y_min = 0
        y_max = 0
        for i in range(number_samples):
            coordinates = self.parametric(number_samples,i,False)
            if coordinates[0] < x_min:
                x_min = coordinates[0]
            if coordinates[1] < y_min:
                y_min = coordinates[1]
            if coordinates[0] > x_max:
                x_max = coordinates[0]
            if coordinates[1] > y_max:
                y_max = coordinates[1]

            #self.Loading_screen.Update()

        y_range = (y_max - y_min)
        x_range = (x_max - x_min)
        x_ratio = (self.map_size_x - tier*60*2)/x_range
        y_ratio = (self.map_size_y - tier*52*2)/y_range
        x_correction = abs(x_min)
        y_correction = abs(y_min)
        self.corrections = [x_ratio,y_ratio,x_correction,y_correction]

    def check_parametric_contained(self,grid):
        """most processor intensive function, this is the cause of long load_world screens. Needs to iterate as many times as there
        are tiles * samples, and this in iteself is done once per tier"""
        number_samples = self.sample_size
        for i in range(number_samples):
            coordinates = self.parametric(number_samples,i,True)
            for col in range(len(grid)):
                for row in range(len(grid[col])):
                    grid[col][row].check_contained(coordinates[0],coordinates[1])
                    #self.Loading_screen.Update()
        return grid

    def parametric(self,number_samples,i,corrected):
        """This is a line drawing function that works on the bases of periodic functions ie:
        sins and cosins. It is set to parameters made by the seed, and as long as each individual
        periodic function is set to end at a factor of 2 pi, there will be no spiral behavior.
        This parametric fucntion is used once to be adjusted to the size of the max map size, and then
        overlayed on the grid and checked for collsion."""
        r= 100
        x_margin = (3 * 90)
        y_margin = (6 * 26)
        pi = 3.1415
        t = (2*pi)*(i/number_samples)

        x = r*(
            self.variables[0]* cos(self.variables[1]*t)+
            self.variables[2]* cos(self.variables[3]*t) +
            self.variables[4]* sin(self.variables[5]*t) +
            self.variables[6]* sin(self.variables[7]*t) 
            )

        y = r*(
            self.variables[8]* sin(self.variables[9]*t)+
            self.variables[10]* sin(self.variables[11]*t) +
            self.variables[12]* cos(self.variables[13]*t) +
            self.variables[14]* cos(self.variables[15]*t) 
            )
        
        #Add corrections to resulting functions to scale to map size
        if corrected:
            x += self.corrections[2]
            y += self.corrections[3]
            x *= self.corrections[0]
            y *= self.corrections[1]
        x += x_margin
        y += y_margin
        return [x,y] 

    def grid_fill_shape(self,grid):
        """fills parametric outline to create solid map, by creating list of all tiles in a row and filling all
        empty blocks between the min and max"""
        for row in range(len(grid[0])):
            set1 = []
            set2 = []
            for col in range(len(grid)):
                if col%2 == 0:
                    if grid[col][row].ID == 1:
                        set1.append(col)
                if col%2 == 1:
                    if grid[col][row].ID == 1:
                        set2.append(col)
            grid = self.grid_fill_verticle(grid,row,set1)
            grid = self.grid_fill_verticle(grid,row,set2)
        return grid

    def grid_fill_verticle(self,grid,col,bounds):
        #fills one row
        if len(bounds) >= 2:
            fill_number = round((bounds[-1] - bounds[0])/2)
            for i in range(fill_number):
                row = (bounds[0]+i*2)
                grid[row][col].ID = 1
                grid[row][col].elevation = 1
        return grid

class Post_Generation():
    def __init__(self,grid,Seed):
        self.grid = grid
        self.seed = Seed
        self.Max_Columns = len(self.grid)
        self.Max_Rows = len(self.grid[0])
        self.create_stairs()
        
    def create_fortress(self):
        r = 1
        dy_max = (2*r + 1)
        dy_min = r + 1
        dx = 0
        self.build_radius(dy_min,dy_max,dx)

    def build_radius(self,dy_min,dy,dx):
        if dy < dy_min:
            return
        y = -dy + 1
        for i in range(dy):
            if dx == 0:
                self.rel_set_hex_id((dx,y),100)
                self.rel_set_hex_elevation((dx,y),self.wall_elevation)
            else:
                if self.stairs_off_center:
                    if dy%2 == 1:
                        x2 = -dx
                    else:
                        x2 = -(dx)+1
                    self.rel_set_hex_id((dx,y),100)
                    self.rel_set_hex_elevation((dx,y),self.wall_elevation)
                    self.rel_set_hex_id((x2,y),100)
                    self.rel_set_hex_elevation((x2,y),self.wall_elevation)
                else:
                    if dy%2 == 1:
                        x2 = dx
                    else:
                        x2 = dx-1
                    self.rel_set_hex_id((-dx,y),100)
                    self.rel_set_hex_elevation((-dx,y),self.wall_elevation)
                    self.rel_set_hex_id((x2,y),100)
                    self.rel_set_hex_elevation((x2,y),self.wall_elevation)
            y += 2
        dy -= 1
        if dy%2 ==0:
            dx += 1
        self.build_radius(dy_min,dy,dx)

    def rel_set_hex_id(self,coordinates,ID):
        x = self.stairs[0] + coordinates[1]
        y = self.stairs[1] + coordinates[0]
        self.grid[x][y].ID = ID

    def rel_set_hex_elevation(self,coordinates,elevation):
        x = self.stairs[0] + coordinates[1]
        y = self.stairs[1] + coordinates[0]
        self.grid[x][y].elevation = elevation

    def create_stairs(self):
        #column
        x = rng.seed_random_bound_int(
            self.seed, (3,self.Max_Columns-3), 2)
        #row
        y = rng.seed_random_bound_int(
            self.seed, (2,self.Max_Rows-2), 3)

        print("x : {}, y: {}".format(x,y))

        self.stairs = [x,y]
        self.door = [x,y-2]

        self.elevation = self.grid[x][y-2].elevation
        self.wall_elevation = self.elevation + 2

        self.stairs_off_center = self.grid[x][y].off_center
        self.create_fortress()


        self.grid[x][y].elevation = self.elevation
        self.grid[x][y].ID = 101
        self.grid[x-2][y].elevation = self.elevation

class Hexagon():
    #perfect hexagon class, use as a means to derive a map
    def __init__(self,row,col):
        self.row = row
        self.col = col
        self.height = 52
        self.width = 60
        self.side_length = self.width/2
        self.offset = (self.side_length*(3/2))

        self.bottom = 0
        self.top = 0
        self.center_y = 0
        self.left = 0

        self.off_center = False
        self.position()

        self.ID = 0
        self.elevation = 0

        self.water = True

    def position(self):
        self.bottom = self.col * (self.height / 2)
        self.top = self.height + self.bottom
        self.left = self.row * (self.width + self.side_length)
        if self.col%2 == 0:
            self.left += self.offset
            self.off_center = True
        self.center_y = self.height/2 + self.bottom

    def check_contained(self,x,y):
        if y >= self.bottom and y <= self.top:
            slope = 1/sqrt(3)
            if y - self.center_y >= 0:
                slope *= -1

            y_rel = self.center_y - y
            left_bound = self.left + (y_rel)*slope
            right_bound = self.left + self.width - (y_rel)*slope

            if x >= left_bound and x <= right_bound:
                self.ID = 1
                self.elevation = 1
