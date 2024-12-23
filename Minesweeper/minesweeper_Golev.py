import time
import numpy as np    
from os import system, name
import itertools
import os
import sys

     #Размер поля
firstOpen = True
numMines = 5
fldS = 5
gameActive = False
menuText = np.array([
"Продолжить игру",
"Сохранить игру",
"Загрузить игру",
"Начать новую игру",
"Выйти"])
mines = np.zeros(shape=(fldS,fldS), dtype=int)
flags = np.zeros(shape=(fldS,fldS), dtype=bool)     #Массив для флажков
revealed = np.zeros(shape=(fldS,fldS), dtype=bool)  #Массив открытых ячеек
calcneared = np.zeros(shape=(fldS,fldS), dtype=int)

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
  
#Функция для ввода начальных параметров игры

#Функция проверки действий только в области игры   
def outBounds(x,y):                                  
    return x<0 or y<0 or x>=fldS or y>=fldS

#Функция подсчета мин вокруг точки 
def calcNear(x,y):                                 
    if(outBounds(x,y)): return 0
    i=0
    for offsetX, offsetY in itertools.product(range(-1,2),range(-1,2)):
        if (outBounds(offsetX+x, offsetY+y)): continue    
        i+=mines[offsetX+x][offsetY+y]
    return i

#Реверсивная функция открывания пустых ячеек 
def reveal(x,y):        
    global revealed
    global calcneared
    if(outBounds(x,y)): return
    if(revealed[x][y]): return
    revealed[x][y]=True
    calcneared[x][y]=calcNear(x,y)
    if(calcNear(x,y)!=0): return
    for i,j in itertools.product(range(-1,2),range(-1,2)):
       if (outBounds(i+x, j+y)): continue
       reveal(x+i,y+j)   

#Расстановка мин на места
def placeMines():
    global mines
    i=0
    while(i<numMines): #We don't want mines to overlap, so while loop
        x=int(np.random.randint(0,fldS))
        y=int(np.random.randint(0,fldS))
        if(mines[x][y]==1):continue
        mines[x][y]=1
        i+=1

#Очистка поля
def clearMines():
    global mines
    mines = np.zeros(shape=(fldS,fldS), dtype=int)

def cellSymbol(x,y):
    Symbol=" "
    if(revealed[x][y]):
        if(calcNear(x,y)>0):
            Symbol=calcNear(x,y)
        if(calcNear(x,y)==0):
            Symbol=" "
    else:
        if(flags[x][y]):
            Symbol="?"
        else: Symbol=str("▓")
    return str(Symbol)

def startInput():                                   
    while True:
        try:
            a = [int(x) for x in input("Введите размер поля и количество бомб (2 числа): ").split()]
            if len(a)<2:
                a.append(int(input()))
            if len(a)>2: continue
            if a[1]<1 or a[1]>a[0]**2 or a[0]<1 or a[0]>30 :
                print("Не хитрите!")
                continue
            return a
        except ValueError:
            print("Неверный формат ввода")
            pass
        
def Game():
    global flags, firstOpen, gameActive
    drawGame()
    #Цикл действует пока пользователь не введет команду правильно
    while True:                                          
        try:
            Input = input("Введите команду вида X Y Action: ")
            if str(Input)=="quit": return False
            y, x, Action = Input.split()
            x, y = int(x), int(y)
            x-=1
            y-=1
            break
        except ValueError:
            print("Неверный формат ввода")
            pass
    #Дейтвие Флажка
    #if (Action=="Quit"):
    #    return False
    if (Action=="flag"): 
        if(not revealed[x][y]): flags[x][y]=not flags[x][y] 
    if (Action=="open"):
        #Открыть
        #Избежание открытия мины первым ходом
        if (firstOpen):
            firstOpen=False
            while True:
                clearMines()
                placeMines() 
                if (calcNear(x,y)==0): break
        #Check for game loss
        if (mines[x][y]==0): 
            reveal(x, y)
            drawGame()
            
            if((fldS*fldS - np.sum(revealed, dtype=int))==np.sum(mines,dtype=int) and not firstOpen):
               print("\nПобеда!")
               print("Возвращение в меню!")
               gameActive = False
               time.sleep(5) # Сон в 3 секунды
               return False 
            return True
        else:
            print("\nВзрыв!")
            print("Возвращение в меню!")
            gameActive = False
            time.sleep(3) # Сон в 3 секунды
            return False 
    else:  
        return True
            
