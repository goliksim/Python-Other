import numpy as np

from task3 import find_bier
from tqdm import tqdm

def task5(L_mar, random_risk):
    X = np.linspace(0,1,2000)
    for x in tqdm(X):
        Y =  np.linspace(0,1-x,2000)
        for y in Y:
            z = 1-x-y
            prob = np.array([x,y,z])
            baer_risk, _ = find_bier(prob, L_mar)
            if abs(baer_risk-random_risk)<0.001:
                return prob, baer_risk
    return None
    
    