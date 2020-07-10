import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
from math import sqrt

"""# Prepare arrays x, y, z
theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
z = np.linspace(-2, 2, 100)
r = z**2 + 1
x = r * np.sin(theta)
y = r * np.cos(theta)"""


def generate_list():
    for i in range(num_variables):
        var.append(
            random.randint(-7,7)
        )

def generate_plot(r,adjustment):
    x = r*(
        var[0]* np.cos(var[1]*theta)+
        var[2]* np.cos(var[3]*theta) +
        var[4]* np.sin(var[5]*theta) +
        var[6]* np.sin(var[7]*theta)
        )

    y = r*(
        var[8]* np.sin(var[9]*theta)+
        var[10]* np.sin(var[11]*theta) +
        var[12]* np.cos(var[13]*theta) +
        var[14]* np.cos(var[15]*theta)
        )

    ax.plot(x, y, z, label='parametric curve')
    if adjustment == False:
        axes = plt.gca()

        y_min, y_max = axes.get_ylim()
        x_min, x_max = axes.get_xlim()

        y_range = y_max - y_min
        x_range = x_max - y_min
        area = x_range * y_range

        r = sqrt(max_area/area) * r

        return r
    else:
        axes = plt.gca()
        y_min, y_max = axes.get_ylim()
        x_min, x_max = axes.get_xlim()

        y -= y_min
        x -= x_min

        ax.plot(x, y, z, label='parametric curve')



####################
plt.rcParams['legend.fontsize'] = 10
fig = plt.figure()
ax = fig.gca(projection='3d')
theta = np.linspace(0, 2 * np.pi, 100)
z=0
r = 1
max_area = 1000
marginal_area = 101
var = []
num_variables = 16

generate_list()
r = generate_plot(r,False)
generate_plot(r,True)
plt.show()