def drawGame():
    clear()
    sysStr="mode con cols=" +  str(100+fldS*5) +" lines=" + str(50+fldS*5)
    os.system(sysStr)
    print("Размер поля: ",fldS, "   Количество мин: ", np.sum(mines))
    print("X - горизонтальная координата\nY - вертикальная координата\nAction:\nopen - открыть ячейку XY\nflag - пометить открыть ячейку XY флажком \n")
    
    offset=len(str(fldS))
    print("x/y"," "*(offset-1),"|",sep="",end='')

    for i in range(fldS):
      # print("%i | " % (i+1), end='')
      print(" "*int(len(str(i+1)) < 3),"%i" % (i+1), " "*int(len(str(i+1)) < 2), "|",sep="",  end='')

    print("")
    print("—"*offset,"——•",sep="", end='')
    for j in range(fldS): 
        print("••••", end='')

    for y in range(fldS):
        print("")
        print(" %i"%(y+1)," "*(offset+1-len(str(y+1))),"•",sep="",end='')
        for x in range(fldS): print(" %s |" %cellSymbol(y,x),end='')
        print("")
        print("—"*offset,"——•",sep="", end='')
        for j in range(fldS): print("---+", end='')

    print("")
    
    print("\nДля выхода в меню используйте 'quit'\n-----------------------------")
    #print(mines)
    #print(revealed)
    #print(flags)
    #print(calcneared)

def drawMenu():
    clear()
    os.system("mode con cols=100 lines=25")
    for row in range (1 + 2*int(not gameActive) ,len(menuText)+1):
        print(row - 2*int(not gameActive) , ". ", menuText[row-1])
    print("_________________________\nВыберете пункт меню: ", end='')

def Continue():
    if(not gameActive): return 0 
    while True:
        if(not Game()): break

def startSetup():
    global mines
    global flags
    global revealed
    global calcneared
    mines = np.zeros(shape=(fldS,fldS), dtype=int)
    flags = np.zeros(shape=(fldS,fldS), dtype=bool)     #Массив для флажков
    revealed = np.zeros(shape=(fldS,fldS), dtype=bool)  #Массив открытых ячеек
    calcneared = np.zeros(shape=(fldS,fldS), dtype=int)

def NewGame():
    clear()
    print("Новая игра\nМаксимальный размер поля 30")
    global fldS, numMines
    fldS, numMines =  (int(i) for i in startInput())
    print("Размер:",fldS,"Мины:", numMines)
    
    startSetup() 
    global firstOpen
    firstOpen=True
    global gameActive
    gameActive = True
    while True:
        if(not Game()): break
        
    return 0

cipher = {
    '0': '8',
    '1': '9',
    '2': 'a',
    '3': 'b',
    '4': 'c',
    '5': 'd',
    '6': 'e',
    '7': 'f',
    '8': '0',
    '9': '1',
    'a': '2',
    'b': '3',
    'c': '4',
    'd': '5',
    'e': '6',
    'f': '7'
}

