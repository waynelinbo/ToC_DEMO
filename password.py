import random

class password():
    def __init__(self):
        self.password = 0
        self.up = 0
        self.down = 0
        self.restart()
    
    def compare(self, num):
        if num < self.down:
            return -2
        elif num > self.up:
            return 2
        elif num < self.password:
            self.down = num + 1
            return -1
        elif num > self.password:
            self.up = num - 1
            return 1
        else:
            return 0
        

    def restart(self):
        self.password = int((random.random())*1000)
        self.up = 999
        self.down = 0
        print(self.password)

"""
p = password()

while(1):

    x = input(str(p.down) + " ~ " + str(p.up) + " : ")
    try :
        c = p.compare(int(x)) 
    except TypeError :
        print("please input an integer1")
        continue
    except ValueError:
        print("please input an integer2")
        continue

    if(c == -2) | (c == 2):
        print("error\n")
    #elif (c == 1) | (c == -1):
        #print(str(p.down) + " ~ " + str(p.up))
    elif c == 0:
        print("congratulations\n")
"""
