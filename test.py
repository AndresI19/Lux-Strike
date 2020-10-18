import numpy
import pylab as plt
import math
import random

"""In computer graphics, centripetal Catmull–Rom spline is a variant form of Catmull-Rom spline, 
originally formulated by Edwin Catmull and Raphael Rom, which can be evaluated using a recursive algorithm 
proposed by Barry and Goldman. It is a type of interpolating spline (a curve that goes through its control points) 
defined by four control points P0,P1,P2,P3 with the curve drawn only from P1 to P2."""

def generate_points(DF,N=3):
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
        for mid_line in grid:
            top_bound = round(mid_line + split)
            bottom_bound = round(mid_line - split)
            angle = random.randint(bottom_bound,top_bound)
            angles.append(angle)
        return angles
    def convert_to_radians(angles):
        for i in range(len(angles)):
            angles[i] = (angles[i] * math.pi)/180
        return angles
    def radial_values(DF,angles):
        point_list = []
        for i in range(len(angles)):
            radius = random.randint(100,(DF*100))/100
            point_list.append([angles[i], radius])
        return point_list
    
    grid = make_grid_lines(N)
    angles = create_angles(N,grid)
    angles = convert_to_radians(angles)
    point_list = radial_values(DF,angles)
    return point_list

def polar_to_cartisian(points):
    for i in range(len(points)):
        angle, radius = points[i]
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        points[i] = [x,y]
    
def CatmullRomSpline(P0, P1, P2, P3, nPoints=25):
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

def CatmullRomChain(P):
    """
    Calculate Catmull–Rom for a chain of points and return the combined curve.
    """
    sz = len(P)

    # The curve C will contain an array of (x, y) points.
    C = []
    for i in range(sz):
        c = CatmullRomSpline(P[i-3], P[i-2], P[i-1], P[i])
        C.extend(c)
    return C

def Q1_scale(curve,MaxParams = [1,1]):
    #scales and puts into first quadrent
    Mx, My = MaxParams
    x,y = zip(*curve)
    minX,minY = min(x),min(y)
    
    RatioX = Mx/(max(x) - minX)
    RatioY = My/(max(y) - minY)
    for i in range(len(curve)):
        curve[i] = [RatioX * (x[i] - minX),
            RatioY * (y[i] - minY)]

N = 8
DF = 20
polar_coords = point_list(DF,N)
polar_to_cartisian(polar_coords)

# Calculate the Catmull-Rom splines through the points
c = CatmullRomChain(polar_coords)
Q1_scale(c,[1000,1000])
print(len(c))
# Convert the Catmull-Rom curve points into x and y arrays and plot
x, y = zip(*c)
plt.plot(x,y,'o')
plt.show()