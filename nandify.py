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

""" Simple Binary Tree """
class Tree:
    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None

    def addLeft(self, data):
        leftChild = Tree(data)
        self.left = leftChild
    
    def addRight(self, data):
        rightChild = Tree(data)
        self.right = rightChild

# Not implemented yet
    def traverse(self):
        return 0

""" (A line of string) => (Simple Binary Tree) 
    Convert given string to a simple binary tree """
class Parser:
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    def __init__(self, string, lineNo):
        self.string = string.replace(" ", "")
        self.tree = Tree()
        self.lineNo = lineNo
        self.outQueue = Queue()
        self.opStack = Stack()

    def syntaxError(self, targetSymbol):
        print("Syntax Error at line " + str(self.lineNo) + ": Please check around your symbol '" + targetSymbol + "'")

    def infixToPostfix(self):
        symbol = "" # This is for tokenizing symbols
        for letter in self.string:
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
                self.outQueue.enqueue(symbol)
                symbol = ""

            if letter == '+':
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
                print("Syntax Error at line " + str(self.lineNo) + ": Invalid character is found")

        if symbol != "":
            self.outQueue.enqueue(symbol)

        while self.opStack.content != [] and self.opStack.content[-1] != '(':
            self.outQueue.enqueue(self.opStack.pop())
        if self.opStack.content != []:
            print("Systax Error at line " + str(self.lineNo) + ": There are mismatched parentheses")
            return False
        return True


parsethis = Parser("aa3+b31*c4(*d+e)", 1)
parsethis.infixToPostfix()
print parsethis.outQueue

parsethis = Parser("aa3+b3i(*c4*(d+e)", 1)
parsethis.infixToPostfix()
