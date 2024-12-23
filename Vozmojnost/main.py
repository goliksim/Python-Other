#created by goliksim on 27 apr 2023

import numpy as np
import matplotlib.pyplot as plt
from task1 import task1
from task2 import task2
from task3 import task3
from task4 import task4
from task5 import task5


if __name__ == "__main__":
    #points = np.array([[3,2,7,5,3,9],[1,4,4,5,1,9],[1,2,6,5,8,9]]).T # задаем матрицу рисков
    points = np.array([[1,3,4,6,7,9],[4,5,5,4,2,9],[7,6,2,5,3,9]]).T
    #points = np.array([[3,2,4,5,3,9],[3,3,6,5,2,9],[2,4,7,5,8,9]]).T # задаем матрицу рисков
    #points = np.array([[0,2,5,6,10],[3,4,3,2,10],[6,2,4,3,10]]).T

    task1(points)
    
    risks = points.T
    
    risks = np.array([[1,7,9],[4,2,9],[7,3,9]])
    #risks = np.array([[0,2,5,10],[3,4,3,10],[6,5,4,10]])
    #P = np.array([[0.3, 0.2, 0.2,0.15,0.1,0.05], [0.15,0.2,0.15,0.2,0.15,0.15], [0.05, 0.1,0.15,0.2,0.2,0.3]])
    #P = np.array([[0.65, 0.2, 0.15], [0.4, 0.5,0.1], [0.15, 0.15,0.7]])
    P = np.array([[0.45, 0.35, 0.2], [0.25, 0.5, 0.25], [0.15, 0.15, 0.7]])
    L_mar, strategy, random_risk, adjacencies = task2(risks,P)
     
    Tp = np.array([0.5,0.2,0.3])

    task4(L_mar.T)

    bad_prob, baes_risk = task5(L_mar,random_risk)
    print('Баесовский риск равен:' + "{:.2f}".format(baes_risk) + f"  для наименее благоприятного распределения - {bad_prob}")

    task3(Tp, L_mar, bad_prob,random_risk, adjacencies)

    plt.show()