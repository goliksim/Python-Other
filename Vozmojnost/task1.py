#created by goliksim on 27 apr 2023

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from shapely.geometry import  LineString

from geom_func import find_random_square, get_clean_points, find_intersection, plot_edges, plot_projection

def plot_settings(ax):

    ax.set_xlim3d(0,10)
    ax.set_ylim3d(0,10)
    ax.set_zlim3d(0,10)

    ax.set_xlabel("θ1")
    ax.set_ylabel("θ2")
    ax.set_zlabel("θ3")

def task1(points):
    min_max_risk = points.max(axis=1).min() # min_max_risk = 3
    action_index = np.where(points == min_max_risk)[0][0] # action_index = 0

    print(f"Минмакс риск: {min_max_risk} для действия d{action_index+1}. {points[action_index]}")

    clean_points, adjacencies = get_clean_points(points) #получим индексы чистых действий
    intersections = find_intersection(clean_points, points, adjacencies,LineString([[0,0,0],[10,10,10]])) #найдем пересечения биссектрисы с выпуклой оболочкой
    print(f"Рандомизированный риск: "+ "{:.2f}".format(intersections[0][0]))
    
    fig1 = plt.figure()
    ax = fig1.add_subplot(111, projection="3d")
    
    find_random_square(points, ax,min_max_risk)

    ax.scatter(points[0:,0],points[:,1],points[:,2]) # выведем все точки
    plot_edges(adjacencies,ax, points) # построим и выведем выпуклую оболочку
    ax.plot([0,10],[0,10],[0,10]) # построим биссектрису
    ax.scatter(intersections[:,0],intersections[:,1],intersections[:,2], c = 'r') # выведем точки пересечения
    plot_settings(ax)
    plot_projection(ax,intersections,0)