#created by goliksim on 27 apr 2023

import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import  LineString
from geom_func import find_random_square, get_clean_points, find_intersection, plot_edges, plot_projection



def pr(s, i, t, strategy, P):
  sum = 0
  for l in strategy[s][t]:
    sum += P[i, l-1]
  return sum

def get_mar(i, s, risks, ps):
  sum = 0
  for t in range(len(risks.T)):
    sum += risks[i, t]*ps[s, i, t]
  return sum

def create_strategy_combination(strategy,N):
    for k in range(N):
        for j in range(N):
            for l in range(N):
                temp = []
                for i in range(N):  
                  temp.append([])
                temp[k].append(1)
                temp[j].append(2)
                temp[l].append(3)
                strategy.append(temp)

def print_poss(strategy,p):
   for s in range(len(strategy)):
        text = "$x^{" + f"({s+1})" + "} = \{"  + f"{ ','.join([ 'x_' + f'{x}' for x in strategy[s][0] ])}" + "\}\cup\{" + f"{ ','.join([ 'x_' + f'{x}' for x in strategy[s][1] ])}" + "\}\cup\{" + f"{ ','.join([ 'x_' + f'{x}' for x in strategy[s][2] ])}" + "\}"
        text = text.replace("\{\}","\{\\emptyset\}") + '$ &'
        for i in range(3):
            for t in range(3):
                text+= f'{p[s, i, t]}' + ' & '
        text+='rrr'
        text = text.replace("& rrr","\\\\")
        text =text.replace('00000000000001','')
        text+= '\n' + '\hline'
        print(text )

def task2(risks,P):
    N = len(risks.T)
    S_num = N**3
    theta = len(risks)

    strategy = []
    create_strategy_combination(strategy,N)
 
    ps = np.ones((S_num, theta, N))
    for s in range(S_num):
        for i in range(theta):
            for t in range(N):
                ps[s, i, t] = pr(s, i, t, strategy, P)
    #print_poss(strategy,ps)  # - LATEX TABLE OUTPUT !!!
    L_mar = np.ones((theta, S_num))
    for i in range(theta):
        for s in range(S_num):
            L_mar[i, s] = get_mar(i, s, risks, ps)
            

    temp = []
    for s in range(S_num):
        temp.append(np.amax(L_mar[:, s]))
    min_max_marj = np.min(temp)
    print(f"Маргинальный минимаксный риск: " + "{:.2f}".format(min_max_marj) + f" для стратегии x{np.argmin(temp)+1}" )
    print(*ps[np.argmin(temp)])

    
    
    margin_points = np.array([[x,y,z] for x,y,z in zip(L_mar[0,:],L_mar[1,:],L_mar[2,:])])
    clean_points, adjacencies = get_clean_points(margin_points) #получим индексы чистых действий
    intersections = find_intersection(clean_points,margin_points, adjacencies,LineString([[0,0,0],[10,10,10]])) #найдем пересечения биссектрисы с выпуклой оболочкой
    
    
    
    
    fig2 = plt.figure()
    ax = fig2.add_subplot(111, projection="3d")

    random_risk = find_random_square(L_mar.T, ax,min_max_marj)

    ax.scatter(L_mar[0,:], L_mar[1,:],L_mar[2,:]) # выведем все точки
    ax.plot([L_mar[0,np.argmin(temp)],0], [L_mar[1,np.argmin(temp)],L_mar[1,np.argmin(temp)]],[L_mar[2,np.argmin(temp)],L_mar[2,np.argmin(temp)]], c= 'g')
    ax.text(0, L_mar[1,np.argmin(temp)],L_mar[2,np.argmin(temp)], "c={:.2f}".format(np.min(temp)))
    plot_edges(adjacencies,ax,margin_points) # построим и выведем выпуклую оболочку
    ax.plot([0,9],[0,9],[0,9]) # построим биссектрису
    
    try:
      print(f"Рандомизированный маржинальный риск: "+ "{:.2f}".format(intersections[0][0]))
      ax.scatter(intersections[:,0],intersections[:,1],intersections[:,2], c = 'r') # выведем точки пересечения
      plot_projection(ax,intersections,0)
    except:
       pass
    return L_mar, strategy, random_risk, adjacencies
   

