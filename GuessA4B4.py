import random

class GuessA4B4():
    def __init__(self):
        self.answer = ""
        self.record = ""
        self.generate()

    def generate(self):
        self.record = ""
        a = int((random.random())*10)
        b = int((random.random())*10)
        while b == a :
            b = int((random.random())*10)
        c = int((random.random())*10)
        while (c == a) | (c == b) :
            c = int((random.random())*10)
        d = int((random.random())*10)
        while (d == a) | (d == b) | (d == c) :
            d = int((random.random())*10)
        st = str(a) + str(b) + str(c) + str(d)
        print(st)
        self.answer = st
    
    def compare(self, st, m):
        if len(st) != 4:
            return "0"
        try :
            num = int(st)
        except ValueError:
            return "1"

        for i in range(4):
            for j in range(i+1,4):
                if st[i] == st[j] :
                    return "2"

        A = 0
        B = 0
        for i in range(4):
            for j in range(4):
                if i == j :
                    if st[i] == self.answer[j] :
                        A += 1
                else :
                    if st[i] == self.answer[j] :
                        B += 1
        if m == 0:
            self.record += st + " => "+ str(A) + "A" + str(B) + "B" + "\n"

        if A == 4:
            return "-1"
        else:
            return str(A) + "A" + str(B) + "B"

"""
s = GuessA4B4()

while(1):

    x = input("4 integers : ")
    a = s.compare(x)

    if a == "2":
        print("please input 4 different intreger\n")
    elif a == "1":
        print("please input 4 \"integer\"\n")
    elif a == "0":
        print("please input \"4\" integer\n")
    elif a == "-1":
        print("congratulations\n")
        s.generate()
    else:
        print(a + "\n")
"""