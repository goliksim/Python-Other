#created by goliksim on 28 apr 2023

import numpy as np
from matplotlib import pyplot as plt
from shapely.geometry import  LineString

from geom_func import find_intersection, get_clean_points, plot_edges

def function(data, a, b, c, d):
    x = data[0]
    y = data[1]
    return (d - a * (x) - b* (y))/c 


def find_bier(prob, L_mar):
    L_bs = []
    for i in range(27):
        sum = 0
        for j in range(3):
            sum += L_mar[j, i]*prob[j]
        L_bs.append(sum)

    baer_risk = L_bs[np.argmin(L_bs)]
    index = np.argmin(L_bs)
    return baer_risk, index

def task3(prob, L_mar, bad_prob,random_risk, adjacencies ):
    L_bs = []
    for i in range(27):
        sum = 0
        for j in range(3):
            sum += L_mar[j, i]*prob[j]
        L_bs.append(sum)

    baer_risk, index = find_bier(prob, L_mar)
    index = np.argmin(L_bs)
    print(f"По Байесу c* = {baer_risk} для стратегии x{index+1}")


    fig3 = plt.figure()
    ax = fig3.add_subplot(111, projection="3d")
    ax.scatter(L_mar[0,np.argmin(L_bs)], L_mar[1,np.argmin(L_bs)],L_mar[2,np.argmin(L_bs)], c = 'r', s = 50)
    ax.scatter(L_mar[0,0:index], L_mar[1,0:index],L_mar[2,0:index], c = 'c') # выведем все точки
    ax.scatter(L_mar[0,index+1:], L_mar[1,index+1:],L_mar[2,index+1:], c = 'c') 
    ax.text(L_mar[0,np.argmin(L_bs)], L_mar[1,np.argmin(L_bs)],L_mar[2,np.argmin(L_bs)], f'cb={baer_risk}')
    ax.text(0, -2,2, f'r1θ1 + r2θ2 + r3θ3 = cb', c = 'g') 
    model_x_data = np.linspace(1, 4, 5)
    model_y_data = np.linspace(0, 6, 5)
    X, Y = np.meshgrid(model_x_data, model_y_data)
    Z = function(np.array([X, Y]), prob[0],prob[1],prob[2],baer_risk)
    ax.plot_surface(X, Y, Z, alpha=0.5, color = 'g')
    '''
    model_x_data = np.linspace(1, 8, 5)
    model_y_data = np.linspace(0, 8, 5)
    X, Y = np.meshgrid(model_x_data, model_y_data)
    Z = function(np.array([X, Y]), bad_prob[0],bad_prob[1],bad_prob[2],random_risk)
    ax.plot_surface(X, Y, Z, alpha=0.5, color = 'r')
    ax.set_zlim3d(0,7)

    margin_points = np.array([[x,y,z] for x,y,z in zip(L_mar[0,:],L_mar[1,:],L_mar[2,:])])
    plot_edges(adjacencies, ax, margin_points)
    ax.text(8, 5,2, f'Baes bad \n distr.', c = 'r') 
    '''
    
