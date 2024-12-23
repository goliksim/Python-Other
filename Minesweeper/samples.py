
"""
file = open("SavedGames.txt", "a")
str1 = "hello world"
file.write(str1+ "\n")
file.close()
file = open("SavedGames.txt", "a")
str2 = "fuck world"
file.write(str2 + "\n")
file.close()
#file = open("SavedGames.txt", "r")









try:
    a, b, c = input().split()
    a, b = int(a), int(b)
    print(a,type(a),b,type(b),c,type(c))
except ValueError:
    print("Неверный формат ввода.")

#-------------------------------------------
#привем работы с классами python 


class Vehicle(object): 
    def __init__(self, color, doors, tires, vtype): #переменные класса
        self.color = color
        self.doors = doors
        self.tires = tires
        self.vtype = vtype
    
    def brake(self):                        #публичный метод brake

        return "%s braking" % self.vtype
        
    def drive(self):

        return "I'm driving a %s %s!" % (self.color, self.vtype)

    def __doors(self):                      #приватные методы
        
        print("%s has %i doors" % (self.vtype, self.doors))

    def __tires(self):                      #приватные методы
        
        print("%s has %i tires" % (self.vtype, self.tires))

    def properties(self):
        self.__doors()
        self.__tires()

class Car(Vehicle):                         #наследуемый класс 
   
    def brake(self):                        #переписанный метод brake для этого подкласса
        
        return "The car class is breaking slowly!"
 
 #---------------------------------

if __name__ == "__main__":                  # проверка на запуск как автономный файл
    truck = Vehicle("red", 3, 6, "truck")
    print(truck.drive())
    print(truck.brake())
    car = Car("yellow", 2, 4, "car")
    print(car.brake())
    print(car.drive())
    truck.properties()
    car.properties()
    try:
        car.__doors()
    except AttributeError:
        print("попытка доступа к приватной переменной")
"""