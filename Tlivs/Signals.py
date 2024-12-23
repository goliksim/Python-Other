import numpy as np
from matplotlib import pyplot as plt

def meander_in(T, count):
    signal = []
    for i in range(count):
        signal+= [1] * (T//2)  + [0] * (T//2)
        
    return signal

def rectang_in(T, count):
    signal = []
    for i in range(count):
        signal+= [1] * (T//2)  + [0] * (T)
        
    return signal

def triang_in(x,count):
    signal = []
    T = x[-1]/count
    signal += [1-4*i/T for i in x[0:int(len(x)/2/(x[-1]/T))+1]]
    #signal+=[-1]*(len(x)//int(T)//4)
    signal += signal[-2:0:-1]
    return (signal)*(count+1) + signal[0:1]

def sin_in(x,count):
    T=x[-1]/count
    return np.sin([i*2*np.pi/T for i in x])

def discSin_in(x,h,count):
    signal = []
    T=x[-1]/count
    disc_count = x[-1]/h
    step = int(len(x)//disc_count)
    for x in np.sin([i*2*np.pi/T for i in x][::step]):
        signal+= [0]*step + [x]
    return signal    

def quantSin_in(x,n,count):
    signal = []
    T=x[-1]/count
    #print(T)
    h=x[0]
    for i in x:
        #print(i,h)
        if i<=h:
            signal.append(np.sin(h*2*np.pi/T))
        else:
            signal.append(np.sin(h*2*np.pi/T))
            h+=T/n
    return signal

