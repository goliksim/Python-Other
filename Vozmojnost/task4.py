#created by goliksim on 28 apr 2023

from matplotlib import pyplot as plt
import numpy as np
from shapely.geometry import  LineString

from geom_func import intersect3D_SegmentPlane

def function(data, L_mar):
    x = data[0]
    y = data[1]
    return L_mar[0]*x + L_mar[1]*y + L_mar[2]*(1-x-y)

def task4(L_mar):
    fig4 = plt.figure()
    ax = fig4.add_subplot(111, projection="3d")

    px, py = 0.5, 0.2
    line = LineString([[px,py,0],[px,py,10]])
    intersections = []
    
    for i in range(len(L_mar)):
        model_x_data = np.linspace(0, 1, 51)
        model_y_data = np.linspace(0, 1, 51)
        X, Y = np.meshgrid(model_x_data, model_y_data)
        for k in range(len(Y)): #так как вероятности в сумме не могут быть больше 1, нужно внести это условие
            for j in range(len(Y[0])):
                if len(Y[0])-k<j : Y[k,j] = Y[k-1,j]                   
        Z = function(np.array([X, Y]),L_mar[i])
        x_dots = [2,2,10]
        y_dots = [2,8,2]
        x = X[0][x_dots]
        y = Y.T[0][y_dots]
        dots = [np.array([x,y,z]) for x,y,z in zip(x,y,function(np.array([x,y]),L_mar[i]))]
        intersect = intersect3D_SegmentPlane(line, dots) 
        intersections.append(intersect[2])

        ax.plot_surface(X, Y, Z, alpha=0.3)
    print(f"При выборе pθ1, pθ2 = {px},{py} Баесово действие - x{np.argmin(intersections)+1}")
    ax.plot([px,px],[py,py],[0,intersections[np.argmin(intersections)]],c = 'g')
    ax.scatter(px,py,intersections[np.argmin(intersections)],c = 'g',s=50)
    ax.text(px,py,0,f"x{np.argmin(intersections)+1}")
    ax.plot([px,0],[py,py],[0,0], c = 'g', linestyle= ":")
    ax.plot([px,px],[py,0],[0,0], c = 'g', linestyle= ":")
    ax.set_ylabel("pθ2")
    ax.set_xlabel("pθ1")
    ax.set_zlabel("L")
    ax.set_zlim3d(0,10)