def SaveGame():
    if(not gameActive): return 0 
    clear()
    file = open("SavedGames.txt", "a")
    #number = sum(1 for line in file)
    #двоичные строки из массивов
    SavedStr=''
    infoStr=['','','']

    for i in range(0,fldS):
        for j in range(0,fldS):
            infoStr[0]+=str(mines[i][j])
            infoStr[1]+=str(int(revealed[i][j]))
            infoStr[2]+=str(int(flags[i][j]))

    for i in range(0,3):     
       SavedStr+=infoStr[i]
    #print(SavedStr)
    
    SavedStr = hex(int(SavedStr,2))
    SavedStr= SavedStr.replace('0x', '')
    time.sleep(5)
    
    SavedStr = str(int(firstOpen)) + SavedStr #добавление параметра первого открытия в начало строки
    #print(SavedStr)
    SavedStr = [cipher[letter] for letter in SavedStr] #шифровка 16-тиричной системы согласно словарю
    SavedStr = ''.join(SavedStr)
    #print(SavedStr)
    time.sleep(5)
    SavedStr = str(fldS)+" " + SavedStr #добавление размера поля в начало строки
    while True:
        Input = 0
        Input = str(input("Имя сохранения: ")).split()
        if(len(Input)==1):
            SavedStr = Input[0] + " " + SavedStr
            break
        print("Пожалуйста, введите имя без пробела")
        
    file.write(SavedStr+ "\n")
    file.close()
    print("Файл сохранен")
    time.sleep(3)
    #file.write("hello world")
    #file.close()


def LoadGame():
    clear()
    try:
        file = open("SavedGames.txt", "r")
        Info = file.read().split('\n')
        file.close()
    except IOError:
        print("Нет доступных сохранений")
        time.sleep(3)
        return 0
    print("Доступные сохранения:")
    for i in range (0,len(Info)-1):
        index = Info[i].find(' ')     #  Находит на каком месте впервые встречается ' '
        print(i+1,") ", Info[i][0 : (index)], sep='')
        #print(i+1,") ", Info[i], sep='')

    choose = int(input("--------------------------\nВведите цифру сохранения: "))

    infoStr=['','','']
    Readed = Info[choose-1].split()
    #print([Readed[1]])
    SavedStr = [cipher[letter] for letter in Readed[2]] #расшифровка согласно словарю
    SavedStr = ''.join(SavedStr)

    global firstOpen
    firstOpen = ("1" == SavedStr[0])
    #print(SavedStr)
    SavedStr=SavedStr[1:]  #убирание его из строки
    #print(SavedStr)

    #firstChar=SavedStr[0] #cчитывание второго (первого) символа о размере поля
    global fldS
    fldS = int(Readed[1])
    #print(fldS)
    #убирание его из строки
    #print(SavedStr)
    SavedStr = bin(int(SavedStr, 16))
    SavedStr = SavedStr.replace('0b','')
    for i in range(0,(int(fldS)**2*3-len(SavedStr))):
        SavedStr = "0" + SavedStr

    fldS2=fldS**2
    for i in range(0,fldS2):
        infoStr[0]+= SavedStr[fldS2*0+i]
        infoStr[1]+= SavedStr[fldS2*1+i]
        infoStr[2]+= SavedStr[fldS2*2+i]
    
    global mines
    global flags
    global revealed

    mines = np.zeros(shape=(fldS,fldS), dtype=int)
    flags = np.zeros(shape=(fldS,fldS), dtype=bool)     #Массив для флажков
    revealed = np.zeros(shape=(fldS,fldS), dtype=bool)  #Массив открытых ячеек

    for i in range(0,fldS):
        for j in range(0,fldS):
            mines[i][j] = infoStr[0][i*fldS+j]
            revealed[i][j] = ("1" == infoStr[1][i*fldS+j])
            flags[i][j] = ("1" == infoStr[2][i*fldS+j])

    global gameActive
    gameActive = True 
    
    #print(mines,flags,revealed)

    time.sleep(1)

    while True:
        if(not Game()): break
    #print(mines,flags,revealed)

    
def Exit():
    clear()
    print("До скорых встреч!")
    exit(0)



menuFunctions = {
    1: Continue,
    2: SaveGame,
    3: LoadGame,
    4: NewGame,
    5: Exit
}

if __name__ == "__main__":
    
    
    while True:
        try:
            drawMenu()
            menuFunctions[int(input()) + 2*int(not gameActive)]()

        except (KeyError,ValueError):
            print("Введите корректно")
            pass
        