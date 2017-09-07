""" NandProject Written by Park Jongmin 
    project #3 from CS492 "Nand to Tetris"

    Usages: python nandify.py (inputfile)       [Try this ->] python nandify.py testInput.txt
     - inputfile is optional
     - It will get inputs from stdin if you miss giving inputfile as an argument
     - It will make some .hdl files corresponding to your inputs in the same directory with the code("nandify.py")

    Developed with Python 2.7.13 on Window 10 and Ubuntu 17.??
"""
import fileinput

class Stack:
    def __init__(self):
        self.content = []

    def push(self, e):
        self.content.append(e)
        
    def pop(self):
        return self.content.pop(-1)
        
    def __str__(self):
        return str(self.content)
        
class Queue:
    def __init__(self):
        self.content = []
        
    def enqueue(self, e):
        self.content.append(e)
        
    def dequeue(self):
        return self.content.pop(0)
        
    def __str__(self):
        return str(self.content)

""" (a line of string) => (hdl file) 
    Convert given string to a hdl file """
class Parser:
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    op = ['~', '+', '*', '->']
    def __init__(self, string, lineNo):
        self.fileName = string.replace(" ", "").split("=")[0]
        try:
            self.formula = string.replace(" ", "").split("=")[1]
        except:
            self.formula = ""
        self.lineNo = lineNo
        self.outQueue = Queue()
        self.opStack = Stack()
        self.stack = Stack()

    def syntaxError(self, targetSymbol):
        print("Syntax Error at line " + str(self.lineNo) + ": Please check around your symbol '" + targetSymbol + "'")

    def infixToPostfix(self):
        if self.formula == "":
            print("Systax Error at line " + str(self.lineNo) + ": Your input is not in form of 'Name = formula'")
            return False
        symbol = "" # This is for tokenizing symbols
        implying = False
        for letter in self.formula:
            if letter in Parser.number:
                if symbol == "":
                    self.syntaxError(letter)
                    return False
                else:
                    symbol += letter
                    continue
                    
            if letter in Parser.alphabet:
                symbol += letter
                continue
            
            if symbol != "":
                if symbol == "out" or symbol[:2] == "pin":
                    print("Input symbols should not be 'out' or 'pin...'")
                    return False
                self.outQueue.enqueue(symbol)
                symbol = ""
            
            if letter == '>':
                if implying:
                    while self.opStack.content != [] and self.opStack.content[-1] in ['~', '*', '+', '->']:
                        self.outQueue.enqueue(self.opStack.pop())
                    self.opStack.push('->')
                    implying = False
                else:
                    print("Syntax Error at line " + str(self.lineNo) + ": Symbol '>' is incorrectly used")
                    return False

            elif implying:
                print("Syntax Error at line " + str(self.lineNo) + ": Symbol '-' is incorrectly used")
                return False

            elif letter == '-':
                implying = True
                continue

            elif letter == '+':
                while self.opStack.content != [] and self.opStack.content[-1] in ['~', '*', '+']:
                    self.outQueue.enqueue(self.opStack.pop())
                self.opStack.push('+')

            elif letter == '*':
                while self.opStack.content != [] and self.opStack.content[-1] in ['~', '*']:
                    self.outQueue.enqueue(self.opStack.pop())
                self.opStack.push('*')

            elif letter == '~':
                if self.opStack.content != [] and self.opStack.content[-1] == '~':
                    self.opStack.pop()
                else:
                    self.opStack.push('~')

            elif letter == ('('):
                self.opStack.push('(')

            elif letter == (')'):
                while self.opStack.content != [] and self.opStack.content[-1] != '(':
                    self.outQueue.enqueue(self.opStack.pop())
                if self.opStack.content == []:
                    print("Syntax Error at line " + str(self.lineNo) + ": There are mismatched parentheses")
                    return False
                self.opStack.pop()

            else:
                print("Syntax Error at line " + str(self.lineNo) + ": Invalid character '" + letter + "'' is found")

        if symbol != "":
            self.outQueue.enqueue(symbol)

        while self.opStack.content != [] and self.opStack.content[-1] != '(':
            self.outQueue.enqueue(self.opStack.pop())
        if self.opStack.content != []:
            print("Systax Error at line " + str(self.lineNo) + ": There are mismatched parentheses")
            return False
        return True

    # '#' stands for "NAND"
    def nandify(self):
        self.stack.content = []
        for token in self.outQueue.content:
            if token == '~':
                try:
                    operand2 = self.stack.pop()
                except:
                    print("Systax Error at line " + str(self.lineNo) + ": Operator without enough operand")
                    return False
                if operand2[-1] == '~':
                    operand2.pop(-1)
                else:
                    operand2.append('~')
                self.stack.push(operand2)

            elif token == '*':
                try:
                    operand2 = self.stack.pop()
                    operand1 = self.stack.pop()
                except:
                    print("Systax Error at line " + str(self.lineNo) + ": Operator without enough operand")
                    return False
                operand2.append('#')
                operand2.append('~')
                self.stack.push(operand1 + operand2)

            elif token == '+':
                try:
                    operand2 = self.stack.pop()
                    operand1 = self.stack.pop()
                except:
                    print("Systax Error at line " + str(self.lineNo) + ": Operator without enough operand")
                    return False
                if operand1[-1] == '~':
                    operand1.pop(-1)
                else:
                    operand1.append('~')
                if operand2[-1] == '~':
                    operand2.pop(-1)
                else:
                    operand2.append('~')
                operand2.append('#')
                self.stack.push(operand1 + operand2)

            elif token == '->':
                try:
                    operand2 = self.stack.pop()
                    operand1 = self.stack.pop()
                except:
                    print("Systax Error at line " + str(self.lineNo) + ": Operator without enough operand")
                    return False
                if operand2[-1] == '~':
                    operand2.pop(-1)
                else:
                    operand2.append('~')
                operand2.append('#')
                self.stack.push(operand1 + operand2)

            else:
                temp = []
                temp.append(token)
                self.stack.push(temp)
        if len(self.stack.content) > 1:
            print("Systax Error at line " + str(self.lineNo) + ": Operand without operator")
            return False
        self.stack.content = self.stack.content[0]
        if len(self.stack.content) == 1:
            print("Systax Error at line " + str(self.lineNo) + ": At least one operator is needed")
            return False
        return True

    def writeHDL(self):
        inputs = set(self.stack.content) - set(['~', '#'])
        f = open(self.fileName + ".hdl", 'w')
        f.write("// This file is created by NandProject\n// File name: " + self.fileName + ".hdl\n\n")
        
        head = "CHIP " + self.fileName + " {\n\tIN "
        for _input in inputs:
            head += _input + ", "
        head = head[:-2]
        head += ";\n\tOUT out;\n\n\tPARTS:\n"
        f.write(head)
        
        pinNo = 0
        body = ""
        
        rStack = []
        for token in self.stack.content[:-1]:
            if token == '#':
                b = rStack.pop(-1)
                a = rStack.pop(-1)
                out = "pin" + str(pinNo)
                pinNo += 1
                body += "\t\tNand(a=" + a + ", b=" + b + ", out=" + out + ");\n"
                rStack.append(out)

            elif token == '~':
                _in = rStack.pop(-1)
                out = "pin" + str(pinNo)
                pinNo += 1 
                body += "\t\tNand(a=" + _in + ", b=" + _in + ", out=" + out + ");\n"
                rStack.append(out)

            else:
                rStack.append(token)
        
        if self.stack.content[-1] == '#':
            b = rStack.pop(-1)
            a = rStack.pop(-1)
            body += "\t\tNand(a=" + a + ", b=" + b + ", out=out);\n"

        elif self.stack.content[-1] == '~':
            _in = rStack.pop(-1)
            body += "\t\tNand(a=" + _in + ", b=" + _in + ", out=out);\n"
        
        f.write(body + "}")
        f.close()


    def parse(self):
        if self.infixToPostfix():
            print self.outQueue.content
            if self.nandify():
                print self.stack.content
                self.writeHDL()
            else:
                self.stack.content = []
        else:
            self.opStack.content = []
            self.outQueue.content = []


if __name__ == "__main__":
    lineNo = 1
    for line in fileinput.input():
        parsethis = Parser(line.strip("\n"), lineNo)
        lineNo += 1
        parsethis.parse()