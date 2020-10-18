import math
import RNG as rng
from pygame import display
from Menus import load_world_screen as loading_screen
import numpy
import random
import sys
sys.setrecursionlimit(2000)
limit = sys.getrecursionlimit()

class Generation():
    def __init__(self,Seed,Max_parameters,Screen,Window,Settings):
        #Seed for world gen!
        if type(Seed) == str:
            self.seed = Seed
        else:
            self.seed = rng.generate_Xdegit_seed(18)
        #set size parameters from arguments
        self.Max_Params = Max_parameters
        #set max height 
        self.total_tiers = rng.seed_random_bound_int(
            self.seed, (3,6), 0)
        #number of iterations of the parametric function
        self.sample_size = 2500

        #experimental
        N = (self.sample_size * self.total_tiers)/2
        self.Loading_screen = loading_screen(Window,Screen,Settings,N)

        #start -----------
        self.center = [0,0]
        self.generate_master_grid()
        #------------------
    def check_off_center(self,x):
        if x%2 == 0:
            self.off_center = 1
        else:
            self.off_center = -1 

    def generate_master_grid(self):
        def base_grid():
            Max_Columns,Max_Rows = self.Max_Params
            grid = []
            for col in range(Max_Rows):
                grid.append([])
                for row in range(Max_Columns):
                    hexagon = Hexagon(row,col)
                    hexagon.position()
                    grid[col].append(hexagon)
            return grid
        def create_base_terrain(self,grid,tier):
            """seed = self.seed TODO: add seed random elements to entire function
            if tier >=1:
                seed = rng.generate_seed_from_seed(self.seed,tier)"""

            seed = rng.generate_seed_from_seed(self.seed,tier)
            parametric = create_parametric(seed,self.Max_Params,tier,self.center)
            grid = check_points_contained_in_grid(parametric,grid)
            return grid
        def condence_tiers(master_grid,Grids):
            for col in range(len(Grids[0])):
                for row in range(len(Grids[0][0])):
                    SUM = 0
                    tile = master_grid[col][row]
                    #Plains/Beach terrain
                    for tier in range(len(Grids)):
                        if Grids[0][col][row].ID == 1:
                            tile.ID = 1
                            SUM += Grids[tier][col][row].elevation
                    if SUM > 0:
                        tile.elevation = SUM -1
                    else:
                        tile.elevation = SUM 
            return master_grid
        def check_points_contained_in_grid(parametric,grid):
            """most processor intensive function, this is the cause of long load_world screens. Needs to iterate as many times as there
            are tiles * samples, and this in itself is done once per tier 
            TODO:make work through nearest neighbor"""
            for point in parametric:
                for col in range(len(grid)):
                    for row in range(len(grid[col])):
                        grid[col][row].check_contained(point[0],point[1])
            return grid

        Grids = []
        for tier in range(self.total_tiers):
            if not tier == 0:
                grid = base_grid()
                self.grid = create_base_terrain(self,grid,tier)
                self.grid_fill_shape()
                Grids.append(grid)
        master_grid = base_grid()
        self.master_grid = condence_tiers(master_grid,Grids)

    def grid_fill_shape(self):
        """fills parametric outline to create solid map, by creating list of all tiles in a row and filling all
        empty blocks between the min and max"""
        def recursive_fill(x,y):
            def rel_check(dx,dy):
                #rel check
                CX = x + dx
                CY = y + dy
                col_bound = CX >= 0 and CX < self.Max_Params[1]
                row_bound = CY >= 0 and CY < self.Max_Params[0]
                if row_bound and col_bound:
                    if self.grid[CX][CY].ID == 0:
                        self.grid[CX][CY].ID = 1
                        self.grid[CX][CY].elevation = 1
                    
                        recursive_fill(CX,CY)

            def check_NE():
                self.check_off_center(x)
                if self.off_center == -1:
                    rel_check(1,0)
                elif self.off_center == 1:
                    rel_check(1,1)
            def check_N():
                rel_check(2,0)
            def check_NW():
                self.check_off_center(x)
                if self.off_center == 1:
                    rel_check(1,0)
                elif self.off_center == -1:
                    rel_check(1,-1)
            def check_SW():
                self.check_off_center(x)
                if self.off_center == 1:
                    rel_check(-1,0)
                elif self.off_center == -1:
                    rel_check(-1,-1)
            def check_S():
                rel_check(-2,0)
            def check_SE():
                self.check_off_center(x)
                if self.off_center == 1:
                    rel_check(-1,1)
                elif self.off_center == -1:
                    rel_check(-1,0)
        
            #recursive fill
            check_S()
            check_SW()
            check_NE()
            check_N()
            check_NW()
            check_SE()

        #fill grid shape
        y,x = self.center
        x = int(round(x/26))
        y = int(round(y/90))
        #print("x: {}, y: {}".format(x,y))
        recursive_fill(x,y)

