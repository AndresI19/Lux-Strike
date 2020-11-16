#Generation
import math
import RNG as rng
from pygame import display
import numpy
import random
import sys
from Tessellation import Hex_Grid
sys.setrecursionlimit(3000)
limit = sys.getrecursionlimit()

def fill(HG,coords):
    """fills parametric outline to create solid map, by creating list of all tiles in a row and filling all
    empty blocks between the min and max"""
    def check(coords):
        #check
        if coords != False:
            col, row = coords
            tile = HG.data(col,row)
            if tile.ID != 1:
                tile.ID = 1
                tile.elevation = 1
                recursive_fill(coords)

    def recursive_fill(coords):
        Next = HG.get_N(coords)
        check(Next)
        Next = HG.get_NW(coords)
        check(Next)
        Next = HG.get_SW(coords)
        check(Next)
        Next = HG.get_S(coords)
        check(Next)
        Next = HG.get_SE(coords)
        check(Next)
        Next = HG.get_NE(coords)
        check(Next)

    #fill grid shape
    col,row = coords
    col = int(round(col/90))
    row = int(round(row/26))
    coords = [col,row]
    recursive_fill(coords)

class generation():
    def __init__(self,Seed,Max_parameters,Loading):
        #Seed for world gen!
        if Seed == None:
            self.seed = rng.generate_Xdegit_seed(18)
        else:
            self.seed = Seed
        #set size parameters from arguments
        self.Max_Params = Max_parameters
        #set max height 
        self.total_tiers = rng.seed_random_bound_int(
            self.seed, (3,6), 0)

        #start -----------
        self.center = [0,0]
        self.Loading = Loading
        N = self.total_tiers * 700
        self.Loading.set_steps(N)
        self.generate_master_grid()
        #------------------

    def generate_master_grid(self):
        def base_grid():
            HG = Hex_Grid(Cols,Rows)
            for col in range(Cols):
                for row in range(Rows):
                    hexagon = Hexagon(col,row)
                    HG.write(hexagon,col,row)
            return HG

        def create_base_terrain():
            seed = rng.generate_seed_from_seed(self.seed,tier)
            parametric = create_parametric(seed,self.Max_Params,tier,self.center)
            for point in parametric:
                for i in range(len(HG)):
                    x,y = point
                    HG[i].check_contained(x,y)
                self.Loading.Update()

        def condence_tiers():
            for col in range(Cols):
                for row in range(Rows):
                    SUM = 0
                    tile = MSTR_Grid.data(col,row)
                    for tier in range(len(Grids)):
                        if Grids[0].data(col,row).ID == 1:
                            tile.ID = 1
                            SUM += Grids[tier].data(col,row).elevation
                    if SUM > 0:
                        tile.elevation = SUM -1
                    else:
                        tile.elevation = SUM
            return MSTR_Grid

        Cols,Rows = self.Max_Params
        Grids = []
        for tier in range(self.total_tiers):
            if not tier == 0:
                HG = base_grid()
                create_base_terrain()
                fill(HG,self.center)
                Grids.append(HG)
        MSTR_Grid = base_grid()
        condence_tiers()
        self.MSTR_Grid = MSTR_Grid

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
        self.grid.num_cols
        self.grid.num_rows
        self.create_stairs()
        self.set_all_cliffs()

    def create_stairs(self):
        def build(coords,ID,elevation):
            if coords != False:
                Ncol,Nrow = coords
                self.grid.data(Ncol,Nrow).ID = ID
                self.grid.data(Ncol,Nrow).elevation = elevation

        #Create Stairs()
        col = rng.seed_random_bound_int(
            self.seed, (3,self.grid.num_cols-3), 2)
        row = rng.seed_random_bound_int(
            self.seed, (2,self.grid.num_rows-4), 3)

        Points = self.grid.get_circle(col,row)

        self.stairs = [col,row]
        self.door = self.grid.get_S(self.stairs)

        elevation = self.grid.data(col,row-2).elevation
        wall_elevation = elevation + 2
        for point in Points:
            COL,ROW = point
            build([COL,ROW],100,wall_elevation)

        build(self.stairs,101,elevation)
        build(self.door,102,wall_elevation)

    def Rel_Edit(self,coordinates,ID,elevation):
        col = self.stairs[0] + coordinates[0]
        row = self.stairs[1] + coordinates[1]
        self.grid.data(col,row).ID = ID
        self.grid.data(col,row).elevation = elevation

    def set_all_cliffs(self):
        def left_cliff():
            DE = tile.elevation + 1
            Rcoords = self.grid.get_SW(coords)
            if Rcoords != False:
                Rtile = self.grid.data(Rcoords[0],Rcoords[1])
                DE =  tile.elevation - Rtile.elevation
                if DE < 0:
                    DE = 0
            tile.cliffs.append(DE)

        def center_cliff():
            DE = tile.elevation + 1
            Rcoords = self.grid.get_S(coords)
            if Rcoords != False:
                Rtile = self.grid.data(Rcoords[0],Rcoords[1])
                DE = tile.elevation - Rtile.elevation
                if DE < 0:
                    DE = 0
            tile.cliffs.append(DE)

        def right_cliff():
            DE = tile.elevation + 1
            Rcoords = self.grid.get_SE(coords)
            if Rcoords != False:
                Rtile = self.grid.data(Rcoords[0],Rcoords[1])
                DE = tile.elevation - Rtile.elevation
                if DE < 0:
                    DE = 0
            tile.cliffs.append(DE)

        for row in range(self.grid.num_rows):
            for col in range(self.grid.num_cols):
                tile = self.grid.data(col,-1-row)
                coords = [tile.col,tile.row]
                left_cliff()
                center_cliff()
                right_cliff()

class Hexagon():
    #perfect hexagon class, use as a means to derive a map
    def __init__(self,col,row,ID=None,elevation=None,cliffs=None):
        self.col = col
        self.row = row
        self.height = 52
        self.width = 60
        self.side_length = self.width/2
        self.offset = (self.side_length*(3/2))

        if ID == None:
            self.ID = 0
            self.elevation = 0
            self.cliffs = []

            self.position()
        else:
            self.ID = ID
            self.elevation = elevation
            self.cliffs = cliffs

    def position(self):
        self.bottom = self.row * (self.height / 2)
        self.top = self.height + self.bottom
        self.left = self.col * (self.width + self.side_length)
        if self.row%2 == 0:
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