###################################
"""MATH.%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
def generate_control_points(seed = 0):
    if seed == 0:
        DF = 13
        N = 3
    else:
        DF = rng.seed_random_bound_int(seed, (10,20), 0)
        N = rng.seed_random_bound_int(seed, (4,12), 1)

    #DF = Degrees of freedom
    if N < 3:
        N = 3
    if DF < 1:
        DF= 1

    def make_grid_lines(N):
        grid_lines = []
        grid_line_angle = 0
        split = 360 / (N)
        for i in range(N):
            grid_lines.append(grid_line_angle)
            grid_line_angle += split
        return grid_lines
    def create_angles(N,grid):
        split = 360 / (2*N)
        angles = []
        instance = 1
        for mid_line in grid:
            instance += 1
            top_bound = round(mid_line + split)
            bottom_bound = round(mid_line - split)
            bounds = (bottom_bound,top_bound)
            angle = rng.seed_random_bound_int(seed, bounds, instance)
            angles.append(angle)
        return angles
    def convert_to_radians(angles):
        for i in range(len(angles)):
            angles[i] = (angles[i] * math.pi)/180
        return angles
    def radial_values(DF,angles):
        point_list = []
        instance = 0
        for i in range(len(angles)):
            bounds = (100,(DF*100))
            radius = rng.seed_random_bound_int(seed,bounds,instance)/100
            point_list.append([angles[i], radius])
            instance += 1
        return point_list
    
    grid = make_grid_lines(N)
    angles = create_angles(N,grid)
    angles = convert_to_radians(angles)
    Control_points = radial_values(DF,angles)
    return Control_points

def create_parametric(seed,Max_parameters,layer,center):
    def CatmullRomSpline(P0, P1, P2, P3, nPoints=35):
        """
        P0, P1, P2, and P3 should be (x,y) point pairs that define the Catmull-Rom spline.
        nPoints is the number of points to include in this curve segment. nPoints = 25 works good 
        for scaling up to 1000
        """
        # Convert the points to numpy so that we can do array multiplication
        P0, P1, P2, P3 = map(numpy.array, [P0, P1, P2, P3])

        # Parametric constant: 0.5 for the centripetal spline, 0.0 for the uniform spline, 1.0 for the chordal spline.
        alpha = 0.5
        # Premultiplied power constant for the following tj() function.
        alpha = alpha/2
        def tj(ti, Pi, Pj):
            xi, yi = Pi
            xj, yj = Pj
            return ((xj-xi)**2 + (yj-yi)**2)**alpha + ti

        # Calculate t0 to t4
        t0 = 0
        t1 = tj(t0, P0, P1)
        t2 = tj(t1, P1, P2)
        t3 = tj(t2, P2, P3)

        # Only calculate points between P1 and P2
        t = numpy.linspace(t1, t2, nPoints)

        # Reshape so that we can multiply by the points P0 to P3
        # and get a point for each value of t.
        t = t.reshape(len(t), 1)
        A1 = (t1-t)/(t1-t0)*P0 + (t-t0)/(t1-t0)*P1
        A2 = (t2-t)/(t2-t1)*P1 + (t-t1)/(t2-t1)*P2
        A3 = (t3-t)/(t3-t2)*P2 + (t-t2)/(t3-t2)*P3
        B1 = (t2-t)/(t2-t0)*A1 + (t-t0)/(t2-t0)*A2
        B2 = (t3-t)/(t3-t1)*A2 + (t-t1)/(t3-t1)*A3

        C = (t2-t)/(t2-t1)*B1 + (t-t1)/(t2-t1)*B2
        return C
    def CatmullRomChain(P,nPoints = 35):
        """
        Calculate Catmull–Rom for a chain of points and return the combined curve.
        """
        sz = len(P)

        # The curve C will contain an array of (x, y) points.
        C = []
        for i in range(sz):
            c = CatmullRomSpline(P[i-3], P[i-2], P[i-1], P[i],nPoints)
            C.extend(c)
        return C
    def polar_to_cartisian(points,N = 8,DF = 20):
        for i in range(len(points)):
            angle, radius = points[i]
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            points[i] = [x,y]
    def Q1_scale(curve,layer,center,MaxParams = [1,1]):
        #scales and puts into first quadrent
        Mx, My = MaxParams
        x,y = zip(*curve)
        minX,minY = min(x),min(y)
    
        margin_spaceX,margin_spaceY = 2*(layer*90),2*(layer*26)
        borders = [(margin_spaceX / 2),(margin_spaceY / 2)]
        Mx -= margin_spaceX
        My -= margin_spaceY

        RatioX = (Mx/(max(x) - minX))
        RatioY = (My/(max(y) - minY))
        for i in range(len(curve)):
            curve[i] = [RatioX * (x[i] - minX) + borders[0],
                RatioY * (y[i] - minY) + borders[1]]
        Q1X,Q1Y = -(minX* RatioX + borders[0]), -(minY* RatioY + borders[1])
        center[0] = Q1X
        center[1] = Q1Y
   
    polar_coords = generate_control_points(seed)
    polar_to_cartisian(polar_coords)
    # Calculate the Catmull-Rom splines through the points
    points = CatmullRomChain(polar_coords,45)
    MaxMapX, MapMaxY = Max_parameters
    MaxMapParams = [MaxMapX * 90, MapMaxY * 26]
    Q1_scale(points,layer,center,MaxMapParams)

    return points

class Post_Generation():
    def __init__(self,grid,Seed):
        self.grid = grid
        self.seed = Seed
        self.Max_Columns = len(self.grid)
        self.Max_Rows = len(self.grid[0])
        self.create_stairs()
        self.variables = []
        self.set_all_cliffs()
        
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

        self.stairs = [x,y]
        self.door = [x,y-2]

        self.elevation = self.grid[x][y-2].elevation
        self.wall_elevation = self.elevation + 2

        self.stairs_off_center = self.grid[x][y].off_center
        self.create_fortress()


        self.grid[x][y].elevation = self.elevation
        self.grid[x][y].ID = 101
        self.grid[x-2][y].elevation = self.elevation

    def set_all_cliffs(self):
        for col in range(self.Max_Columns):
            #subject_row = self.Max_Columns - col - 1
            for row in range(len(self.grid[col])):
                subject_tile = self.grid[-1-col][row]
                self.set_cliffs(subject_tile)

    def set_cliffs(self,subject_tile):
        #TODO: labeling of x and y are backwards for all these functions. should be functional, 
        # but not developer friendly
        def check_left_cliff(subject_tile):
            Ly = subject_tile.col - 1
            if subject_tile.off_center == 1:
                Lx = subject_tile.row
            else:
                Lx = subject_tile.row - 1
            Le = subject_tile.elevation + 1
            if Lx >= 0:
                if Ly >= 0:
                    Le = subject_tile.elevation - self.grid[Ly][Lx].elevation
                    if Le < 0:
                        Le = 0
            subject_tile.cliffs.append(Le)
        def check_center_cliff(subject_tile):
            Cy = subject_tile.col - 2
            Ce = 1 + subject_tile.elevation
            if Cy >= 0:
                Ce = subject_tile.elevation - self.grid[Cy][subject_tile.row].elevation
                if Ce < 0:
                    Ce = 0
            subject_tile.cliffs.append(Ce)
        def check_right_cliff(subject_tile):
            Ry = subject_tile.col - 1
            if subject_tile.off_center == 1:
                Rx = subject_tile.row + 1
            else:
                Rx = subject_tile.row
            Re = subject_tile.elevation + 1
            if Rx < self.Max_Rows:
                if Ry >= 0:
                    Re = subject_tile.elevation - self.grid[Ry][Rx].elevation
                    if Re < 0:
                        Re = 0                        
            subject_tile.cliffs.append(Re)

        check_left_cliff(subject_tile)
        check_center_cliff(subject_tile)
        check_right_cliff(subject_tile)

class Hexagon():
    #perfect hexagon class, use as a means to derive a map
    def __init__(self,row,col):
        self.row = row
        self.col = col
        self.height = 52
        self.width = 60
        self.side_length = self.width/2
        self.offset = (self.side_length*(3/2))

        self.off_center = False
        self.position()

        self.ID = 0
        self.elevation = 0
        self.cliffs = []

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
            slope = 1/math.sqrt(3)
            if y - self.center_y >= 0:
                slope *= -1

            y_rel = self.center_y - y
            left_bound = self.left + (y_rel)*slope
            right_bound = self.left + self.width - (y_rel)*slope

            if x >= left_bound and x <= right_bound:
                self.ID = 1
                self.elevation = 1